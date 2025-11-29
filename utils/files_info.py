"""
Script to display all files in the repository with their relative paths and sizes.
Organized by directory structure.
"""

import os
from pathlib import Path


def format_size(size_bytes: int) -> str:
    """Convert bytes to human-readable format."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"


def get_all_files(root_path: Path) -> list[tuple[str, int]]:
    """Get all files with their relative paths and sizes."""
    files = []
    
    for file_path in root_path.rglob("*"):
        if file_path.is_file():
            # Skip git internals and common non-essential files
            if ".git" in file_path.parts:
                continue
            if "__pycache__" in file_path.parts:
                continue
            if file_path.suffix == ".pyc":
                continue
                
            relative_path = file_path.relative_to(root_path)
            size = file_path.stat().st_size
            files.append((str(relative_path), size))
    
    return sorted(files, key=lambda x: x[0])


def print_files_by_directory(files: list[tuple[str, int]]) -> None:
    """Print files organized by directory."""
    current_dir = None
    dir_total = 0
    grand_total = 0
    
    print("=" * 70)
    print(f"{'📁 REPOSITORY FILE STRUCTURE':^70}")
    print("=" * 70)
    print()
    
    for file_path, size in files:
        parts = Path(file_path).parts
        
        # Determine the directory (or root)
        if len(parts) == 1:
            file_dir = "."
        else:
            file_dir = str(Path(*parts[:-1]))
        
        # Print directory header when it changes
        if file_dir != current_dir:
            if current_dir is not None:
                print(f"  {'─' * 50}")
                print(f"  📊 Directory total: {format_size(dir_total):>15}")
                print()
            
            current_dir = file_dir
            dir_total = 0
            print(f"📂 {file_dir}/")
            print(f"  {'─' * 50}")
        
        # Print file info
        file_name = parts[-1]
        dir_total += size
        grand_total += size
        print(f"  📄 {file_name:<40} {format_size(size):>10}")
    
    # Print last directory total
    if current_dir is not None:
        print(f"  {'─' * 50}")
        print(f"  📊 Directory total: {format_size(dir_total):>15}")
    
    # Print grand total
    print()
    print("=" * 70)
    print(f"📊 TOTAL FILES: {len(files):<10} TOTAL SIZE: {format_size(grand_total):>15}")
    print("=" * 70)


def main() -> None:
    """Main entry point."""
    # Go up one level from utils/ to reach the repo root
    root_path = Path(__file__).parent.parent
    
    print()
    print(f"🔍 Scanning: {root_path.absolute()}")
    print()
    
    files = get_all_files(root_path)
    
    if not files:
        print("No files found in the repository.")
        return
    
    print_files_by_directory(files)


if __name__ == "__main__":
    main()