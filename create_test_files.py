import os

# Your PracticeFolder path (already correct from your working code)
test_folder = r"/Users/sowmyakothakapu/Desktop/PracticeFolder"

# Create 5 test files with different extensions
test_files = [
    "notes.txt",
    "budget.txt", 
    "vacation.jpg",
    "report.pdf",
    "song.mp3"
]

for filename in test_files:
    filepath = os.path.join(test_folder, filename)
    
    # Write some content to the file
    with open(filepath, 'w') as f:
        f.write(f"This is a test file called {filename}")
    
    print(f"Created: {filename}")

print("\n✅ Test files created! Now run sorter.py")