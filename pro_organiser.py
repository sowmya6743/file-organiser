#!/usr/bin/env python3
"""
PROFESSIONAL FILE ORGANISER
A background service that automatically sorts files by type, date, or size.
Author: Your Name
Created: 2025
"""

import os
import shutil
import time
import argparse
import sys
import json
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ============================================
# CONFIGURATION (Default settings)
# ============================================

DEFAULT_SETTINGS = {
    "watch_folder": os.path.expanduser("~/Desktop/PracticeFolder"),
    "sort_by": "type",  # type, date, or size
    "run_in_background": False,
    "log_file": "organiser_log.txt"
}

# ============================================
# LOGGING SYSTEM (Saves history of what happened)
# ============================================

def log_message(message, log_file="organiser_log.txt"):
    """
    Writes a message to both the terminal AND a log file
    Think of this as a diary that records everything the program does
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"[{timestamp}] {message}"
    
    # Print to terminal
    print(full_message)
    
    # Also save to file
    with open(log_file, "a") as f:
        f.write(full_message + "\n")

# ============================================
# THE SORTING LOGIC (Reused from Day 3)
# ============================================

def get_type_category(filename):
    """Sort by file extension"""
    extension = os.path.splitext(filename)[1].lower()
    
    type_mappings = {
        ".txt": "Text_Files",
        ".jpg": "Images", ".jpeg": "Images", ".png": "Images", ".gif": "Images",
        ".pdf": "Documents", ".doc": "Documents", ".docx": "Documents",
        ".mp3": "Music", ".wav": "Music",
        ".mp4": "Videos", ".mov": "Videos",
        ".zip": "Archives", ".rar": "Archives"
    }
    
    return type_mappings.get(extension, "Other")

def get_date_category(file_path):
    """Sort by age: Today, This Week, or Old"""
    file_timestamp = os.path.getmtime(file_path)
    now = time.time()
    seconds_in_day = 24 * 60 * 60
    
    age_seconds = now - file_timestamp
    
    if age_seconds < seconds_in_day:
        return "Today"
    elif age_seconds < (7 * seconds_in_day):
        return "This_Week"
    else:
        return "Old"

def get_size_category(file_path):
    """Sort by size: Small, Medium, Large"""
    size_bytes = os.path.getsize(file_path)
    size_mb = size_bytes / (1024 * 1024)
    
    if size_mb < 1:
        return "Small_Files"
    elif size_mb < 10:
        return "Medium_Files"
    else:
        return "Large_Files"

def get_category(file_path, filename, sort_by):
    """Route to the correct sorting function based on user's choice"""
    if sort_by == "type":
        return get_type_category(filename)
    elif sort_by == "date":
        return get_date_category(file_path)
    elif sort_by == "size":
        return get_size_category(file_path)
    else:
        return "Unsorted"

def organize_single_file(file_path, watch_folder, sort_by, log_file):
    """Move a single file to its appropriate category folder"""
    filename = os.path.basename(file_path)
    
    # Skip folders and system files
    if os.path.isdir(file_path) or filename == ".DS_Store":
        return
    
    # Determine where the file should go
    category = get_category(file_path, filename, sort_by)
    
    # Create destination folder
    dest_folder = os.path.join(watch_folder, category)
    os.makedirs(dest_folder, exist_ok=True)
    
    # Move the file
    new_path = os.path.join(dest_folder, filename)
    
    # Small delay to ensure file is fully written
    time.sleep(0.5)
    
    try:
        shutil.move(file_path, new_path)
        log_message(f"AUTO-MOVED: {filename} → {category}/", log_file)
    except Exception as e:
        log_message(f"ERROR moving {filename}: {e}", log_file)

# ============================================
# WATCHDOG EVENT HANDLER (From Day 4)
# ============================================

class FileOrganiserHandler(FileSystemEventHandler):
    def __init__(self, watch_folder, sort_by, log_file):
        self.watch_folder = watch_folder
        self.sort_by = sort_by
        self.log_file = log_file
    
    def on_created(self, event):
        if not event.is_directory:
            log_message(f"NEW FILE DETECTED: {os.path.basename(event.src_path)}", self.log_file)
            organize_single_file(event.src_path, self.watch_folder, self.sort_by, self.log_file)

# ============================================
# COMMAND LINE ARGUMENTS (NEW for Day 5!)
# ============================================

def parse_arguments():
    """
    Reads what the user typed in the terminal and converts it to settings
    Example: python pro_organiser.py --folder ~/Downloads --sort-by date
    """
    parser = argparse.ArgumentParser(
        description="Professional File Organiser - Automatically sorts files in a folder",
        epilog="Examples:\n"
               "  python pro_organiser.py --folder ~/Downloads\n"
               "  python pro_organiser.py --sort-by date\n"
               "  python pro_organiser.py --help"
    )
    
    parser.add_argument(
        "--folder", "-f",
        type=str,
        default=DEFAULT_SETTINGS["watch_folder"],
        help="Folder to watch (default: ~/Desktop/PracticeFolder)"
    )
    
    parser.add_argument(
        "--sort-by", "-s",
        choices=["type", "date", "size"],
        default=DEFAULT_SETTINGS["sort_by"],
        help="How to sort files: by type, date, or size (default: type)"
    )
    
    parser.add_argument(
        "--background", "-b",
        action="store_true",
        help="Run in background mode (no terminal output, just log file)"
    )
    
    parser.add_argument(
        "--log-file", "-l",
        type=str,
        default=DEFAULT_SETTINGS["log_file"],
        help="File to save activity log (default: organiser_log.txt)"
    )
    
    parser.add_argument(
        "--once", "-o",
        action="store_true",
        help="Run once (organize existing files) then exit (don't watch continuously)"
    )
    
    return parser.parse_args()

# ============================================
# ORGANIZE EXISTING FILES (Run once mode)
# ============================================

def organize_existing_files(watch_folder, sort_by, log_file):
    """
    Organizes all files currently in the folder (doesn't watch for new ones)
    Useful for cleaning up a messy folder
    """
    log_message(f"SCANNING: {watch_folder}", log_file)
    log_message(f"SORTING BY: {sort_by}", log_file)
    
    files_moved = 0
    
    for item in os.listdir(watch_folder):
        old_path = os.path.join(watch_folder, item)
        
        if os.path.isdir(old_path):
            continue
        
        if item == ".DS_Store":
            continue
        
        category = get_category(old_path, item, sort_by)
        dest_folder = os.path.join(watch_folder, category)
        os.makedirs(dest_folder, exist_ok=True)
        
        new_path = os.path.join(dest_folder, item)
        
        try:
            shutil.move(old_path, new_path)
            log_message(f"MOVED: {item} → {category}/", log_file)
            files_moved += 1
        except Exception as e:
            log_message(f"ERROR: Could not move {item} - {e}", log_file)
    
    log_message(f"COMPLETE: Moved {files_moved} files", log_file)
    return files_moved

# ============================================
# MAIN WATCHER FUNCTION
# ============================================

def start_watching(watch_folder, sort_by, log_file, background_mode=False):
    """
    Starts the background watcher that monitors for new files
    """
    # Expand ~ to full path (e.g., ~/Desktop becomes /Users/name/Desktop)
    watch_folder = os.path.expanduser(watch_folder)
    
    # Check if folder exists
    if not os.path.exists(watch_folder):
        log_message(f"ERROR: Folder not found: {watch_folder}", log_file)
        log_message("Please create the folder or use --folder to specify a different one", log_file)
        return False
    
    # Create event handler and observer
    event_handler = FileOrganiserHandler(watch_folder, sort_by, log_file)
    observer = Observer()
    observer.schedule(event_handler, watch_folder, recursive=False)
    observer.start()
    
    # Display startup message
    log_message("="*50, log_file)
    log_message("🤖 PROFESSIONAL FILE ORGANISER STARTED", log_file)
    log_message(f"📁 WATCHING: {watch_folder}", log_file)
    log_message(f"📊 SORTING BY: {sort_by}", log_file)
    log_message(f"📝 LOG FILE: {log_file}", log_file)
    log_message("🛑 Press Ctrl+C to stop", log_file)
    log_message("="*50, log_file)
    
    if background_mode:
        print(f"Running in background mode. Check {log_file} for activity.")
    
    try:
        # Keep running until interrupted
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        log_message("\n🛑 Stopping the observer...", log_file)
        observer.stop()
        log_message("✅ Program stopped. Goodbye!", log_file)
    
    observer.join()
    return True

# ============================================
# ENTRY POINT - Where the program starts
# ============================================

def main():
    """
    Main function - runs when you execute the script
    """
    # Read command line arguments
    args = parse_arguments()
    
    # If --once flag is used, organize existing files and exit
    if args.once:
        print(f"\n📂 Organizing existing files in: {args.folder}")
        print(f"📊 Sorting by: {args.sort_by}")
        print("-"*40)
        
        files_moved = organize_existing_files(args.folder, args.sort_by, args.log_file)
        
        print("-"*40)
        print(f"✅ Done! Moved {files_moved} files.")
        print(f"📝 Check {args.log_file} for details.")
        return
    
    # Otherwise, start the continuous watcher
    start_watching(args.folder, args.sort_by, args.log_file, args.background)

# This ensures the code only runs when you execute the script directly
# (not when you import it as a module)
if __name__ == "__main__":
    main()