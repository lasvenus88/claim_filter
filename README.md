# CSV Duplicate Analyzer

This Python script analyzes a CSV file to identify duplicate rows, limits the number of duplicate rows to a maximum of 5 per unique row pattern, includes non-duplicate rows (rows appearing exactly once), and exports the results to a new CSV file with a `duplicate_count` column indicating how many times each row appears in the original dataset. The script uses a progress bar to track processing and includes a debug mode for troubleshooting.

## Features
- **Duplicate Detection**: Identifies duplicate rows based on all columns or a specified subset of columns.
- **Duplicate Limiting**: Includes up to 5 instances of each duplicate row pattern in the output.
- **Non-Duplicate Inclusion**: Includes all non-duplicate rows (rows appearing exactly once) in the output.
- **Output**: Exports results to a CSV file with a `duplicate_count` column showing the total occurrences of each row in the original dataset.
- **Progress Bar**: Displays a progress bar during processing using the `tqdm` library.
- **Debug Mode**: Provides detailed output (e.g., sample data, duplicate counts) for troubleshooting.
- **Flexible Configuration**: Allows customization of input file, output file, columns to check for duplicates, and maximum duplicates per pattern.

## Requirements
- **Python**: Version 3.6 or higher
- **Dependencies**:
  - `pandas`: For CSV handling and data processing
  - `tqdm`: For progress bar display
- Install dependencies using:
  ```bash
  pip install pandas tqdm
