"""
Data parsing utilities for CSV and manual input
"""
import pandas as pd
import numpy as np
from typing import List, Tuple, Dict
import io
import csv


class DataParser:
    """Utility class for parsing input data"""
    
    @staticmethod
    def parse_manual_input(x_string: str, y_string: str) -> Tuple[List[float], List[float]]:
        """Parse manual input strings into lists of floats"""
        try:
            # Clean and split the input strings
            x_values = [float(x.strip()) for x in x_string.split(',') if x.strip()]
            y_values = [float(y.strip()) for y in y_string.split(',') if y.strip()]
            
            if len(x_values) != len(y_values):
                raise ValueError("Number of X and Y values must be equal")
            
            if len(x_values) < 2:
                raise ValueError("At least 2 data points are required")
            
            return x_values, y_values
            
        except ValueError as e:
            if "could not convert string to float" in str(e):
                raise ValueError("All values must be valid numbers")
            raise e
    
    @staticmethod
    def parse_csv_file(file_content: str) -> Tuple[List[float], List[float]]:
        """Parse CSV file content into X and Y values"""
        try:
            # Try to read CSV with different delimiters
            csv_reader = csv.reader(io.StringIO(file_content))
            rows = list(csv_reader)
            
            if len(rows) < 2:
                raise ValueError("CSV file must contain at least 2 rows of data")
            
            # Check if first row is header
            first_row = rows[0]
            try:
                # Try to convert first row to floats
                [float(val) for val in first_row if val.strip()]
                has_header = False
            except ValueError:
                has_header = True
            
            # Extract data rows
            data_rows = rows[1:] if has_header else rows
            
            if len(data_rows) < 2:
                raise ValueError("CSV file must contain at least 2 rows of numerical data")
            
            x_values = []
            y_values = []
            
            for i, row in enumerate(data_rows):
                if len(row) < 2:
                    raise ValueError(f"Row {i + (2 if has_header else 1)} must contain at least 2 values")
                
                try:
                    x_val = float(row[0].strip()) if row[0].strip() else None
                    y_val = float(row[1].strip()) if row[1].strip() else None
                    
                    if x_val is not None and y_val is not None:
                        x_values.append(x_val)
                        y_values.append(y_val)
                        
                except ValueError:
                    raise ValueError(f"Row {i + (2 if has_header else 1)} contains invalid numerical data")
            
            if len(x_values) < 2:
                raise ValueError("At least 2 valid data points are required")
            
            # Sort by X values
            sorted_pairs = sorted(zip(x_values, y_values))
            x_values, y_values = zip(*sorted_pairs)
            
            return list(x_values), list(y_values)
            
        except Exception as e:
            raise ValueError(f"Error parsing CSV file: {str(e)}")
    
    @staticmethod
    def validate_data_for_method(x_values: List[float], y_values: List[float], method: str) -> Dict[str, str]:
        """Validate data compatibility with specific integration method"""
        errors = {}
        n = len(x_values) - 1  # number of intervals
        
        # Note: Adaptive integration now handles both equal and unequal intervals
        # No strict validation required - the methods will automatically adapt
        
        return errors