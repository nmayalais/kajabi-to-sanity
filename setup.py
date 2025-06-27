#!/usr/bin/env python
"""Setup script for Kajabi to Sanity migration tool."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="kajabi-to-sanity",
    version="1.0.0",
    author="Nicholas Ayala",
    author_email="your.email@example.com",
    description="Extract blog posts from Kajabi and convert to Sanity CMS format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nmayalais/kajabi-to-sanity",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "kajabi-to-sanity=extract_kajabi:main",
        ],
    },
    keywords="kajabi sanity cms migration blog scraping",
    project_urls={
        "Bug Reports": "https://github.com/nmayalais/kajabi-to-sanity/issues",
        "Source": "https://github.com/nmayalais/kajabi-to-sanity",
    },
)