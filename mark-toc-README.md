# Key Features of the Script

1. **Backup Creation**:
   - Automatically creates a backup of the file with a timestamped suffix before modifying it.

2. **Header Parsing**:
   - Identifies Markdown headers (`##`, `###`, etc.) up to a user-defined depth.

3. **TOC Generation**:
   - Creates a hierarchical table of contents based on the headers, using indentation for subheadings.

4. **TOC Insertion**:
   - Inserts the TOC after the title heading (`#`) or at the beginning if no title heading is found.

5. **Command-Line Options**:
   - `filepath`: Path to the Markdown file.
   - `-d` or `--depth`: Depth of the TOC (1-5). Default is 3.
   - Validates that the depth is an integer between 1 and 5.

## Example Usage

```bash
python markdown_toc_generator.py my_document.md --depth 3
```
