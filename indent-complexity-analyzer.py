# python indent_analysis.py my_code.py -s 4 -t 1 -m 3
import argparse
import math
import statistics


def parse_args():
    parser = argparse.ArgumentParser(
        description="Analyze indentation complexity of a source code file."
    )
    parser.add_argument(
        "filepath", type=str, help="Path to the source code file to analyze."
    )
    parser.add_argument(
        "-s", "--spaces", type=int, default=4, help="Number of spaces per logical indent."
    )
    parser.add_argument(
        "-t", "--tabs", type=int, default=1, help="Number of tabs per logical indent."
    )
    parser.add_argument(
        "-m", "--max", type=int, default=3, help="Max logical indentation before flagging."
    )
    return parser.parse_args()


def calculate_indentation(line, spaces_per_indent, tabs_per_indent):
    spaces = line.count(" ")
    tabs = line.count("\t")
    return spaces // spaces_per_indent + tabs // tabs_per_indent


def analyze_file(filepath, spaces_per_indent, tabs_per_indent, max_indent):
    try:
        with open(filepath, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        return None

    indent_levels = []
    flagged_lines = []

    for line_number, line in enumerate(lines, start=1):
        stripped_line = line.strip()
        if not stripped_line or stripped_line.startswith("#") or stripped_line.startswith("//"):
            # Ignore blank lines and comments
            continue

        indent_level = calculate_indentation(line, spaces_per_indent, tabs_per_indent)
        indent_levels.append((line_number, indent_level))

        if indent_level > max_indent:
            flagged_lines.append((line_number, indent_level))

    # Extract indentation values for statistics
    indent_values = [level for _, level in indent_levels]
    total_complexity = sum(indent_values)
    stats = {
        "total": total_complexity,
        "mean": statistics.mean(indent_values) if indent_values else 0,
        "median": statistics.median(indent_values) if indent_values else 0,
        "std_dev": statistics.stdev(indent_values) if len(indent_values) > 1 else 0,
    }

    return flagged_lines, stats


def main():
    args = parse_args()

    flagged_lines, stats = analyze_file(
        args.filepath, args.spaces, args.tabs, args.max
    )

    if flagged_lines is None:
        return

    print("\nIndentation Complexity Analysis:\n")
    print(f"File: {args.filepath}\n")

    if flagged_lines:
        print("Lines exceeding max indentation:")
        for line_number, indent_level in flagged_lines:
            print(f"  Line {line_number}: Indentation level {indent_level}")
    else:
        print("No lines exceeded the max indentation level.")

    print("\nAggregate Statistics:")
    print(f"  Total Complexity: {stats['total']}")
    print(f"  Mean Complexity: {stats['mean']:.2f}")
    print(f"  Median Complexity: {stats['median']:.2f}")
    print(f"  Standard Deviation: {stats['std_dev']:.2f}")


if __name__ == "__main__":
    main()
