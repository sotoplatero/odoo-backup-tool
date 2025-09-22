#!/usr/bin/env python3
"""
Odoo Backup Tool
Interactive tool for backing up Odoo databases and filestore
"""

import os
import sys
import subprocess
import zipfile
import tempfile
from pathlib import Path
from datetime import datetime
from typing import List, Optional

import click
import psycopg2
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.progress import track

console = Console()


def get_databases(host: str, port: int, user: str, password: str) -> List[str]:
    """Get list of available databases"""
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database='postgres'
        )
        cur = conn.cursor()
        cur.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
        databases = [row[0] for row in cur.fetchall()]
        cur.close()
        conn.close()
        return databases
    except Exception as e:
        console.print(f"[red]Error connecting to PostgreSQL: {e}[/red]")
        sys.exit(1)


def create_db_backup(host: str, port: int, user: str, password: str, database: str, output_file: str):
    """Create database backup using pg_dump"""
    env = os.environ.copy()
    if password:
        env['PGPASSWORD'] = password

    cmd = [
        'pg_dump',
        '-h', host,
        '-p', str(port),
        '-U', user,
        '-d', database,
        '--no-password',
        '-f', output_file
    ]

    try:
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        if result.returncode != 0:
            console.print(f"[red]Error creating database backup: {result.stderr}[/red]")
            return False
        return True
    except FileNotFoundError:
        console.print("[red]pg_dump not found. Please install PostgreSQL client tools.[/red]")
        return False


def create_filestore_backup(filestore_path: str, temp_dir: str) -> str:
    """Create filestore backup"""
    filestore_backup = os.path.join(temp_dir, "filestore.zip")

    if not os.path.exists(filestore_path):
        console.print(f"[yellow]Filestore path not found: {filestore_path}[/yellow]")
        return None

    with zipfile.ZipFile(filestore_backup, 'w', zipfile.ZIP_DEFLATED) as zipf:
        filestore_path_obj = Path(filestore_path)
        for file_path in track(list(filestore_path_obj.rglob('*')), description="Backing up filestore..."):
            if file_path.is_file():
                arcname = file_path.relative_to(filestore_path_obj.parent)
                zipf.write(file_path, arcname)

    return filestore_backup


def create_full_backup(db_backup: str, filestore_backup: Optional[str], output_path: str, database: str):
    """Create final ZIP backup with database and filestore"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"{database}_{timestamp}.zip"
    full_backup_path = os.path.join(output_path, backup_filename)

    os.makedirs(output_path, exist_ok=True)

    with zipfile.ZipFile(full_backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add database backup
        zipf.write(db_backup, f"{database}.sql")

        # Add filestore if exists
        if filestore_backup and os.path.exists(filestore_backup):
            zipf.write(filestore_backup, "filestore.zip")

    return full_backup_path


def detect_filestore_path(database: str) -> Optional[str]:
    """Detect Odoo filestore path automatically"""
    # Common Odoo filestore locations
    possible_paths = [
        f"/opt/odoo/data/filestore/{database}",
        f"/var/lib/odoo/filestore/{database}",
        f"/usr/local/var/odoo/filestore/{database}",
        f"/home/odoo/data/filestore/{database}",
        f"/opt/odoo/filestore/{database}",
        f"./filestore/{database}",
        f"../filestore/{database}",
        f"./data/filestore/{database}",
        f"../data/filestore/{database}",
        # Windows paths
        f"C:\\Program Files\\Odoo\\data\\filestore\\{database}",
        f"C:\\Odoo\\data\\filestore\\{database}",
        f"C:\\odoo\\filestore\\{database}",
    ]

    for path in possible_paths:
        if os.path.exists(path) and os.path.isdir(path):
            # Check if it looks like a real filestore (has some files)
            try:
                files = list(Path(path).rglob('*'))
                if len(files) > 0:  # Has some files
                    console.print(f"[green]✓ Detected filestore: {path}[/green]")
                    return path
            except (PermissionError, OSError):
                continue

    console.print(f"[yellow]⚠ Could not auto-detect filestore for database '{database}'[/yellow]")
    return None


def add_to_crontab(cron_line: str) -> bool:
    """Add or modify a line in user's crontab"""
    try:
        # Get current crontab
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        current_crontab = result.stdout if result.returncode == 0 else ""

        # Check if a similar job already exists (looking for 'uvx obx' lines)
        existing_lines = current_crontab.split('\n')
        obx_lines = [line for line in existing_lines if 'uvx obx' in line]

        if obx_lines:
            console.print(f"[yellow]⚠ Found existing obx cron job(s):[/yellow]")
            for i, line in enumerate(obx_lines, 1):
                console.print(f"  {i}. [cyan]{line.strip()}[/cyan]")

            action = Prompt.ask(
                "\nChoose action",
                choices=["replace", "add", "cancel"],
                default="replace"
            )

            if action == "cancel":
                console.print("[yellow]Cron setup cancelled[/yellow]")
                return False
            elif action == "replace":
                # Remove existing obx lines and add new one
                new_lines = [line for line in existing_lines if 'uvx obx' not in line]
                new_lines.append(cron_line.strip())
                new_crontab = '\n'.join(new_lines) + '\n'
                console.print("[green]Replacing existing obx cron job...[/green]")
            else:  # add
                new_crontab = current_crontab + cron_line + "\n"
                console.print("[green]Adding additional cron job...[/green]")
        else:
            # Check if the exact job already exists
            if cron_line.strip() in current_crontab:
                console.print("[yellow]⚠ This exact cron job already exists in your crontab[/yellow]")
                return True

            # Add new line to crontab
            new_crontab = current_crontab + cron_line + "\n"

        # Write back to crontab
        process = subprocess.Popen(['crontab', '-'], stdin=subprocess.PIPE, text=True)
        process.communicate(input=new_crontab)

        if process.returncode == 0:
            console.print("[bold green]✅ Cron job updated successfully in your crontab![/bold green]")
            return True
        else:
            console.print("[red]❌ Failed to update cron job in crontab[/red]")
            return False

    except FileNotFoundError:
        console.print("[red]❌ crontab command not found. Please install cron or add manually.[/red]")
        return False
    except Exception as e:
        console.print(f"[red]❌ Error updating crontab: {e}[/red]")
        return False


def setup_cron_job(command: str):
    """Setup cron job for automated backups"""
    console.print("\n[bold cyan]⏰ Cron Job Configuration[/bold cyan]")
    console.print("Common schedules:")
    console.print("  • [green]0 2 * * *[/green]     - Daily at 2:00 AM")
    console.print("  • [green]0 3 * * 0[/green]     - Weekly on Sunday at 3:00 AM")
    console.print("  • [green]0 1 1 * *[/green]     - Monthly on 1st at 1:00 AM")
    console.print("  • [green]0 */6 * * *[/green]   - Every 6 hours")

    cron_entry = Prompt.ask("\nEnter cron schedule", default="0 2 * * *")
    full_command = f"{cron_entry} {command}"

    console.print(f"\n[bold yellow]📋 Cron job to be added:[/bold yellow]")
    console.print(f"[bold green]{full_command}[/bold green]")

    # Ask if user wants automatic addition to crontab
    if Confirm.ask("\nAdd this cron job to your crontab automatically?", default=True):
        success = add_to_crontab(full_command)

        if success:
            console.print("\n[bold]✅ Setup complete![/bold]")
            console.print("Your automated backup is now configured.")
            console.print("\n[bold]To verify:[/bold]")
            console.print("Run: [cyan]crontab -l[/cyan]")
        else:
            console.print(f"\n[bold yellow]📋 Manual setup required:[/bold yellow]")
            console.print("1. Run: [cyan]crontab -e[/cyan]")
            console.print("2. Add the line above")
            console.print("3. Save and exit")
    else:
        console.print(f"\n[bold yellow]📋 Manual setup:[/bold yellow]")
        console.print("1. Run: [cyan]crontab -e[/cyan]")
        console.print("2. Add the line above")
        console.print("3. Save and exit")

    console.print("\n[dim]💡 Tip: Test the command manually first to ensure it works![/dim]")


@click.command()
@click.option('--host', default=None, help='PostgreSQL host')
@click.option('--port', default=None, type=int, help='PostgreSQL port')
@click.option('--user', default=None, help='PostgreSQL user')
@click.option('--password', default=None, help='PostgreSQL password')
@click.option('--database', default=None, help='Database name')
@click.option('--filestore-path', default=None, help='Odoo filestore path')
@click.option('--output-path', default=None, help='Output directory for backups')
@click.option('--setup-cron', is_flag=True, help='Setup cron job for automated backups')
@click.option('--non-interactive', is_flag=True, help='Run in non-interactive mode')
def main(host, port, user, password, database, filestore_path, output_path, setup_cron, non_interactive):
    """Odoo Backup Tool - Interactive backup for Odoo databases and filestore"""

    console.print("[bold blue]🗄️  Odoo Backup Tool[/bold blue]")
    console.print()

    # Interactive mode if parameters not provided
    if not non_interactive:
        if not host:
            host = Prompt.ask("PostgreSQL host", default="localhost")
        if not port:
            port = int(Prompt.ask("PostgreSQL port", default="5432"))
        if not user:
            user = Prompt.ask("PostgreSQL user", default="odoo")
        if not password:
            password = Prompt.ask("PostgreSQL password", password=True, default="")
    else:
        # Set defaults for non-interactive mode
        host = host or "localhost"
        port = port or 5432
        user = user or "odoo"
        password = password or ""

    # Get available databases if not specified
    if not database:
        console.print("\n[bold]Available databases:[/bold]")
        databases = get_databases(host, port, user, password)

        if not databases:
            console.print("[red]No databases found[/red]")
            sys.exit(1)

        table = Table()
        table.add_column("Index", style="cyan")
        table.add_column("Database", style="green")

        for i, db in enumerate(databases, 1):
            table.add_row(str(i), db)

        console.print(table)

        if non_interactive:
            console.print("[red]Database must be specified in non-interactive mode[/red]")
            sys.exit(1)

        choice = Prompt.ask("\nSelect database index", choices=[str(i) for i in range(1, len(databases) + 1)])
        database = databases[int(choice) - 1]

    # Get filestore path - try auto-detection first
    if not filestore_path:
        console.print(f"\n[bold]🔍 Auto-detecting filestore for database '{database}'...[/bold]")
        detected_filestore = detect_filestore_path(database)

        if detected_filestore:
            filestore_path = detected_filestore
        elif not non_interactive:
            # Fallback to asking user if auto-detection fails
            default_filestore = f"/opt/odoo/data/filestore/{database}"
            console.print(f"[yellow]Please specify the filestore path manually:[/yellow]")
            filestore_path = Prompt.ask("Filestore path", default=default_filestore)
        else:
            # Non-interactive mode fallback
            filestore_path = f"/opt/odoo/data/filestore/{database}"
            console.print(f"[yellow]Using default filestore path: {filestore_path}[/yellow]")

    # Get output path
    if not output_path and not non_interactive:
        output_path = Prompt.ask("Output directory", default="./backups")
    elif not output_path:
        output_path = "./backups"

    console.print(f"\n[bold]Backup Configuration:[/bold]")
    console.print(f"Database: {database}")
    console.print(f"Filestore: {filestore_path}")
    console.print(f"Output: {output_path}")

    if not non_interactive and not Confirm.ask("\nProceed with backup?"):
        console.print("[yellow]Backup cancelled[/yellow]")
        sys.exit(0)

    # Create backup
    with tempfile.TemporaryDirectory() as temp_dir:
        console.print("\n[bold]Creating backup...[/bold]")

        # Database backup
        db_backup_file = os.path.join(temp_dir, f"{database}.sql")
        console.print("📊 Backing up database...")
        if not create_db_backup(host, port, user, password, database, db_backup_file):
            sys.exit(1)

        # Filestore backup
        filestore_backup_file = None
        if filestore_path and os.path.exists(filestore_path):
            console.print("📁 Backing up filestore...")
            filestore_backup_file = create_filestore_backup(filestore_path, temp_dir)

        # Create final backup
        console.print("🗜️  Creating final backup...")
        backup_file = create_full_backup(db_backup_file, filestore_backup_file, output_path, database)

        console.print(f"\n[bold green]✅ Backup completed successfully![/bold green]")
        console.print(f"[green]Backup saved to: {backup_file}[/green]")

        # File size
        backup_size = os.path.getsize(backup_file)
        size_mb = backup_size / (1024 * 1024)
        console.print(f"[blue]Backup size: {size_mb:.2f} MB[/blue]")

    # Ask about cron setup in interactive mode
    if not setup_cron and not non_interactive:
        console.print("\n[bold]📅 Automated Backups[/bold]")
        if Confirm.ask("Would you like to set up automatic daily backups with cron?", default=False):
            setup_cron = True

    # Setup cron if requested
    if setup_cron:
        console.print("\n[bold]Setting up cron job...[/bold]")
        command_parts = [
            f"--host {host}",
            f"--port {port}",
            f"--user {user}",
            f"--database {database}",
            f"--filestore-path '{filestore_path}'",
            f"--output-path '{output_path}'",
            "--non-interactive"
        ]
        if password:
            command_parts.append(f"--password '{password}'")

        # Use uvx obx for cron command (more modern approach)
        full_command = f"uvx obx {' '.join(command_parts)}"
        setup_cron_job(full_command)


if __name__ == "__main__":
    main()
