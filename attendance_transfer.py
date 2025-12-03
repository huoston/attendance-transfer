#!/usr/bin/env python3
"""
Attendance Transfer Script

This script transfers attendance data from Microsoft Forms Excel files to attendance 
template files, calculating attendance codes and minutes based on class start time 
and duration.

Usage:
    python attendance_transfer.py --start_time 13:00 --duration 180
    python attendance_transfer.py -s 13:00 -d 180

Author: Dr. Huoston Rodrigues
Institution: RMIT Vietnam
Email: huoston.rodriguesbatista@rmit.edu.vn
Date: November 2025
Version: 1.3
"""

import argparse
import os
import re
import sys
from datetime import datetime, timedelta
from typing import Tuple, Optional, Dict

import pandas as pd
import xlrd
from xlwt import Workbook, XFStyle
from xlutils.copy import copy as xlutils_copy


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments containing start_time and duration
        
    Raises:
        SystemExit: If arguments are invalid or missing
    """
    parser = argparse.ArgumentParser(
        description='Transfer attendance data from Microsoft Forms to attendance template',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python attendance_transfer.py --start_time 13:00 --duration 180
  python attendance_transfer.py -s 09:30 -d 120
        """
    )
    
    parser.add_argument(
        '-s', '--start_time',
        required=True,
        help='Class start time in HH:MM format (e.g., 13:00)'
    )
    
    parser.add_argument(
        '-d', '--duration',
        required=True,
        type=int,
        help='Class duration in minutes (e.g., 180)'
    )
    
    args = parser.parse_args()
    
    # Validate start_time format
    if not re.match(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', args.start_time):
        parser.error(f'Invalid start_time format: {args.start_time}. Expected HH:MM (e.g., 13:00)')
    
    # Validate duration
    if args.duration <= 0:
        parser.error(f'Duration must be positive, got: {args.duration}')
    
    return args


def extract_student_id(email: str) -> Optional[str]:
    """
    Extract numeric student ID from email address.
    
    Removes the 'S' prefix (case-insensitive) and everything after '@'.
    
    Args:
        email (str): Email in format S[ID]@rmit.edu.vn
        
    Returns:
        Optional[str]: Numeric student ID, or None if extraction fails
        
    Examples:
        >>> extract_student_id('S4186054@rmit.edu.vn')
        '4186054'
        >>> extract_student_id('s3992383@rmit.edu.vn')
        '3992383'
        >>> extract_student_id('4019025@rmit.edu.vn')
        '4019025'
    """
    if pd.isna(email) or not isinstance(email, str):
        return None
    
    try:
        # Extract part before '@'
        email_prefix = email.split('@')[0].strip()
        
        # Remove 'S' or 's' prefix if present
        if email_prefix.upper().startswith('S'):
            student_id = email_prefix[1:]
        else:
            student_id = email_prefix
        
        # Verify it's numeric
        if student_id.isdigit():
            return student_id
        else:
            print(f"Warning: Non-numeric student ID extracted from email: {email}")
            return None
            
    except Exception as e:
        print(f"Error extracting student ID from email '{email}': {e}")
        return None


def convert_date_format(date_obj: datetime) -> str:
    """
    Convert datetime object to DD/MM format (without leading zeros).
    
    Args:
        date_obj (datetime): Datetime object containing the date
        
    Returns:
        str: Date in D/M format (e.g., '3/12' not '03/12')
        
    Examples:
        >>> convert_date_format(datetime(2024, 11, 26))
        '26/11'
        >>> convert_date_format(datetime(2024, 12, 3))
        '3/12'
    """
    # Use %-d and %-m on Unix/Mac, %#d and %#m on Windows
    # But simpler: just format and remove leading zeros
    day = date_obj.day
    month = date_obj.month
    return f'{day}/{month}'


def calculate_attendance(
    completion_time: datetime,
    start_time_str: str,
    duration_minutes: int
) -> Tuple[str, int]:
    """
    Calculate attendance code and minutes based on completion time.
    
    Args:
        completion_time (datetime): When the student completed the attendance form
        start_time_str (str): Class start time in HH:MM format
        duration_minutes (int): Class duration in minutes
        
    Returns:
        Tuple[str, int]: Attendance code ('Y' or 'N') and minutes present
        
    Examples:
        Class starts at 13:00, duration 180 minutes (ends at 16:00)
        >>> calculate_attendance(datetime(2024, 11, 26, 13, 0), '13:00', 180)
        ('Y', 180)
        >>> calculate_attendance(datetime(2024, 11, 26, 13, 15), '13:00', 180)
        ('Y', 165)
        >>> calculate_attendance(datetime(2024, 11, 26, 16, 30), '13:00', 180)
        ('N', 0)
    """
    # Parse start time
    start_hour, start_minute = map(int, start_time_str.split(':'))
    
    # Create class start datetime using the completion date
    class_start = completion_time.replace(
        hour=start_hour,
        minute=start_minute,
        second=0,
        microsecond=0
    )
    
    # Calculate class end time
    class_end = class_start + timedelta(minutes=duration_minutes)
    
    # If student arrived before class started, they're present for full duration
    if completion_time <= class_start:
        return 'Y', duration_minutes
    
    # If student arrived after class ended, they're absent
    if completion_time >= class_end:
        return 'N', 0
    
    # Student arrived during class - calculate remaining minutes
    minutes_late = (completion_time - class_start).total_seconds() / 60
    minutes_present = duration_minutes - int(minutes_late)
    
    return 'Y', minutes_present


def find_forms_file() -> Optional[str]:
    """
    Find the Microsoft Forms file (.xlsx) in the current directory.
    
    Returns:
        Optional[str]: Filename of the .xlsx file, or None if not found
    """
    xlsx_files = [f for f in os.listdir('.') if f.endswith('.xlsx')]
    
    if len(xlsx_files) == 0:
        print("Error: No .xlsx file found in the current directory")
        return None
    elif len(xlsx_files) > 1:
        print(f"Warning: Multiple .xlsx files found. Using: {xlsx_files[0]}")
    
    return xlsx_files[0]


def find_template_file() -> Optional[str]:
    """
    Find the attendance template file (.xls) in the current directory.
    
    Returns:
        Optional[str]: Filename of the .xls file, or None if not found
    """
    xls_files = [f for f in os.listdir('.') if f.endswith('.xls') and not f.endswith('.xlsx')]
    
    if len(xls_files) == 0:
        print("Error: No .xls file found in the current directory")
        return None
    elif len(xls_files) > 1:
        print(f"Warning: Multiple .xls files found. Using: {xls_files[0]}")
    
    return xls_files[0]


def read_forms_data(filename: str) -> pd.DataFrame:
    """
    Read and process Microsoft Forms Excel file.
    
    Args:
        filename (str): Path to the .xlsx file
        
    Returns:
        pd.DataFrame: Processed dataframe with student_id, date, and completion_time
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        Exception: If there's an error reading the file
    """
    print(f"\nReading Microsoft Forms file: {filename}")
    
    try:
        df = pd.read_excel(filename)
        print(f"  Loaded {len(df)} records")
        
        # Extract student IDs from Email column
        df['student_id'] = df['Email'].apply(extract_student_id)
        
        # Convert start time to date format DD/MM
        df['date'] = df['Start time'].apply(convert_date_format)
        
        # Keep only necessary columns
        result = df[['student_id', 'date', 'Completion time']].copy()
        
        # Remove records with missing student IDs
        result = result.dropna(subset=['student_id'])
        
        print(f"  Extracted {len(result)} valid student records")
        
        return result
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        raise
    except Exception as e:
        print(f"Error reading forms file: {e}")
        raise


def read_template_file(filename: str) -> Tuple[pd.DataFrame, Dict]:
    """
    Read attendance template file and extract structure information.
    
    Args:
        filename (str): Path to the .xls template file
        
    Returns:
        Tuple[pd.DataFrame, Dict]: 
            - DataFrame with the raw template data
            - Dictionary mapping dates to column indices
            
    The template has a multi-level header:
    - Row 3: Dates (DD/MM format)
    - Row 4: Sub-headers (Code, Minutes)
    - Row 5+: Student data
    """
    print(f"\nReading attendance template file: {filename}")
    
    try:
        # Read without header to get raw structure
        df = pd.read_excel(filename, header=None)
        
        # Extract date row (row index 3)
        date_row = df.iloc[3]
        
        # Extract sub-header row (row index 4)
        subheader_row = df.iloc[4]
        
        # Build date column mapping
        date_columns = {}
        for col_idx, date_val in enumerate(date_row):
            if pd.notna(date_val) and isinstance(date_val, str) and '/' in date_val:
                # This is a date column
                # The Code column is at col_idx, Minutes at col_idx + 1
                date_columns[date_val] = {
                    'code_col': col_idx,
                    'minutes_col': col_idx + 1
                }
        
        print(f"  Found {len(date_columns)} date columns: {list(date_columns.keys())}")
        print(f"  Template has {len(df) - 5} student records")
        
        return df, date_columns
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        raise
    except Exception as e:
        print(f"Error reading template file: {e}")
        raise


def update_attendance_data(
    forms_df: pd.DataFrame,
    template_df: pd.DataFrame,
    date_columns: Dict,
    start_time: str,
    duration: int
) -> pd.DataFrame:
    """
    Update attendance template with data from Microsoft Forms.
    
    Args:
        forms_df (pd.DataFrame): Processed forms data
        template_df (pd.DataFrame): Raw template data
        date_columns (Dict): Mapping of dates to column indices
        start_time (str): Class start time in HH:MM format
        duration (int): Class duration in minutes
        
    Returns:
        pd.DataFrame: Updated template dataframe
    """
    print("\nProcessing attendance data...")
    
    updated_df = template_df.copy()
    updates_count = 0
    
    # Get all dates being processed from forms
    dates_in_forms = forms_df['date'].unique()
    
    # Process each form submission
    for _, form_row in forms_df.iterrows():
        student_id = str(int(float(form_row['student_id'])))
        date = form_row['date']
        completion_time = form_row['Completion time']
        
        # Check if this date exists in the template
        if date not in date_columns:
            print(f"  Warning: Date {date} not found in template for student {student_id}")
            continue
        
        # Find the student in the template (student IDs start at row 5, column 0)
        student_found = False
        for row_idx in range(5, len(updated_df)):
            template_student_id = str(int(updated_df.iloc[row_idx, 0])) if pd.notna(updated_df.iloc[row_idx, 0]) else None
            
            if template_student_id == student_id:
                student_found = True
                
                # Calculate attendance
                code, minutes = calculate_attendance(completion_time, start_time, duration)
                
                # Update the template
                code_col = date_columns[date]['code_col']
                minutes_col = date_columns[date]['minutes_col']
                
                updated_df.iloc[row_idx, code_col] = code
                updated_df.iloc[row_idx, minutes_col] = minutes
                
                updates_count += 1
                print(f"  Updated student {student_id} for {date}: Code={code}, Minutes={minutes}")
                break
        
        if not student_found:
            print(f"  Warning: Student {student_id} not found in template")
    
    print(f"\nTotal updates made: {updates_count}")
    
    # Mark absent students (those who didn't submit the form) as 'N' with 0 minutes
    print("\nMarking absent students...")
    absent_count = 0
    
    for date in dates_in_forms:
        if date not in date_columns:
            continue
            
        code_col = date_columns[date]['code_col']
        minutes_col = date_columns[date]['minutes_col']
        
        # Check each student in the template
        for row_idx in range(5, len(updated_df)):
            current_code = updated_df.iloc[row_idx, code_col]
            
            # If the code is still '--' (default value), student is absent
            if current_code == '--':
                updated_df.iloc[row_idx, code_col] = 'N'
                updated_df.iloc[row_idx, minutes_col] = 0
                
                student_id = updated_df.iloc[row_idx, 0]
                print(f"  Marked student {student_id} as absent for {date}: Code=N, Minutes=0")
                absent_count += 1
    
    print(f"\nTotal absent students marked: {absent_count}")
    return updated_df


def save_updated_template(df: pd.DataFrame, original_filename: str) -> str:
    """
    Save the updated template as a new .xls file with '_updated' suffix,
    preserving the original formatting using xlutils.copy.
    
    Args:
        df (pd.DataFrame): Updated template dataframe
        original_filename (str): Original template filename
        
    Returns:
        str: Filename of the saved file
    """
    # Create output filename
    base_name = os.path.splitext(original_filename)[0]
    output_filename = f"{base_name}_updated.xls"
    
    print(f"\nSaving updated file: {output_filename}")
    
    try:
        # Open the original file with xlrd to preserve formatting
        rb = xlrd.open_workbook(original_filename, formatting_info=True)
        rs = rb.sheet_by_index(0)
        
        # Copy the workbook to preserve all formatting
        wb = xlutils_copy(rb)
        
        # Get the first sheet for writing
        ws = wb.get_sheet(0)
        
        # Only write cells that have been updated (not NaN and different from original)
        for row_idx in range(len(df)):
            for col_idx in range(len(df.columns)):
                updated_value = df.iloc[row_idx, col_idx]
                
                # Skip if the value is NaN (not updated)
                if pd.isna(updated_value):
                    continue
                
                # Get original value to check if it changed
                if row_idx < rs.nrows and col_idx < rs.ncols:
                    original_value = rs.cell(row_idx, col_idx).value
                    
                    # Convert both to strings for comparison (handles type differences)
                    # IMPORTANT: Handle 0 and False explicitly
                    orig_str = str(original_value) if original_value is not None and original_value != '' else ""
                    updated_str = str(updated_value) if updated_value is not None and updated_value != '' else ""
                    
                    # Only write if the value actually changed
                    if orig_str != updated_str:
                        if isinstance(updated_value, (int, float)):
                            ws.write(row_idx, col_idx, updated_value)
                        else:
                            ws.write(row_idx, col_idx, str(updated_value))
                else:
                    # New cell (beyond original file), write it
                    if isinstance(updated_value, (int, float)):
                        ws.write(row_idx, col_idx, updated_value)
                    else:
                        ws.write(row_idx, col_idx, str(updated_value))
        
        # Save the workbook
        wb.save(output_filename)
        print(f"  Successfully saved: {output_filename}")
        
        return output_filename
        
    except Exception as e:
        print(f"Error saving file: {e}")
        raise


def main():
    """
    Main function to orchestrate the attendance transfer process.
    """
    print("=" * 80)
    print("ATTENDANCE TRANSFER SCRIPT")
    print("=" * 80)
    
    # Parse command-line arguments
    args = parse_arguments()
    
    print(f"\nConfiguration:")
    print(f"  Class start time: {args.start_time}")
    print(f"  Class duration: {args.duration} minutes")
    
    try:
        # Find input files
        forms_file = find_forms_file()
        template_file = find_template_file()
        
        if not forms_file or not template_file:
            print("\nError: Required files not found")
            sys.exit(1)
        
        # Read forms data
        forms_df = read_forms_data(forms_file)
        
        # Read template
        template_df, date_columns = read_template_file(template_file)
        
        # Update attendance data
        updated_df = update_attendance_data(
            forms_df,
            template_df,
            date_columns,
            args.start_time,
            args.duration
        )
        
        # Save updated template
        output_file = save_updated_template(updated_df, template_file)
        
        print("\n" + "=" * 80)
        print("PROCESS COMPLETED SUCCESSFULLY")
        print("=" * 80)
        print(f"\nOutput file: {output_file}")
        print(f"You can now use this file for attendance tracking.")
        
    except Exception as e:
        print(f"\n{'=' * 80}")
        print("ERROR OCCURRED")
        print("=" * 80)
        print(f"\n{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
