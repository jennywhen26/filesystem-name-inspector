from pathlib import Path
import argparse
import re

'''
version 0.2.1
last updated: 05/21/2025
developed by Jenny Hsu
'''

# ANSI color codes
RED = '\033[91m'
# GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
RESET = '\033[0m'  # Reset to default color

# Initialize argument parser
parser = argparse.ArgumentParser(
    description="Filesystem Name Inspector: Scans directories to identify problematic files and naming issues that could cause compatibility problems.",
    formatter_class=argparse.RawDescriptionHelpFormatter,  # Preserves formatting in description and epilog
    usage="python3 fs-name-inspector_v0-2-1.py /path/to/directory [optional flags]",  # Custom usage line
    epilog="""
    Examples:
      python3 fs-name-inspector_v0-2-1.py /path/to/directory
      python3 fs-name-inspector_v0-2-1.py /path/to/directory --csv results.csv

    Version: 0.2.1
    Last updated: 05/21/2025
    Developed by: Jenny Hsu
    License: MIT
    """
)

# Add the required directory argument and an optional CSV flag
parser.add_argument('directory', type=Path, help="Path to the directory you want to scan")
parser.add_argument('--csv', metavar='FILE', type=str,
                    help="Export results to a CSV file at the specified path")

# Parse arguments
args = parser.parse_args()

# Check if directory was provided
if args.directory is None:
    print(f"{CYAN}Filesystem Name Inspector v0.2.1{RESET}")
    print(f"{CYAN}Usage: python3 fs-name-inspector_v0-2-1.py /path/to/directory [optional flags]{RESET}")
    print(f"{CYAN}For more information, run: python3 fs-name-inspector_v0-2-1.py --help{RESET}")
    exit(1)

# Specify the file types to look for
problematic_file_packages = [".zip", ".tar", ".rar", ".7z", ".s7z", ".apk", ".zipx", ".wim", ".gz", ".iso", ".dmg",".app",
                          ".warc", ".warcz", ".war", ".jar", ".ewf", ".e01", ".dd",".raw", ".01", ".001", ".1", ".gzip",
                          ".img", ".aff", ".nrg", ".bin", ".sit", ".sitx", ".tgz", ".tlz", ".txz", ".zz", ".ecc", ".dar",
                          ".ima", ".deb", ".pkg", ".mpkg", ".rpm", ".msi", ".crx"]

# Regular expressions specifications
problem_file_names = r"[/\\:]"  # Matches forward slash, backslash, and colon
dir_space_pattern = r"^\s+|\s+$"  # Matches spaces at start OR end of directory names
file_trailing_space = r"\s+$"  # Matches any trailing spaces at the end
non_english_pattern = r'[^\x00-\x7F]'  # Matches any non-ASCII character

# Initialize lists to hold results
problem_packages = []
problem_filenames = []
problem_dirnames = []
problem_system_files = []
problem_system_dirs = []
non_ascii = []

# Initialize counters for total files and directories
total_files = 0
total_directories = 0

# First, count all files and directories
print("Scanning directory structure... This may take a while for large directories.")
for item in args.directory.rglob('*'):
    if item.is_file():
        total_files += 1
    elif item.is_dir():
        total_directories += 1

# Search for file packages
print("Checking for file packages...")
for file_type in problematic_file_packages:
    # Look for extension strings at the end of a filename
    # Escape the dot (in regex module, "." can match any character),
    # "\." will match the period literally, extra "\" is to escape Python syntax.
    pattern = file_type.replace(".", "\\.") + "$"
    for item in args.directory.rglob('*'):
        if item.is_file() and re.search(pattern, item.name, re.IGNORECASE):
            problem_packages.append(item)

# Search for problematic file names
for item in args.directory.rglob('*'):
    # Skip directories in this loop
    if item.is_dir():
        continue

    # Check for problematic characters (/, \, :)
    if re.search(problem_file_names, item.name):
        problem_filenames.append(item)

    # Check for trailing spaces in ALL files
    if re.search(file_trailing_space, item.name):
        problem_filenames.append(item)

    # Check for non-English characters in file names
    if re.search(non_english_pattern, item.name):
        non_ascii.append(item)

    # Check for system files (starting with . or Thumbs.db)
    if item.name.startswith('.') or item.name == 'Thumbs.db':
        problem_system_files.append(item)

# Search for problematic directory names
for item in args.directory.rglob('*'):
    # Only check directories
    if not item.is_dir():
        continue

    # # Check for spaces at beginning OR end of directory name
    # if re.search(dir_space_pattern, item.name):
    #     problem_dirnames.append(item)
    # commented out as we no longer need this search,
    # since we create our own bag names when bagging, spaces won't be problem

    # Check for non-English characters in directory names
    if re.search(non_english_pattern, item.name):
        non_ascii.append(item)

    # Check for system directories (starting with .)
    if item.name.startswith('.'):
        problem_system_dirs.append(item)

# Export to a CSV feature with --csv [path to destination folder]
if args.csv:
    try:
        import csv

        with open(args.csv, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)

            # Write scan summary
            csvwriter.writerow(['SCAN SUMMARY', ''])
            csvwriter.writerow(['Total files scanned', total_files])
            csvwriter.writerow(['Total directories scanned', total_directories])
            csvwriter.writerow(['', ''])  # Empty row as separator

            # Write FILE PACKAGES section
            csvwriter.writerow(['FILE PACKAGES: total number of matching items:', len(problem_packages)])
            if problem_packages:
                for item in problem_packages:
                    csvwriter.writerow([str(item.absolute()), ''])
            else:
                csvwriter.writerow(['Congrats! None found.', ''])
            csvwriter.writerow(['', ''])  # Empty row as separator

            # Write FILE NAMES section
            csvwriter.writerow(['FILE NAMES: total number of matching items:', len(problem_filenames)])
            if problem_filenames:
                for item in problem_filenames:
                    csvwriter.writerow([str(item.absolute()), ''])
            else:
                csvwriter.writerow(['Congrats! None found.', ''])
            csvwriter.writerow(['', ''])  # Empty row as separator

            # Write SYSTEM FILES section
            csvwriter.writerow(['SYSTEM FILES: total number of matching items:', len(problem_system_files)])
            if problem_system_files:
                for item in problem_system_files:
                    csvwriter.writerow([str(item.absolute()), ''])
            else:
                csvwriter.writerow(['Congrats! None found.', ''])
            csvwriter.writerow(['', ''])  # Empty row as separator

            # Write SYSTEM DIRECTORIES section
            csvwriter.writerow(['SYSTEM DIRECTORIES: total number of matching items:', len(problem_system_dirs)])
            if problem_system_dirs:
                for item in problem_system_dirs:
                    csvwriter.writerow([str(item.absolute()), ''])
            else:
                csvwriter.writerow(['Congrats! None found.', ''])
            csvwriter.writerow(['', ''])  # Empty row as separator

            # Write NON-ASCII CHARACTERS section
            csvwriter.writerow(['NON-ASCII CHARACTERS: total number of matching items:', len(non_ascii)])
            if non_ascii:
                for item in non_ascii:
                    csvwriter.writerow([str(item.absolute()), ''])
            else:
                csvwriter.writerow(['Congrats! None found.', ''])

            print(f"\n{YELLOW}Results exported to {args.csv}{RESET}")
    except Exception as e:
        print(f"\n{RED}Error exporting to CSV: {e}{RESET}")


# Print summary of total files and directories scanned
print(f"\n{CYAN}SCAN SUMMARY:{RESET}")
print(f"Total directories scanned: {total_directories}")
print(f"Total files scanned: {total_files}")

# Print results with absolute paths
print(f"\n{MAGENTA}FILE PACKAGES, total number of matching items: {len(problem_packages)}{RESET}")
if problem_packages:
    for item in problem_packages:
        print(item.absolute())
else:
    print(f"{YELLOW}Congrats! None found.{RESET}")

print(f"\n{MAGENTA}FILE NAMES, total number of matching items: {len(problem_filenames)}{RESET}")
if problem_filenames:
    for item in problem_filenames:
        print(item.absolute())
else:
    print(f"{YELLOW}Congrats! None found.{RESET}")

# print(f"\nTotal number of problematic directories: {len(problem_dirnames)}")
# if problem_dirnames:
#     for item in problem_dirnames:
#         print(item.absolute())
# else:
#     print(f"{YELLOW}Congrats! None found.{RESET}")

print(f"\n{MAGENTA}SYSTEM FILES, total number of matching items: {len(problem_system_files)}{RESET}")
if problem_system_files:
    for item in problem_system_files:
        print(item.absolute())
else:
    print(f"{YELLOW}Congrats! None found.{RESET}")

print(f"\n{MAGENTA}SYSTEM DIRECTORIES, total number of matching items: {len(problem_system_dirs)}{RESET}")
if problem_system_dirs:
    for item in problem_system_dirs:
        print(item.absolute())
else:
    print(f"{YELLOW}Congrats! None found.{RESET}")

print(f"\n{MAGENTA}NON-ASCII CHARACTERS, total number of matching items: {len(non_ascii)}{RESET}")
if non_ascii:
    for item in non_ascii:
        print(item.absolute())
else:
    print(f"{YELLOW}Congrats! None found.{RESET}")