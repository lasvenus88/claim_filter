import pandas as pd
from tqdm import tqdm
import sys

def analyze_duplicates(csv_file_path, columns=None, debug=False, output_csv="duplicates_and_singles.csv", max_duplicates=5):
    """
    Analyze duplicates in a CSV file, include up to max_duplicates per duplicate pattern and all non-duplicates,
    and export to a CSV with a duplicate_count column.
    
    Parameters:
    - csv_file_path: Path to the CSV file
    - columns: List of column names to consider for duplicates (None = all columns)
    - debug: If True, prints additional info for troubleshooting
    - output_csv: Path to save the output CSV file
    - max_duplicates: Maximum number of duplicate rows to include per pattern (default: 5)
    """
    try:
        # Read the CSV file
        print("Reading CSV file...")
        df = pd.read_csv(csv_file_path)
        
        # Get total number of rows and columns
        total_rows = len(df)
        print(f"Total rows in CSV: {total_rows}")
        print(f"Columns in CSV: {list(df.columns)}")
        
        if total_rows == 0:
            print("Error: CSV file is empty.")
            return
        
        # Check if specified columns exist
        if columns:
            missing_cols = [col for col in columns if col not in df.columns]
            if missing_cols:
                print(f"Error: Columns {missing_cols} not found in CSV.")
                return
        
        # Initialize progress bar and tracking
        print("Analyzing duplicates...")
        duplicate_counts = {}
        duplicate_indices = {}
        non_duplicate_indices = []
        
        # Identify duplicates and non-duplicates
        with tqdm(total=total_rows, desc="Processing rows", file=sys.stdout) as pbar:
            # Use specified columns or all columns
            duplicate_series = df.duplicated(subset=columns, keep=False)
            
            # Process each row
            for idx in range(total_rows):
                row_data = df.iloc[idx][columns] if columns else df.iloc[idx]
                row_tuple = tuple(row_data)
                
                if duplicate_series.iloc[idx]:
                    # Duplicate row
                    duplicate_counts[row_tuple] = duplicate_counts.get(row_tuple, 0) + 1
                    if row_tuple not in duplicate_indices:
                        duplicate_indices[row_tuple] = []
                    duplicate_indices[row_tuple].append(idx)
                else:
                    # Non-duplicate row
                    non_duplicate_indices.append(idx)
                    duplicate_counts[row_tuple] = 1  # Count of 1 for non-duplicates
                pbar.update(1)
        
        # Output results
        total_duplicates = sum(min(v, max_duplicates) for k, v in duplicate_counts.items() if v >= 2)
        total_non_duplicates = len(non_duplicate_indices)
        unique_duplicate_patterns = len([k for k, v in duplicate_counts.items() if v >= 2])
        
        print("\nAnalysis Complete!")
        print(f"Total duplicate rows (up to {max_duplicates} per pattern): {total_duplicates}")
        print(f"Total non-duplicate rows: {total_non_duplicates}")
        print(f"Unique duplicate row patterns: {unique_duplicate_patterns}")
        
        # Prepare data for export
        output_data = []
        
        if unique_duplicate_patterns > 0:
            print(f"\nDuplicate rows (limited to {max_duplicates} per pattern):")
            for row_tuple, count in duplicate_counts.items():
                if count >= 2:  # Only print duplicates here
                    print(f"Row {row_tuple}: {count} times (including up to {min(count, max_duplicates)} in output)")
                    # Include up to max_duplicates rows for this pattern
                    for idx in duplicate_indices[row_tuple][:max_duplicates]:
                        row_data = df.iloc[idx].copy()
                        row_data['duplicate_count'] = count
                        output_data.append(row_data)
        
        # Add non-duplicate rows
        for idx in non_duplicate_indices:
            row_data = df.iloc[idx].copy()
            row_tuple = tuple(df.iloc[idx][columns] if columns else df.iloc[idx])
            row_data['duplicate_count'] = duplicate_counts[row_tuple]
            output_data.append(row_data)
        
        # Convert to DataFrame and export to CSV
        if output_data:
            output_df = pd.DataFrame(output_data)
            output_df.to_csv(output_csv, index=False)
            print(f"\nExported {len(output_data)} rows (duplicates and non-duplicates) to '{output_csv}'")
        else:
            print("\nNo rows to export. No CSV created.")
        
        # Debug mode: Print sample data and duplicate info
        if debug:
            print("\nDebug Info:")
            print("Sample of first 5 rows:")
            print(df.head().to_string())
            print(f"\nRows marked as duplicates: {duplicate_series.sum()}")
            print(f"Duplicate check based on columns: {columns if columns else 'All columns'}")
        
        return duplicate_counts
    
    except FileNotFoundError:
        print(f"Error: File '{csv_file_path}' not found.")
    except pd.errors.EmptyDataError:
        print("Error: CSV file is empty.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    # Example usage
    csv_file = "Book3.csv"  # Replace with your CSV file path
    columns_to_check = None  # e.g., ['column1', 'column2'] or None for all columns
    output_file = "duplicates_and_singles.csv"  # Output CSV file name
    analyze_duplicates(csv_file, columns=columns_to_check, debug=True, output_csv=output_file, max_duplicates=5)
