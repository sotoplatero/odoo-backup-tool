# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Planned: Support for remote filestore backups (FTP/SFTP)
- Planned: Backup encryption options
- Planned: Restore functionality
- Planned: Progress webhooks for monitoring

## [0.2.2] - 2024-09-22

### Added
- 🤖 **Automatic crontab management**: Script can now add/modify cron jobs automatically
- Smart detection of existing `uvx obx` cron jobs
- Options to replace, add, or cancel when existing jobs are found
- Duplicate prevention for cron entries
- One-click crontab updates

### Enhanced
- `add_to_crontab()` function with intelligent job management
- Better user experience with automatic cron setup
- Clear action choices: replace/add/cancel existing jobs
- Immediate verification instructions after cron setup

### Features
- Automatic crontab modification using `crontab -` command
- Detection and handling of existing backup jobs
- Safe replacement of old jobs with new configurations
- Support for multiple backup jobs if needed

## [0.2.1] - 2024-09-22

### Added
- 📅 **Interactive cron setup**: Tool now asks if you want to set up automated backups after successful backup
- Enhanced cron job configuration with common schedule examples
- Improved cron command generation using `uvx obx` syntax
- Step-by-step cron activation instructions

### Changed
- Better user experience with automated cron setup flow
- Enhanced `setup_cron_job()` function with schedule examples and clear instructions
- Updated cron commands to use modern `uvx obx` syntax instead of `odoo-backup`

### Features
- Interactive prompt: "Would you like to set up automatic daily backups with cron?"
- Common schedule options: Daily, Weekly, Monthly, Every 6 hours
- Clear activation steps with `crontab -e` guidance
- Generated commands are ready-to-use and tested

## [0.2.0] - 2024-09-22

### Added
- 🔍 **Smart filestore detection**: Automatically detects Odoo filestore locations
- Added `detect_filestore_path()` function that searches common Odoo directories
- Support for multiple OS filestore paths (Linux, Windows)
- Enhanced user experience with automatic path detection

### Changed
- Improved interactive flow - users no longer need to specify filestore paths manually in most cases
- Better error handling and fallback mechanisms for filestore detection
- Enhanced console output with detection status messages

### Features
- Searches common locations: `/opt/odoo/data/filestore/`, `/var/lib/odoo/filestore/`, Windows paths, etc.
- Validates detected paths to ensure they contain actual filestore data
- Falls back to manual input if auto-detection fails
- Works in both interactive and non-interactive modes

## [0.1.3] - 2024-09-22

### Added
- Added `obx` executable alongside `odoo-backup` for direct uvx usage
- Now supports both `uvx obx` and `uvx --from obx odoo-backup` commands

### Changed
- Updated all documentation to use `uvx obx` as the primary command
- Simplified usage examples with shorter command syntax

## [0.1.2] - 2024-09-22

### Fixed
- Corrected uvx command syntax in documentation to use `uvx --from obx odoo-backup`
- Fixed all README examples to reflect the correct executable name (`odoo-backup`)
- Updated cron job examples with proper uvx syntax

## [0.1.1] - 2024-09-22

### Changed
- Updated documentation to correctly show `uvx obx` usage patterns
- Improved README with better uvx examples and installation instructions
- Enhanced cron job examples to use uvx syntax

### Fixed
- Corrected uvx command examples in documentation
- Fixed installation instructions for uvx usage

## [0.1.0] - 2024-09-22

### Added
- Interactive CLI tool for Odoo database backups
- Complete PostgreSQL database backup using `pg_dump`
- Odoo filestore backup with compression
- Rich terminal interface with progress indicators
- Non-interactive mode for automation and cron jobs
- Cron job setup helper with configuration generation
- Timestamped ZIP archive creation
- Comprehensive error handling and user feedback
- Support for custom database connection parameters
- Flexible filestore and output path configuration
- Beautiful terminal output with Rich library
- Click-based command-line interface
- Full documentation and examples

### Features
- 🎯 Interactive mode with guided prompts
- 🤖 Automation-ready non-interactive mode
- 📊 Complete backup (database + filestore)
- 🗜️ Compressed ZIP archives with timestamps
- ⏰ Built-in cron job setup
- 🎨 Rich terminal interface
- 🔧 Flexible configuration options

### Technical Details
- Python 3.8+ support
- PostgreSQL integration via psycopg2
- Click framework for CLI
- Rich library for terminal formatting
- Comprehensive error handling
- Cross-platform compatibility (Windows, Linux, macOS)

### Dependencies
- `click>=8.0.0` - CLI framework
- `psycopg2-binary>=2.9.0` - PostgreSQL adapter
- `rich>=13.0.0` - Terminal formatting

---

### Legend
- **Added** for new features
- **Changed** for changes in existing functionality
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** for vulnerability fixes