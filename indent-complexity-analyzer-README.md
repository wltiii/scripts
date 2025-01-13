# How It Works

1. **Indentation Calculation**:
   - Logical indentation is determined by dividing spaces by the specified `--spaces` value and tabs by the specified `--tabs` value.

2. **Analysis**:
   - Ignores blank lines and lines with comments (lines starting with `#` or `//`).
   - Tracks the total complexity and flags lines exceeding the `--max` value.

3. **Output**:
   - Lists lines that exceed the max indentation threshold.
   - Provides aggregate statistics: total complexity, mean, median, and standard deviation.

4. **Command-Line Arguments**:
   - `filepath`: Path to the file to analyze.
   - `-s` or `--spaces`: Specify the number of spaces per logical indent (default: 4).
   - `-t` or `--tabs`: Specify the number of tabs per logical indent (default: 1).
   - `-m` or `--max`: Max indentation before flagging (default: 3).

## Usage Example

   ```bash
   python indent_analysis.py my_code.py -s 4 -t 1 -m 3
   ```
