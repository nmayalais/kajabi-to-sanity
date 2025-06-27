# Kajabi to Sanity CMS Migration Tool

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

A Python tool to extract blog posts from Kajabi-hosted websites and convert them to Sanity CMS-compatible NDJSON format for easy import.

## Features

- 🚀 Crawls all blog posts with automatic pagination handling
- 📝 Extracts title, date, content, tags, and featured images
- 🔄 Converts to Sanity-compatible NDJSON format
- 🛠 Configurable via command-line arguments
- 📊 Progress tracking with detailed logging
- 🎯 Optimized for Kajabi's blog structure

## Installation

1. Clone this repository:
```bash
git clone https://github.com/nmayalais/kajabi-to-sanity.git
cd kajabi-to-sanity
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

Extract blog posts from the default site:
```bash
python extract_kajabi.py
```

This creates `sanity_import.ndjson` with all blog posts ready for import.

## Usage

### Basic Usage

```bash
python extract_kajabi.py --url https://yourkajabidomain.com --output blog_export.ndjson
```

### Command Line Options

```
usage: extract_kajabi.py [-h] [--url URL] [--blog-path BLOG_PATH] [--output OUTPUT]
                        [--author AUTHOR] [--log-level {DEBUG,INFO,WARNING,ERROR}]
                        [--version] [--no-images] [--no-tags]

Extract blog posts from Kajabi and convert to Sanity NDJSON format

optional arguments:
  -h, --help            show this help message and exit
  --url URL             Base URL of the Kajabi site (default: https://example-kajabi-site.com)
  --blog-path BLOG_PATH Path to the blog section (default: /blog)
  --output OUTPUT, -o OUTPUT
                        Output NDJSON file name (default: sanity_import.ndjson)
  --author AUTHOR       Default author name for posts (default: Author Name)
  --log-level {DEBUG,INFO,WARNING,ERROR}
                        Logging level (default: INFO)
  --version             show program's version number and exit
  --no-images           Skip extracting featured images
  --no-tags             Skip extracting tags
```

### Examples

Extract from a custom domain with debug logging:
```bash
python extract_kajabi.py --url https://example.com --log-level DEBUG
```

Extract without images and tags:
```bash
python extract_kajabi.py --no-images --no-tags --output minimal_export.ndjson
```

## Output Format

The tool generates NDJSON (newline-delimited JSON) with the following structure:

```json
{
  "_type": "post",
  "title": "Blog Post Title",
  "slug": {
    "_type": "slug",
    "current": "blog-post-url-slug"
  },
  "publishedAt": "2024-01-01T00:00:00Z",
  "body": "Full blog post content...",
  "sourceUrl": "https://example.com/blog/post-slug",
  "author": "Author Name",
  "tags": ["tag1", "tag2"],
  "featuredImageUrl": "https://example.com/image.jpg"
}
```

## Importing to Sanity

After extraction, import the data using Sanity CLI:

```bash
# Install Sanity CLI if you haven't already
npm install -g @sanity/cli

# Import the data
sanity dataset import sanity_import.ndjson production
```

### Sanity Schema

Ensure your Sanity schema includes a `post` document type. Here's a minimal example:

```javascript
// schemas/post.js
export default {
  name: 'post',
  title: 'Blog Post',
  type: 'document',
  fields: [
    {
      name: 'title',
      title: 'Title',
      type: 'string',
      validation: Rule => Rule.required()
    },
    {
      name: 'slug',
      title: 'Slug',
      type: 'slug',
      options: {
        source: 'title',
        maxLength: 96
      },
      validation: Rule => Rule.required()
    },
    {
      name: 'publishedAt',
      title: 'Published at',
      type: 'datetime'
    },
    {
      name: 'body',
      title: 'Body',
      type: 'text'
    },
    {
      name: 'author',
      title: 'Author',
      type: 'string'
    },
    {
      name: 'tags',
      title: 'Tags',
      type: 'array',
      of: [{type: 'string'}]
    },
    {
      name: 'featuredImageUrl',
      title: 'Featured Image URL',
      type: 'url'
    },
    {
      name: 'sourceUrl',
      title: 'Original URL',
      type: 'url'
    }
  ]
}
```

## Advanced Usage

### Extending the Tool

The tool is designed to be extensible. Key customization points:

1. **Custom Selectors**: Modify the CSS selectors in `extract_post_data()` method
2. **Additional Fields**: Add new fields to the extraction logic
3. **Post-Processing**: Add data transformation before export

### Converting to Portable Text

For rich text formatting, consider post-processing the content to Sanity's Portable Text format:

```python
# Example transformation (not included in base tool)
from html2text import HTML2Text

def convert_to_portable_text(html_content):
    # Convert HTML to markdown first
    h = HTML2Text()
    markdown = h.handle(html_content)
    # Then convert markdown to Portable Text
    # Implementation depends on your needs
```

## Troubleshooting

### Common Issues

1. **No posts found**: Check that the blog path is correct and the site is accessible
2. **Missing content**: Verify the CSS selectors match your Kajabi theme
3. **Date parsing errors**: The tool expects dates in "MMM DD, YYYY" format

### Debug Mode

Run with debug logging to see detailed extraction information:
```bash
python extract_kajabi.py --log-level DEBUG
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built for migrating from [Kajabi](https://kajabi.com) to [Sanity CMS](https://www.sanity.io)
- Uses [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing
- Progress bars powered by [tqdm](https://github.com/tqdm/tqdm)