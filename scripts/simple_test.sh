#!/bin/bash
# Simple script to run the local server

echo "===== Starting Local Jekyll Server ====="

# Navigate to website root directory
cd "$(dirname "$0")/.." 

# Apply any pending filename fixes
if [ -f "./scripts/fix_filenames.py" ]; then
  echo "Fixing any filenames with spaces..."
  python ./scripts/fix_filenames.py
fi

# Build and serve the site locally
echo "Starting Jekyll server..."
bundle exec jekyll serve --livereload

# This will:
# - Build the site
# - Serve it at http://localhost:4000
# - Automatically refresh when changes are made
