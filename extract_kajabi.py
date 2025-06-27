#!/usr/bin/env python3
"""
Kajabi Blog to Sanity CMS Migration Tool

This script extracts blog posts from a Kajabi-hosted site and converts them
to Sanity-compatible NDJSON format for import.

Author: Nicholas Ayala
License: MIT
"""

import argparse
import json
import logging
import re
import sys
from datetime import datetime
from typing import Dict, List, Optional, Set
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

__version__ = "1.0.0"


class KajabiToSanityMigrator:
    """Handles the migration of blog posts from Kajabi to Sanity CMS."""
    
    def __init__(self, base_url: str = "https://www.nicholasayala.com", 
                 blog_path: str = "/blog",
                 output_file: str = "sanity_import.ndjson"):
        """
        Initialize the migrator with configuration.
        
        Args:
            base_url: The base URL of the Kajabi site
            blog_path: The path to the blog section
            output_file: The output NDJSON file name
        """
        self.base_url = base_url.rstrip('/')
        self.blog_path = blog_path.rstrip('/')
        self.blog_url = f"{self.base_url}{self.blog_path}"
        self.output_file = output_file
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; KajabiToSanityMigrator/1.0)'
        })
        
        # Default options (can be overridden)
        self.default_author = "Nicholas Ayala"
        self.extract_images = True
        self.extract_tags = True
        
        self.logger = logging.getLogger(__name__)
    
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Fetch a page and return parsed HTML.
        
        Args:
            url: The URL to fetch
            
        Returns:
            BeautifulSoup object or None if error
        """
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            self.logger.error(f"Error fetching {url}: {e}")
            return None
    
    def extract_blog_urls(self) -> List[str]:
        """
        Extract all blog post URLs from the blog listing pages.
        
        Returns:
            List of blog post URLs
        """
        blog_urls: Set[str] = set()
        page = 1
        
        self.logger.info("Starting blog URL extraction...")
        
        while True:
            page_url = f"{self.blog_url}?page={page}"
            self.logger.info(f"Fetching page {page}: {page_url}")
            
            soup = self.fetch_page(page_url)
            if not soup:
                break
            
            # Find blog post links using the specific class
            post_links = soup.select('a.blog-listing__title')
            new_urls = 0
            
            for link in post_links:
                href = link.get('href', '')
                if href and href.startswith('/blog/'):
                    full_url = urljoin(self.base_url, href)
                    if full_url not in blog_urls:
                        blog_urls.add(full_url)
                        new_urls += 1
                        self.logger.debug(f"Found: {link.get_text(strip=True)}")
            
            self.logger.info(f"Found {new_urls} new blog posts on page {page}")
            
            # Check if there's a next page
            if new_urls == 0 or not self.has_next_page(soup):
                break
            
            page += 1
        
        self.logger.info(f"Total blog posts found: {len(blog_urls)}")
        return sorted(list(blog_urls))
    
    def has_next_page(self, soup: BeautifulSoup) -> bool:
        """
        Check if there's a next page in pagination.
        
        Args:
            soup: BeautifulSoup object of current page
            
        Returns:
            True if next page exists
        """
        # Look for the next page link in pagination
        next_link = soup.select_one('a.pag__link--next')
        if next_link and next_link.get('href'):
            return True
        
        # Alternative: check if current page has a next sibling in pagination
        current_page = soup.select_one('a.pag__link--current')
        if current_page:
            next_sibling = current_page.find_next_sibling('a', class_='pag__link')
            if next_sibling and not 'next' in next_sibling.get('class', []):
                return True
        
        return False
    
    def extract_post_data(self, url: str) -> Optional[Dict]:
        """
        Extract data from a single blog post.
        
        Args:
            url: The blog post URL
            
        Returns:
            Dictionary with post data or None if error
        """
        soup = self.fetch_page(url)
        if not soup:
            return None
        
        try:
            # Extract title
            title_elem = soup.select_one('.blog-post-body__title')
            if not title_elem:
                title_elem = soup.find('h1')
            title = title_elem.get_text(strip=True) if title_elem else "Untitled"
            
            # Extract date
            date_elem = soup.select_one('.blog-post-body__date')
            if date_elem:
                # Parse date format like "Apr 30, 2025"
                date_text = date_elem.get_text(strip=True)
                try:
                    from datetime import datetime
                    parsed_date = datetime.strptime(date_text, "%b %d, %Y")
                    published_at = parsed_date.isoformat() + 'Z'
                except:
                    published_at = datetime.now().isoformat() + 'Z'
            else:
                published_at = datetime.now().isoformat() + 'Z'
            
            # Extract body content
            body_elem = soup.select_one('.blog-post-body__content')
            if not body_elem:
                # Fallback selectors
                body_elem = soup.find('div', class_='kajabi-rich-text') or soup.find('main')
            
            body = body_elem.get_text(strip=True) if body_elem else ""
            
            # Extract tags if enabled
            tags = []
            if self.extract_tags:
                tag_elements = soup.select('.blog-post-body__tags .tag')
                for tag in tag_elements:
                    tags.append(tag.get_text(strip=True))
            
            # Extract slug from URL
            path = urlparse(url).path
            slug = path.split('/')[-1] or path.split('/')[-2]
            
            # Extract featured image if enabled
            featured_image = None
            if self.extract_images:
                image_elem = soup.select_one('.blog-post-body__media img')
                featured_image = image_elem.get('src') if image_elem else None
            
            post_data = {
                "_type": "post",
                "title": title,
                "slug": {
                    "_type": "slug",
                    "current": slug
                },
                "publishedAt": published_at,
                "body": body,
                "sourceUrl": url,
                "author": self.default_author
            }
            
            # Add optional fields if available
            if tags and self.extract_tags:
                post_data["tags"] = tags
            if featured_image and self.extract_images:
                post_data["featuredImageUrl"] = featured_image
            
            return post_data
            
        except Exception as e:
            self.logger.error(f"Error extracting data from {url}: {e}")
            return None
    
    def save_to_ndjson(self, posts: List[Dict]) -> None:
        """
        Save posts to NDJSON file for Sanity import.
        
        Args:
            posts: List of post dictionaries
        """
        with open(self.output_file, 'w', encoding='utf-8') as f:
            for post in posts:
                json.dump(post, f, ensure_ascii=False)
                f.write('\n')
        
        self.logger.info(f"Saved {len(posts)} posts to {self.output_file}")
    
    def run(self) -> None:
        """Run the complete migration process."""
        self.logger.info("Starting Kajabi to Sanity migration...")
        
        # Extract blog URLs
        blog_urls = self.extract_blog_urls()
        
        if not blog_urls:
            self.logger.warning("No blog posts found!")
            return
        
        # Extract data from each post
        posts = []
        for url in tqdm(blog_urls, desc="Extracting posts"):
            post_data = self.extract_post_data(url)
            if post_data:
                posts.append(post_data)
                self.logger.debug(f"Extracted: {post_data['title']}")
        
        # Save to NDJSON
        self.save_to_ndjson(posts)
        
        self.logger.info(f"Migration complete! Extracted {len(posts)} posts.")
        self.logger.info(f"Run 'sanity dataset import {self.output_file} production' to import.")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Extract blog posts from Kajabi and convert to Sanity NDJSON format",
        epilog="Example: python extract_kajabi.py --url https://example.com --output blog_export.ndjson"
    )
    
    parser.add_argument(
        "--url",
        default="https://www.nicholasayala.com",
        help="Base URL of the Kajabi site (default: https://www.nicholasayala.com)"
    )
    
    parser.add_argument(
        "--blog-path",
        default="/blog",
        help="Path to the blog section (default: /blog)"
    )
    
    parser.add_argument(
        "--output",
        "-o",
        default="sanity_import.ndjson",
        help="Output NDJSON file name (default: sanity_import.ndjson)"
    )
    
    parser.add_argument(
        "--author",
        default="Nicholas Ayala",
        help="Default author name for posts (default: Nicholas Ayala)"
    )
    
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level (default: INFO)"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )
    
    parser.add_argument(
        "--no-images",
        action="store_true",
        help="Skip extracting featured images"
    )
    
    parser.add_argument(
        "--no-tags",
        action="store_true",
        help="Skip extracting tags"
    )
    
    args = parser.parse_args()
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Create migrator with CLI arguments
    migrator = KajabiToSanityMigrator(
        base_url=args.url,
        blog_path=args.blog_path,
        output_file=args.output
    )
    
    # Store additional options
    migrator.default_author = args.author
    migrator.extract_images = not args.no_images
    migrator.extract_tags = not args.no_tags
    
    try:
        migrator.run()
    except KeyboardInterrupt:
        logging.info("Migration interrupted by user")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Migration failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()