#!/usr/bin/env python3
"""
Obsidian to Website Publishing Script

This script:
1. Traverses the Obsidian vault to find notes marked for publication
2. Processes them for Jekyll compatibility
3. Copies them to the website repository
4. Handles images and attachments
5. Downsizes images to reduce file size
6. Implements safety features to prevent accidental publication

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
import subprocess

# Try to import PIL for image processing
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("PIL not found. Installing Pillow...")
    subprocess.call([sys.executable, "-m", "pip", "install", "Pillow"])
    try:
        from PIL import Image
        PIL_AVAILABLE = True
        print("Pillow installed successfully!")
    except ImportError:
        print("Error: Failed to install Pillow. Images will be copied without resizing.")
        PIL_AVAILABLE = False

# Configuration
OBSIDIAN_ROOT = "/Users/kshitijaggarwal/Documents/Notes/FRBs"
WEBSITE_ROOT = "/Users/kshitijaggarwal/Documents/Personal/Website/kshitijaggarwal.github.io"
NOTES_DIR = os.path.join(WEBSITE_ROOT, "_notes")
IMAGES_DIR = os.path.join(WEBSITE_ROOT, "images")
LOG_FILE = os.path.join(WEBSITE_ROOT, "scripts", "publish_log.txt")

# Image processing settings
MAX_IMAGE_WIDTH = 1200  # Maximum width in pixels
MAX_IMAGE_HEIGHT = 1200  # Maximum height in pixels
JPEG_QUALITY = 80  # JPEG compression quality (0-100)
PNG_COMPRESSION = 9  # PNG compression level (0-9)
TARGET_MAX_SIZE_KB = 300  # Target maximum file size in KB

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

def downsize_image(source_path, destination_path):
    """Downsample an image to reduce file size while maintaining quality."""
    if not PIL_AVAILABLE:
        # If PIL is not available, just copy the image
        shutil.copy2(source_path, destination_path)
        return destination_path
    
    try:
        # Check if the file is an image
        if not source_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            shutil.copy2(source_path, destination_path)
            return destination_path
        
        # Get the original file size in KB
        original_size_kb = os.path.getsize(source_path) / 1024
        
        # If file is already smaller than target, just copy it
        if original_size_kb <= TARGET_MAX_SIZE_KB:
            shutil.copy2(source_path, destination_path)
            log_message(f"Image already small enough ({original_size_kb:.1f}KB): {os.path.basename(source_path)}")
            return destination_path
            
        # Open the image
        with Image.open(source_path) as img:
            # Get original dimensions
            width, height = img.size
            
            # Calculate scale factor if image is larger than max dimensions
            scale = 1.0
            if width > MAX_IMAGE_WIDTH or height > MAX_IMAGE_HEIGHT:
                width_scale = MAX_IMAGE_WIDTH / width if width > MAX_IMAGE_WIDTH else 1.0
                height_scale = MAX_IMAGE_HEIGHT / height if height > MAX_IMAGE_HEIGHT else 1.0
                scale = min(width_scale, height_scale)
                
                # Calculate new dimensions
                new_width = int(width * scale)
                new_height = int(height * scale)
                
                # Resize the image
                img = img.resize((new_width, new_height), Image.LANCZOS)
            
            # Save with appropriate settings based on format
            if source_path.lower().endswith('.jpg') or source_path.lower().endswith('.jpeg'):
                img.save(destination_path, 'JPEG', quality=JPEG_QUALITY, optimize=True)
            elif source_path.lower().endswith('.png'):
                img.save(destination_path, 'PNG', optimize=True, compress_level=PNG_COMPRESSION)
            else:
                # For other formats, just save normally
                img.save(destination_path)
        
        # Get the new file size
        new_size_kb = os.path.getsize(destination_path) / 1024
        size_reduction = (1 - (new_size_kb / original_size_kb)) * 100
        
        log_message(f"Image optimized: {os.path.basename(source_path)} - {original_size_kb:.1f}KB → {new_size_kb:.1f}KB ({size_reduction:.1f}% reduction)")
        return destination_path
        
    except Exception as e:
        log_message(f"Error downsizing image {source_path}: {str(e)}")
        # Fallback to simple copy if optimization fails
        shutil.copy2(source_path, destination_path)
        return destination_path

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
            
            # Copy and optimize the image to the website images directory
            destination = os.path.join(IMAGES_DIR, new_image_name)
            downsize_image(image_path, destination)
            
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

def optimize_existing_images():
    """Optimize existing images in the website's images directory."""
    if not PIL_AVAILABLE:
        print("PIL not available. Skipping optimization of existing images.")
        return

    print("\nChecking for large images to optimize...")
    optimized_count = 0
    skipped_count = 0
    failed_count = 0
    
    for file in os.listdir(IMAGES_DIR):
        file_path = os.path.join(IMAGES_DIR, file)
        if not os.path.isfile(file_path):
            continue
            
        if not file.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue
            
        file_size_kb = os.path.getsize(file_path) / 1024
        if file_size_kb > TARGET_MAX_SIZE_KB:
            print(f"Optimizing: {file} ({file_size_kb:.1f}KB)")
            
            # Create a temporary path for the optimized image
            temp_path = file_path + ".temp"
            
            try:
                # Optimize the image
                downsize_image(file_path, temp_path)
                
                # Replace the original with the optimized version
                os.replace(temp_path, file_path)
                
                # Get the new file size
                new_size_kb = os.path.getsize(file_path) / 1024
                size_reduction = (1 - (new_size_kb / file_size_kb)) * 100
                
                print(f"  → Optimized to {new_size_kb:.1f}KB ({size_reduction:.1f}% reduction)")
                optimized_count += 1
                
            except Exception as e:
                print(f"  → Failed to optimize: {str(e)}")
                failed_count += 1
                # Remove the temporary file if it exists
                if os.path.exists(temp_path):
                    os.remove(temp_path)
        else:
            skipped_count += 1
    
    print(f"\nImage optimization complete: {optimized_count} optimized, {skipped_count} already small enough, {failed_count} failed")

def main():
    """Main execution function."""
    print("\n===== Obsidian to Website Publishing Tool =====\n")
    
    # Check if PIL is available
    if PIL_AVAILABLE:
        print("Image optimization is enabled.")
    else:
        print("Warning: PIL (Pillow) is not available. Images will not be optimized.")
    
    # Create necessary directories
    create_directories()
    
    # Check for command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--optimize-images-only":
        optimize_existing_images()
        return
    
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
    
    # Ask if user wants to optimize existing images
    optimize_confirmation = input("\nWould you like to optimize existing images in the website? (yes/no): ")
    if optimize_confirmation.lower() in ["yes", "y"]:
        optimize_existing_images()

if __name__ == "__main__":
    main()
