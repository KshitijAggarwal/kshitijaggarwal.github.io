#!/usr/bin/env python3
"""
Obsidian to Website Publishing Script

This script:
1. Traverses the Obsidian vault to find notes marked for publication
2. Processes them for Jekyll compatibility
3. Copies them to the website repository
4. Handles images and attachments
5. Implements safety features to prevent accidental publication

Usage:
    python publish_notes.py
"""

import os
import re
import sys
import shutil
import yaml
import datetime
import hashlib
from pathlib import Path

# Configuration
OBSIDIAN_ROOT = "/Users/kshitijaggarwal/Documents/Notes/FRBs"
WEBSITE_ROOT = "/Users/kshitijaggarwal/Documents/Personal/Website/kshitijaggarwal.github.io"
NOTES_DIR = os.path.join(WEBSITE_ROOT, "_notes")
IMAGES_DIR = os.path.join(WEBSITE_ROOT, "images")
LOG_FILE = os.path.join(WEBSITE_ROOT, "scripts", "publish_log.txt")

# Regular expression patterns
FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
OBSIDIAN_IMAGE_PATTERN = re.compile(r"!\[\[(.*?)\]\]")
OBSIDIAN_LINK_PATTERN = re.compile(r"\[\[(.*?)(\|(.*?))?\]\]")

def log_message(message):
    """Log a message to console and log file."""
    print(message)
    with open(LOG_FILE, "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {message}\n")

def create_directories():
    """Create necessary directories if they don't exist."""
    os.makedirs(NOTES_DIR, exist_ok=True)
    os.makedirs(IMAGES_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def extract_frontmatter(content):
    """Extract frontmatter from note content."""
    match = FRONTMATTER_PATTERN.match(content)
    if match:
        try:
            frontmatter = yaml.safe_load(match.group(1))
            content_without_frontmatter = content[match.end():]
            return frontmatter, content_without_frontmatter
        except yaml.YAMLError:
            return None, content
    return None, content

def should_publish(frontmatter):
    """Determine if a note should be published based on frontmatter."""
    return frontmatter and frontmatter.get("publish") is True

def get_destination_path(frontmatter, file_path):
    """Determine the destination path for a note."""
    # Get the base name without extension and replace spaces with hyphens
    base_name = os.path.basename(file_path).replace(".md", "")
    slug_base_name = base_name.replace(" ", "-")
    
    if frontmatter.get("website_path"):
        # Use custom path if specified
        # Create the path without quotes, replacing spaces with hyphens
        path_parts = frontmatter["website_path"].split('/')
        # Clean path parts (remove quotes and replace spaces with hyphens)
        clean_parts = [part.replace('"', '').replace(' ', '-') for part in path_parts]
        clean_path = os.path.join(NOTES_DIR, *clean_parts)
        
        # Ensure directory exists
        os.makedirs(clean_path, exist_ok=True)
        
        return os.path.join(clean_path, f"{slug_base_name}.md")
    
    # Default: use hyphenated filename
    return os.path.join(NOTES_DIR, f"{slug_base_name}.md")

def handle_obsidian_images(content, file_path):
    """Process Obsidian image embeds and copy images to website directory."""
    def replace_image(match):
        image_path = match.group(1)
        
        # Handle relative paths
        if not os.path.isabs(image_path):
            image_path = os.path.join(os.path.dirname(file_path), image_path)
        
        # If the image doesn't exist in the specified path, try to find it in common image directories
        if not os.path.exists(image_path):
            for root, _, files in os.walk(OBSIDIAN_ROOT):
                for file in files:
                    if file == os.path.basename(image_path):
                        possible_path = os.path.join(root, file)
                        if os.path.exists(possible_path):
                            image_path = possible_path
                            break
        
        if os.path.exists(image_path):
            # Create a hash-based filename to avoid collisions
            image_hash = hashlib.md5(image_path.encode()).hexdigest()[:8]
            image_ext = os.path.splitext(image_path)[1]
            new_image_name = f"{image_hash}{image_ext}"
            
            # Copy the image to the website images directory
            destination = os.path.join(IMAGES_DIR, new_image_name)
            shutil.copy2(image_path, destination)
            
            # Return markdown image syntax with the new path
            return f"![{os.path.basename(image_path)}](/images/{new_image_name})"
        else:
            log_message(f"Warning: Image not found: {image_path}")
            return f"![Image not found: {match.group(1)}]"
    
    return OBSIDIAN_IMAGE_PATTERN.sub(replace_image, content)

def handle_obsidian_links(content):
    """Convert Obsidian internal links to website links."""
    def replace_link(match):
        link_text = match.group(3) if match.group(3) else match.group(1)
        link_target = match.group(1).split("#")[0].strip()
        
        # Convert to Jekyll link format
        return f"[{link_text}](/notes/{link_target})"
    
    return OBSIDIAN_LINK_PATTERN.sub(replace_link, content)

def process_note_content(content, file_path):
    """Process the note content for Jekyll compatibility."""
    # Handle Obsidian-specific syntax
    content = handle_obsidian_images(content, file_path)
    content = handle_obsidian_links(content)
    
    # Add any additional processing here
    
    return content

def find_publishable_notes():
    """Find all notes marked for publication in the Obsidian vault."""
    publishable_notes = []
    
    for root, _, files in os.walk(OBSIDIAN_ROOT):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    frontmatter, _ = extract_frontmatter(content)
                    if should_publish(frontmatter):
                        publishable_notes.append((file_path, frontmatter))
                except Exception as e:
                    log_message(f"Error processing {file_path}: {str(e)}")
    
    return publishable_notes

def publish_note(file_path, frontmatter):
    """Process and publish a single note."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        _, content_without_frontmatter = extract_frontmatter(content)
        processed_content = process_note_content(content_without_frontmatter, file_path)
        
        # Ensure frontmatter has required fields
        if "layout" not in frontmatter:
            frontmatter["layout"] = "note"
        if "date" not in frontmatter:
            frontmatter["date"] = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Create updated content with frontmatter
        updated_content = "---\n" + yaml.dump(frontmatter, sort_keys=False) + "---\n\n" + processed_content
        
        # Determine destination path and create directory if needed
        dest_path = get_destination_path(frontmatter, file_path)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        
        # Write the processed note
        with open(dest_path, "w", encoding="utf-8") as f:
            f.write(updated_content)
        
        log_message(f"Published: {os.path.basename(file_path)} -> {dest_path}")
        return True
    
    except Exception as e:
        log_message(f"Error publishing {file_path}: {str(e)}")
        return False

def main():
    """Main execution function."""
    print("\n===== Obsidian to Website Publishing Tool =====\n")
    
    # Create necessary directories
    create_directories()
    
    # Find publishable notes
    publishable_notes = find_publishable_notes()
    
    if not publishable_notes:
        print("No notes marked for publication found.")
        return
    
    # Display notes to be published
    print(f"\nFound {len(publishable_notes)} notes marked for publication:\n")
    for i, (file_path, frontmatter) in enumerate(publishable_notes, 1):
        title = frontmatter.get("title", os.path.basename(file_path))
        print(f"{i}. {title} ({file_path})")
    
    # Confirm before publishing
    confirmation = input("\nPublish these notes? (yes/no): ")
    if confirmation.lower() not in ["yes", "y"]:
        print("Publication cancelled.")
        return
    
    # Publish notes
    print("\nPublishing notes...")
    success_count = 0
    
    for file_path, frontmatter in publishable_notes:
        if publish_note(file_path, frontmatter):
            success_count += 1
    
    print(f"\nPublication complete. {success_count}/{len(publishable_notes)} notes published successfully.")

if __name__ == "__main__":
    main()
