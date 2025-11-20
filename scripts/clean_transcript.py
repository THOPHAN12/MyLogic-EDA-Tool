#!/usr/bin/env python3
"""
Script để dọn sạch ANSI escape codes từ transcript file.

Loại bỏ tất cả ANSI escape sequences từ file transcript để dễ đọc hơn.
"""

import sys
import re
from pathlib import Path


def strip_ansi_codes(text):
    """Remove ANSI escape sequences from text."""
    # ANSI escape code pattern: ESC [ ... m (for colors/formatting)
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)


def clean_transcript(input_file, output_file=None):
    """Clean ANSI codes from transcript file."""
    input_path = Path(input_file)
    
    if not input_path.exists():
        print(f"ERROR: File not found: {input_file}")
        return False
    
    # Read original file
    print(f"Reading: {input_path}")
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Clean ANSI codes
    print("Cleaning ANSI escape codes...")
    cleaned_content = strip_ansi_codes(content)
    
    # Determine output file
    if output_file is None:
        # Add _cleaned suffix before extension
        output_path = input_path.parent / f"{input_path.stem}_cleaned{input_path.suffix}"
    else:
        output_path = Path(output_file)
    
    # Write cleaned file
    print(f"Writing: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)
    
    # Compare sizes
    original_size = len(content)
    cleaned_size = len(cleaned_content)
    removed = original_size - cleaned_size
    
    print(f"\nCleaning complete!")
    print(f"  Original size: {original_size:,} bytes")
    print(f"  Cleaned size: {cleaned_size:,} bytes")
    print(f"  Removed: {removed:,} bytes ({removed/original_size*100:.1f}%)")
    print(f"\nCleaned file saved to: {output_path}")
    
    return True


def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python clean_transcript.py <input_file> [output_file]")
        print("\nExample:")
        print("  python clean_transcript.py outputs/test_transcript_20251120_133209.txt")
        print("  python clean_transcript.py outputs/test_transcript_20251120_133209.txt outputs/cleaned.txt")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    success = clean_transcript(input_file, output_file)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

