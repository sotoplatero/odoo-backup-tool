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