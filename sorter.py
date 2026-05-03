import os
import shutil
import time
import datetime

print("=== SMART FILE ORGANISER ===")
print("I can sort by: type, date, OR size")

# ============================================
# CONFIGURATION - CHANGE THIS TO CONTROL SORTING
# ============================================
SORT_BY = "date"  # OPTIONS: "type", "date", or "size"

# UPDATE THIS PATH WITH YOUR USERNAME!
practice_folder = r"/Users/sowmyakothakapu/Desktop/PracticeFolder"
# For Mac users, use this format instead (uncomment and modify):
# practice_folder = r"/Users/YourName/Desktop/PracticeFolder"

# ============================================
# FUNCTION 1: Sort by FILE TYPE (.txt, .jpg, etc.)
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
    
    # If the extension is in our mapping, return the folder name
    # Otherwise, put it in "Other"
    if extension in type_mappings:
        return type_mappings[extension]
    else:
        return "Other"

# ============================================
# FUNCTION 2: Sort by DATE (Today, This Week, Old)
# ============================================
def get_date_category(file_path):
    """Determines if a file is from Today, This Week, or Old"""
    
    # Get the file's last modification time (as a computer number)
    file_timestamp = os.path.getmtime(file_path)
    
    # Get the current time (as a computer number)
    now = time.time()
    
    # Calculate how many seconds are in one day
    seconds_in_day = 24 * 60 * 60  # 24 hours × 60 minutes × 60 seconds = 86,400
    
    # Calculate the file's age in seconds
    age_in_seconds = now - file_timestamp
    
    # Is the file from today? (less than 24 hours old)
    if age_in_seconds < seconds_in_day:
        return "Today"
    # Is the file from this week? (between 1 and 7 days old)
    elif age_in_seconds < (7 * seconds_in_day):
        return "This_Week"
    # Otherwise it's older than 7 days
    else:
        return "Old"

# ============================================
# FUNCTION 3: Sort by SIZE (Small, Medium, Large)
# ============================================
def get_size_category(file_path):
    """Categorizes files by size: Small (<1 MB), Medium (1-10 MB), Large (>10 MB)"""
    
    # Get file size in bytes
    size_bytes = os.path.getsize(file_path)
    
    # Convert to megabytes (1 MB = 1,048,576 bytes)
    size_mb = size_bytes / (1024 * 1024)
    
    # Categorize by size in MB
    if size_mb < 1:
        return "Small_Files"
    elif size_mb < 10:
        return "Medium_Files"
    else:
        return "Large_Files"

# ============================================
# MAIN FUNCTION - This does the actual organizing
# ============================================
def organize_files():
    """Main function that looks at all files and moves them to the right folders"""
    
    print("\n" + "="*50)
    print(f"SORTING BY: {SORT_BY.upper()}")
    print(f"WATCHING FOLDER: {practice_folder}")
    print("="*50 + "\n")
    
    # Check if the folder exists
    if not os.path.exists(practice_folder):
        print(f"ERROR: Cannot find folder '{practice_folder}'")
        print("Please update the 'practice_folder' path with your correct username!")
        return
    
    # Get all items in the practice folder
    all_items = os.listdir(practice_folder)
    
    # Keep track of how many files we move
    files_moved = 0
    files_skipped = 0
    
    # Look at each item one by one
    for item in all_items:
        # Build the full path (folder location + item name)
        old_path = os.path.join(practice_folder, item)
        
        # Skip folders - we only want to move individual files
        if os.path.isdir(old_path):
            print(f"📁 SKIPPING FOLDER: {item}")
            continue
        
        # --- DECIDE WHERE THIS FILE SHOULD GO ---
        if SORT_BY == "type":
            category = get_type_category(item)
        elif SORT_BY == "date":
            category = get_date_category(old_path)
        elif SORT_BY == "size":
            category = get_size_category(old_path)
        else:
            print(f"⚠️ WARNING: Unknown SORT_BY value '{SORT_BY}'")
            print("   Please use 'type', 'date', or 'size'")
            return
        
        # Create the destination folder if it doesn't exist
        # exist_ok=True means "don't crash if the folder already exists"
        destination_folder = os.path.join(practice_folder, category)
        os.makedirs(destination_folder, exist_ok=True)
        
        # Build the new path (where the file will go after moving)
        new_path = os.path.join(destination_folder, item)
        
        # MOVE THE FILE!
        shutil.move(old_path, new_path)
        
        # Show what happened (formatted nicely)
        print(f"📄 MOVED: {item:<25} → {category}/")
        files_moved = files_moved + 1
    
    # Print summary
    print("\n" + "="*50)
    print(f"✅ ORGANIZATION COMPLETE!")
    print(f"   📄 Files moved: {files_moved}")
    print(f"   📁 Folders created: (see above)")
    print("="*50)

# ============================================
# RUN THE PROGRAM
# ============================================
organize_files()