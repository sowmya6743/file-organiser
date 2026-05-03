# 📁 Automated File Organiser

> A Python tool that automatically watches a folder and sorts files by type, date, or size. Runs as a background service.

## 🎯 What This Project Does

This program monitors any folder on your computer and automatically organizes files:

| Sort Method | What It Does | Example |
|-------------|--------------|---------|
| **By Type** | Sorts by file extension | `.txt` → `Text_Files/`, `.jpg` → `Images/` |
| **By Date** | Sorts by last modified time | `Today/`, `This_Week/`, `Old/` |
| **By Size** | Sorts by file size | `Small_Files/`, `Medium_Files/`, `Large_Files/` |

## 🛠️ Technologies Used

- **Python 3** - Main programming language
- **watchdog** - Real-time folder monitoring
- **os / shutil** - File system operations
- **argparse** - Command-line argument parsing
- **datetime** - Date-based sorting logic

## 📂 Project Structure