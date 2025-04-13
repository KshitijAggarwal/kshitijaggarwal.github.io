# Obsidian to Website Publishing System

A minimal system for publishing selected Obsidian notes to your GitHub Pages website.

## Quick Start

1. Mark a note for publication by adding this to its frontmatter:
   ```yaml
   ---
   title: "Your Note Title"
   date: 2025-04-13
   publish: true
   ---
   ```

2. Run the publishing script:
   ```bash
   cd /Users/kshitijaggarwal/Documents/Personal/Website/kshitijaggarwal.github.io/scripts
   python publish_notes.py
   ```

3. Test the website locally:
   ```bash
   cd /Users/kshitijaggarwal/Documents/Personal/Website/kshitijaggarwal.github.io/scripts
   ./simple_test.sh
   ```

4. Open your browser to http://localhost:4000 to see the result

## Essential Files

- **publish_notes.py** - Processes Obsidian notes and publishes them to the website
- **simple_test.sh** - Runs the Jekyll server locally for testing
- **fix_filenames.py** - Utility to replace spaces with hyphens in filenames

## Directory Paths in Frontmatter

You can control where your note appears on the website by using the `website_path` frontmatter option:

```yaml
---
title: "Understanding Machine Learning"
date: 2025-04-13
publish: true
website_path: "blog/machine-learning/concepts"
---
```

This will place the note in the corresponding directory structure on your website.
