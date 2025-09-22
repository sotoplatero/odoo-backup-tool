# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Interactive Odoo backup tool that creates complete backups of Odoo databases and filestore. The tool can run interactively with prompts or non-interactively for automation/cron jobs.

## Project Structure

- `main.py` - Main backup script with interactive prompts and CLI interface
- `pyproject.toml` - Python project configuration with dependencies
- `.python-version` - Specifies Python 3.8+ requirement
- `.gitignore` - Standard Python gitignore

## Dependencies

- `click` - Command line interface framework
- `psycopg2-binary` - PostgreSQL database adapter
- `rich` - Rich text and beautiful formatting in the terminal

## Development Setup

The project requires Python 3.8+ and PostgreSQL client tools (pg_dump).

## Running the Application

### Interactive Mode (default)
```bash
python main.py
# or after installation
odoo-backup
```

### Non-interactive Mode (for automation)
```bash
python main.py --host localhost --port 5432 --user odoo --database mydb --filestore-path /path/to/filestore --output-path ./backups --non-interactive
```

### Setup Cron Job
```bash
python main.py --setup-cron
```

### Installation with uvx
```bash
uvx --from . odoo-backup
```

## Application Features

- Interactive database selection from available PostgreSQL databases
- Automatic backup of both database (SQL) and filestore (files)
- Creates compressed ZIP backups with timestamp
- Supports cron job setup for automated backups
- Rich terminal interface with progress indicators
- Configurable output directory and filestore paths
- Non-interactive mode for automation

## Default Values

- PostgreSQL host: localhost
- PostgreSQL port: 5432
- PostgreSQL user: odoo
- Filestore path: `/opt/odoo/data/filestore/{database}`
- Output directory: `./backups`