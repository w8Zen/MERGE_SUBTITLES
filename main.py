# Project: COURSE_SUBTITLES_MERGER
# Main Script: main.py
# Description: Merges subtitles from multiple sections of a course into one text file.
# Author: w8Zen
# Date: 17/08/2025
# Version: 1.0
#
# Scope:
#   This script recursively scans a course folder containing multiple sections,
#   each with subtitle files (.srt). It cleans and merges all subtitles into one file.
#   according to the course structure, ensuring that the output is well-organized and readable.
#
# Usage:
#   1. Set BASE_FOLDER to the root directory of your course.
#
#     Example:
#           BASE_FOLDER = r"D:\Training\Python-with-Gandalf.the.Gray"
#
#     Where the folder structure should look like this:
#
#           Python-with-Gandalf.the.Gray/
#           ├── 1. Introduction/
#           │   ├── 1. Getting Started.mp4
#           │   ├── 1. Getting Started.srt
#           │   ├── 1.1 Getting Started.html
#           │   ├── 2. Basic Concepts.mp4
#           │   ├── 2. Basic Concepts.srt
#           │   └── 2.1 Basic Concepts.html
#           ├── 2. Advanced Topics/
#           │   ├── 1. Object-Oriented Programming.mp4
#           │   ├── 1. Object-Oriented Programming.srt
#           │   ├── 1.1 Object-Oriented Programming.html
#           │   ├── 2. Functional Programming.mp4
#           │   ├── 2. Functional Programming.srt
#           │   └── 2.1 Functional Programming.html
#           ├── 3. Conclusion/
#           │   ├── 1. Developers path.mp4
#           │   └── 1. Developers path.str
#           └── 4. Bonus Content/
#               ├── 1. Bonus Topic.mp4
#               └── 1. Bonus Topic.str
#
#   2. Run the script: python main.py
#   3. Output will be saved as MERGED_SUBTITLES.txt
#


import os
import re

BASE_FOLDER = r"YOUR_COURSE_PATH"  # Set your course folder path here
OUTPUT_FILE = r"MERGED_SUBTITLES.txt"


def sort_content(folder_content: str) -> list[str]:
    """
    Returns a naturally sorted list of subdirectories in the given base directory.

    Parameters:
        base_dir (str): Path to the base folder.

    Returns:
        list[str]: Sorted list of subdirectory names.
    """

    try:
        return sorted(
            os.listdir(folder_content),
            key=lambda x: [int(part) if part.isdigit() else part.lower()
                           for part in re.split(r'(\d+)', x)]
        )
    except FileNotFoundError:
        print(f"ERROR: Directory '{folder_content}' not found.")
    except Exception as e:
        print(f"ERROR: Unexpected error while listing subdirectories - {e}")
    return []


def build_section_paths(base_dir: str, sections: list[str]) -> list[str]:
    """
    Constructs full paths for each section (subdirectory).

    Parameters:
        base_dir (str): Base directory path.
        sections (list[str]): List of subdirectory names.

    Returns:
        list[str]: List of full paths to each section.
    """

    return [os.path.join(base_dir, section) for section in sections]


def clean_subtitle(file_path: str) -> str:
    """
    Cleans subtitle content by removing timestamps, numeric indices, and extra blank lines.

    Parameters:
        file_path (str): Path to the .srt subtitle file.

    Returns:
        str: Cleaned subtitle text.
    """

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        content = re.sub(
            r"\d{2}:\d{2}:\d{2},\d{3}\s*-->\s*\d{2}:\d{2}:\d{2},\d{3}\n", "", content)
        content = re.sub(r"^\d+\n", "", content, flags=re.MULTILINE)
        return re.sub(r"\n+", "\n", content).strip()
    except Exception as e:
        print(f"ERROR: Failed to clean subtitle file '{file_path}' - {e}")
        return ""


def merge_subtitles(paths: list[str]) -> str:
    """
    Merges cleaned subtitle content from all .srt files in the given paths.

    Parameters:
        paths (list[str]): List of section folder paths.

    Returns:
        str: Combined subtitle content and web documatation.
    """

    merged: list[str] = []
    links: list[str] = []

    for path in paths:
        for root, _dirs, _files in os.walk(path):
            folder = os.path.basename(root)
            merged.append(f"--- START FOLDER: {folder} ---")
            sort_files = sort_content(root)
            for file in sort_files:
                if file.endswith(".srt"):
                    file_path = os.path.join(root, file)
                    cleaned = clean_subtitle(file_path)
                    if cleaned:
                        merged.append(f"--- FILE: {file} ---\n\n{cleaned}\n")
                elif file.endswith(".html"):
                    link_path = os.path.join(root, file)
                    links.append(f"\n{link_path}\n")
                else:
                    pass
            if links:
                merged.append(f"--- WEB DOCUMENTATION ---")
                for link in links:
                    merged.append(link)
                links.clear()
            merged.append(f"--- STOP FOLDER: {folder} ---\n\n")
    return "\n".join(merged)


def write_output(content: str, output_file: str):
    """
    Writes merged subtitle content to the output file.

    Parameters:
        content (str): Merged subtitle text.
        output_file (str): Path to the output file.
    """

    try:
        if content:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"\nSUCCESS: Subtitles merged into '{output_file}'")
        else:
            print(
                f"ERROR: No content to write. Check BASE_FOLDER '{BASE_FOLDER}'.")
    except Exception as e:
        print(f"ERROR: Failed to write output file '{output_file}' - {e}")


def main():
    """
    Main function to initiate the subtitle merging process.
    """

    subdirs = sort_content(BASE_FOLDER)
    if subdirs:
        paths = build_section_paths(BASE_FOLDER, subdirs)
        merged_content = merge_subtitles(paths)
        write_output(merged_content, OUTPUT_FILE)


if __name__ == "__main__":
    main()
