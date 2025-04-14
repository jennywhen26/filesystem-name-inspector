# filesystem-name-inspector Documentation

## Summary
A Python script that scans directories to identify file packages, problematic file and directory names, including non-ASCII characters, system files, trailing spaces, and other naming issues that could cause compatibility problems when transferring. The script will search the directories and files recursively, and give results when it’s done with absolute paths to help users locate the exact directory or file.

## Installation and Dependencies
### Requirements
- Python 3.6 or higher
- No external package dependencies required
### Python Libraries Used
- _pathlib.Path_: For cross-platform file path handling
- _argparse_: For command-line argument parsing
- _re_: For regular expression pattern matching

## What is the script searching for?
- Identifies compressed/package files that may cause transfer issues
- Detects problematic characters in filenames (/, , :)
- Flags files with trailing spaces
- Identifies hidden system files and directories
- Detects non-ASCII characters in both file and directory names
- Displays clear, categorized results with absolute paths

### The script is searching recursively in the directory structure for several things:
1. File packages, as these could become problems when transferring or ingesting. File packages identified are as listed:
.zip, .tar, .rar, .7z, .s7z, .apk, .zipx, .wim, .gz, .iso, .dmg, .app, .warc, .warcz, .war, .jar, .ewf, .e01, .dd, .raw, .01, .001, .1, .gzip, .img, .aff, .nrg, .bin, .sit, .sitx, .tgz, .tlz, .txz, .zz, .ecc, .dar, .ima, .deb, .pkg, .mpkg, .rpm, .msi, .crx
2. File names with trailing spaces
3. Hidden system files, like Thumbs.db or anything that starts with “.”
4. Both file and directory names with non-ASCII characters

## How to use?

### On macOS/Linux
```python3 filesystem-name-inspector.py /path/to/directory```

### On Windows
```python filesystem-name-inspector.py C:\path\to\directory```

### Example Output
```
Total number of matching problematic file types: 3
/home/user/data/archive.zip
/home/user/data/backup.tar.gz
/home/user/data/image.iso

Total number of problematic file names: 2
/home/user/data/report.pdf 
/home/user/data/document:v1.txt

Total number of problematic directories: 1
/home/user/data/presentations 

Total number of problematic system files: 2
/home/user/data/.DS_Store
/home/user/data/Thumbs.db

Total number of problematic system directories: 1
/home/user/data/.git

Total number of items with non-ASCII characters: 2
/home/user/data/résumé.pdf
/home/user/data/документы
```
If no issues are found in a category, the script displays "Congrats! None found!"
