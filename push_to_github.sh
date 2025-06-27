#!/bin/bash
# Commands to push to GitHub after creating the repository

# Add the remote origin (replace with your actual repository URL)
git remote add origin https://github.com/nmayalais/kajabi-to-sanity.git

# Push to GitHub
git branch -M main
git push -u origin main

echo "Repository pushed to GitHub successfully!"