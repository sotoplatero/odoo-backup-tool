# 🗄️ Odoo Backup Tool

[![PyPI version](https://badge.fury.io/py/obx.svg)](https://badge.fury.io/py/obx)
[![Python](https://img.shields.io/pypi/pyversions/obx.svg)](https://pypi.org/project/obx/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/obx)](https://pepy.tech/project/obx)

Interactive command-line tool for creating complete backups of Odoo databases and filestore. Supports both interactive and automated modes, perfect for development, staging, and production environments.

## ✨ Features

- 🎯 **Interactive Mode**: User-friendly prompts for easy backup creation
- 🤖 **Automation Ready**: Non-interactive mode for cron jobs and scripts
- 📊 **Complete Backups**: Includes both PostgreSQL database and filestore
- 🗜️ **Compression**: Creates compressed ZIP archives with timestamps
- ⏰ **Cron Integration**: Built-in cron job setup helper
- 🎨 **Beautiful Interface**: Rich terminal output with progress indicators
- 🔧 **Flexible Configuration**: Customizable paths and connection settings

## 🚀 Quick Start

### Installation

```bash
# Install from PyPI
pip install obx

# Or run directly with uvx (recommended - no installation needed)
uvx obx
```

### Basic Usage

```bash
# Interactive mode (guided setup)
uvx obx
# or if installed: odoo-backup

# Non-interactive mode (automation)
uvx obx --host localhost --port 5432 --user odoo --database mydb --non-interactive
# or if installed: odoo-backup --host localhost --port 5432 --user odoo --database mydb --non-interactive
```

## 📋 Requirements

- Python 3.8+
- PostgreSQL client tools (`pg_dump`)
- Access to Odoo database and filestore

## 💡 Usage Examples

### Interactive Mode

Start the tool and follow the prompts:

```bash
uvx obx
# or if installed: odoo-backup
```

The tool will guide you through:
1. Database connection settings
2. Database selection from available options
3. Filestore path configuration
4. Output directory selection
5. Backup confirmation

### Automated Backups

For production environments and automated backups:

```bash
uvx obx \
  --host localhost \
  --port 5432 \
  --user odoo \
  --password mypassword \
  --database production_db \
  --filestore-path /opt/odoo/data/filestore/production_db \
  --output-path /backups \
  --non-interactive
```

### Cron Job Setup

Set up automated daily backups:

```bash
# Generate cron configuration
uvx obx --setup-cron

# This will output a cron line like:
# 0 2 * * * uvx obx --host localhost --port 5432 --user odoo --database mydb --non-interactive
```

Add the generated line to your crontab:

```bash
crontab -e
```

## ⚙️ Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `--host` | PostgreSQL server host | `localhost` |
| `--port` | PostgreSQL server port | `5432` |
| `--user` | PostgreSQL username | `odoo` |
| `--password` | PostgreSQL password | (prompted) |
| `--database` | Database name to backup | (interactive selection) |
| `--filestore-path` | Path to Odoo filestore | `/opt/odoo/data/filestore/{database}` |
| `--output-path` | Backup output directory | `./backups` |
| `--non-interactive` | Run without prompts | `false` |
| `--setup-cron` | Generate cron job configuration | `false` |

## 📁 Backup Structure

Each backup creates a timestamped ZIP file containing:

```
mydb_20240322_143052.zip
├── mydb.sql              # PostgreSQL database dump
└── filestore.zip         # Compressed filestore directory
```

## 🛠️ Development

### Local Development Setup

```bash
# Clone the repository
git clone https://github.com/sotoplatero/odoo-backup-tool.git
cd odoo-backup-tool

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e .

# Run the tool
python -m odoo_backup.cli
```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest

# Run with coverage
pytest --cov=odoo_backup
```

### Building and Publishing

```bash
# Install build tools
pip install build twine

# Build the package
python -m build

# Upload to PyPI
twine upload dist/*
```

## 🔧 Troubleshooting

### Common Issues

**`pg_dump: command not found`**
- Install PostgreSQL client tools
- On Ubuntu/Debian: `sudo apt-get install postgresql-client`
- On CentOS/RHEL: `sudo yum install postgresql`
- On macOS: `brew install postgresql`

**Permission denied accessing filestore**
- Ensure the user has read permissions to the filestore directory
- Run with appropriate user privileges or adjust file permissions

**Database connection errors**
- Verify PostgreSQL server is running
- Check connection parameters (host, port, username)
- Ensure the user has access to the target database

### Environment Variables

You can set default values using environment variables:

```bash
export PGHOST=localhost
export PGPORT=5432
export PGUSER=odoo
export PGPASSWORD=mypassword
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

- 📧 Email: soto.platero@gmail.com
- 🐛 Issues: [GitHub Issues](https://github.com/sotoplatero/odoo-backup-tool/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/sotoplatero/odoo-backup-tool/discussions)

## 🌟 Acknowledgments

- Built with [Click](https://click.palletsprojects.com/) for CLI interface
- Styled with [Rich](https://rich.readthedocs.io/) for beautiful terminal output
- PostgreSQL integration via [psycopg2](https://pypi.org/project/psycopg2/)

---

Made with ❤️ for the Odoo community