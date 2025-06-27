# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-06-26

### Added
- Initial release of Kajabi to Sanity migration tool
- Support for extracting blog posts from Kajabi sites
- Automatic pagination handling
- Extraction of title, date, content, tags, and featured images
- Command-line interface with multiple configuration options
- Progress tracking with tqdm
- Comprehensive logging system
- Export to Sanity-compatible NDJSON format
- Support for custom author names
- Options to skip image and tag extraction
- Debug mode for troubleshooting

### Technical Details
- Built with Python 3.7+ compatibility
- Uses Beautiful Soup 4 for HTML parsing
- Implements proper error handling and recovery
- Follows PEP 8 coding standards
- Type hints for better code maintainability