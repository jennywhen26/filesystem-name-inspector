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
SCAN SUMMARY:
Total files scanned: 19
Total directories scanned: 8

FILE PACKAGES, total number of matching items: 8
/Users/hsujen/Desktop/Test-Driven_00/File_types/x.zip
/Users/hsujen/Desktop/Test-Driven_00/測試一/Straße.tar
/Users/hsujen/Desktop/Test-Driven_00/File_types/y.tar
/Users/hsujen/Desktop/Test-Driven_00/File_types/z.rar
/Users/hsujen/Desktop/Test-Driven_00/File_types/w.7z
/Users/hsujen/Desktop/Test-Driven_00/File_types/u.gz
/Users/hsujen/Desktop/Test-Driven_00/File_types/t.iso
/Users/hsujen/Desktop/Test-Driven_00/File_types/s.dmg

FILE NAMES, total number of matching items: 2
/Users/hsujen/Desktop/Test-Driven_00/File_names/spaceafterextension.pdf 
/Users/hsujen/Desktop/Test-Driven_00/File_names/spaceatend_noextension 

SYSTEM FILES, total number of matching items: 2
/Users/hsujen/Desktop/Test-Driven_00/.DS_Store
/Users/hsujen/Desktop/Test-Driven_00/File_names/.DS_Store

SYSTEM DIRECTORIES, total number of matching items: 1
/Users/hsujen/Desktop/Test-Driven_00/.jen

NON-ASCII CHARACTERS, total number of matching items: 7
/Users/hsujen/Desktop/Test-Driven_00/тестовые_файлы.pdf
/Users/hsujen/Desktop/Test-Driven_00/測試檔案.txt
/Users/hsujen/Desktop/Test-Driven_00/測試一/Straße.tar
/Users/hsujen/Desktop/Test-Driven_00/тестовые файлы один/Bänke
/Users/hsujen/Desktop/Test-Driven_00/Bänke Straße
/Users/hsujen/Desktop/Test-Driven_00/測試一
/Users/hsujen/Desktop/Test-Driven_00/тестовые файлы один
```
If no issues are found in a category, the script displays "Congrats! None found!"
