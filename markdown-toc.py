import argparse
import os
import re
from datetime import datetime


def backup_file(filepath):
    """Creates a backup of the given file with a timestamped suffix."""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = f"{filepath}.TOC-{timestamp}"
    with open(filepath, "r") as original:
        content = original.read()
    with open(backup_path, "w") as backup:
        backup.write(content)
    return backup_path


def parse_markdown_headers(content, max_depth):
    """Parses the markdown content and extracts headers up to the specified depth."""
    headers = []
    for line in content.splitlines():
        match = re.match(r"^(#{2,6})\s+(.*)", line)
        if match:
            level = len(match.group(1))  # Number of '#' determines the level
            if 2 <= level <= max_depth + 1:
                headers.append((level, match.group(2).strip()))
    return headers


def generate_toc(headers):
    """Generates a table of contents from parsed headers."""
    toc = []
    for level, title in headers:
        indent = "  " * (level - 2)  # Indent based on heading level
        link = re.sub(r"[^a-zA-Z0-9\s]", "", title).replace(" ", "-").lower()
        toc.append(f"{indent}- [{title}](#{link})")
    return "\n".join(toc)


def insert_toc(content, toc):
    """Inserts the table of contents after the first title heading."""
    lines = content.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("# "):
            return "\n".join(lines[:i + 1] + ["\n## Table of Contents\n", toc, ""] + lines[i + 1:])
    # If no title heading is found, prepend the TOC
    return f"## Table of Contents\n{toc}\n\n{content}"


def validate_depth(value):
    """Validates that the depth value is an integer between 1 and 5."""
    try:
        depth = int(value)
        if 1 <= depth <= 5:
            return depth
        raise argparse.ArgumentTypeError("Depth must be between 1 and 5.")
    except ValueError:
        raise argparse.ArgumentTypeError("Depth must be an integer.")


def parse_args():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate a Table of Contents for a Markdown file."
    )
    parser.add_argument(
        "filepath", type=str, help="Path to the Markdown file to process."
    )
    parser.add_argument(
        "-d",
        "--depth",
        type=validate_depth,
        default=3,
        help="Depth of headings to include in the TOC (1-5). Default is 3.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Backup the original file
    backup_path = backup_file(args.filepath)
    print(f"Backup created: {backup_path}")

    # Read the original content
    with open(args.filepath, "r") as file:
        content = file.read()

    # Parse headers and generate TOC
    headers = parse_markdown_headers(content, args.depth)
    toc = generate_toc(headers)

    # Insert TOC into the content
    updated_content = insert_toc(content, toc)

    # Write updated content back to the original file
    with open(args.filepath, "w") as file:
        file.write(updated_content)

    print(f"Table of Contents generated and inserted into {args.filepath}")


if __name__ == "__main__":
    main()
