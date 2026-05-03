import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

print("="*50)
print("🤖 AUTOMATIC FILE ORGANISER")
print("="*50)
print("This program will watch a folder and automatically")
print("organize new files as they appear.")
print("Press Ctrl+C to stop.\n")

# ============================================
# CONFIGURATION - UPDATE THIS PATH!
# ============================================

# CHANGE THIS to the folder you want to watch
# For now, let's keep using your PracticeFolder
WATCH_FOLDER = r"/Users/sowmyakothakapu/Desktop/PracticeFolder"

# For Windows users (uncomment and modify):
# WATCH_FOLDER = r"C:\Users\YourName\Desktop\PracticeFolder"

# ============================================
# REUSE OUR SORTING LOGIC FROM DAY 3
# ============================================

def get_type_category(filename):
    """Determines where a file should go based on its extension"""
    extension = os.path.splitext(filename)[1].lower()
    
    type_mappings = {
        ".txt": "Text_Files",
        ".jpg": "Images",
        ".png": "Images",
        ".jpeg": "Images",
        ".gif": "Images",
        ".pdf": "Documents",
        ".doc": "Documents",
        ".docx": "Documents",
        ".mp3": "Music",
        ".wav": "Music",
        ".mp4": "Videos",
        ".mov": "Videos",
        ".zip": "Archives",
        ".rar": "Archives"
    }
    
    if extension in type_mappings:
        return type_mappings[extension]
    else:
        return "Other"

def organize_single_file(file_path):
    """
    Organize a single file - this will be called automatically
    whenever a new file appears
    """
    # Get just the filename from the full path
    filename = os.path.basename(file_path)
    
    # Skip folders
    if os.path.isdir(file_path):
        return
    
    # Skip Mac system files
    if filename == ".DS_Store":
        return
    
    # Determine category based on file type
    category = get_type_category(filename)
    
    # Create destination folder if needed
    destination_folder = os.path.join(WATCH_FOLDER, category)
    os.makedirs(destination_folder, exist_ok=True)
    
    # Move the file
    new_path = os.path.join(destination_folder, filename)
    
    # Small delay to ensure file is completely written
    # (Sometimes programs are still saving when watchdog triggers)
    time.sleep(0.5)
    
    try:
        shutil.move(file_path, new_path)
        print(f"✅ AUTO-MOVED: {filename} → {category}/")
    except Exception as e:
        print(f"❌ ERROR moving {filename}: {e}")

# ============================================
# THE WATCHDOG EVENT HANDLER
# ============================================

class FileOrganiserHandler(FileSystemEventHandler):
    """
    This class defines what happens when files are created/modified
    """
    
    def on_created(self, event):
        """
        This runs when a NEW file is created in the watched folder
        """
        # Check if it's a file (not a folder)
        if not event.is_directory:
            print(f"\n🔔 NEW FILE DETECTED: {os.path.basename(event.src_path)}")
            organize_single_file(event.src_path)
    
    def on_modified(self, event):
        """
        This runs when a file is MODIFIED (changed)
        We'll ignore modifications to avoid moving files repeatedly
        """
        pass  # We don't need to do anything on modification

# ============================================
# START THE WATCHER
# ============================================

def start_watching():
    """Starts the background watcher"""
    
    # Check if the folder exists
    if not os.path.exists(WATCH_FOLDER):
        print(f"❌ ERROR: Folder not found: {WATCH_FOLDER}")
        print("Please update the WATCH_FOLDER path with your correct username!")
        return
    
    # Create the event handler
    event_handler = FileOrganiserHandler()
    
    # Create the observer
    observer = Observer()
    
    # Schedule the observer to watch the folder
    observer.schedule(event_handler, WATCH_FOLDER, recursive=False)
    
    # Start the observer (this runs in the background)
    observer.start()
    
    print(f"👁️  WATCHING FOLDER: {WATCH_FOLDER}")
    print("📋 The program is now running in the background.")
    print("💡 Try creating a new text file in the watched folder...")
    print("🛑 Press Ctrl+C to stop the program.\n")
    
    try:
        # Keep the program running
        while True:
            time.sleep(1)  # Sleep for 1 second, then check again
    except KeyboardInterrupt:
        # This happens when you press Ctrl+C
        print("\n\n🛑 Stopping the observer...")
        observer.stop()
        print("✅ Program stopped. Goodbye!")
    
    # Wait for the observer to fully stop
    observer.join()

# ============================================
# RUN THE PROGRAM
# ============================================
if __name__ == "__main__":
    start_watching()