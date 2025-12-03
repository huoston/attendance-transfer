# Attendance Transfer Script

Automate the transfer of attendance data from Microsoft Forms Excel files to attendance template files, with automatic calculation of attendance codes and minutes based on class timing.

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.3-orange)](https://github.com/yourusername/attendance-transfer)

## 📋 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Examples](#examples)
- [Requirements](#requirements)
- [File Structure](#file-structure)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

## ✨ Features

- ✅ **Automatic Student ID Extraction** - Extracts numeric IDs from email addresses (handles S prefix)
- ✅ **Date Format Conversion** - Converts MM/DD/YY to DD/MM format automatically
- ✅ **Smart Attendance Calculation** - Calculates attendance based on arrival time
- ✅ **Late Arrival Support** - Deducts minutes for students who arrive late
- ✅ **Absent Student Marking** - Automatically marks non-respondents as absent
- ✅ **Format Preservation** - Maintains original Excel template formatting
- ✅ **Comprehensive Error Handling** - Detailed error messages and validation
- ✅ **Command-Line Interface** - Easy to use with simple arguments

## 🚀 Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

### Install Dependencies

```bash
pip install pandas openpyxl xlrd xlwt xlutils
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

### Download the Script

Clone this repository:

```bash
git clone https://github.com/yourusername/attendance-transfer.git
cd attendance-transfer
```

Or download the script directly:
- [attendance_transfer.py](attendance_transfer.py)

## 📖 Usage

### Basic Command

```bash
python attendance_transfer.py --start_time HH:MM --duration MINUTES
```

### Arguments

| Argument | Short | Required | Description | Example |
|----------|-------|----------|-------------|---------|
| `--start_time` | `-s` | Yes | Class start time in HH:MM format | `13:00` |
| `--duration` | `-d` | Yes | Class duration in minutes | `180` |

### Quick Examples

**Afternoon class (1:00 PM, 3 hours):**
```bash
python attendance_transfer.py --start_time 13:00 --duration 180
```

**Morning class (9:30 AM, 2 hours):**
```bash
python attendance_transfer.py -s 09:30 -d 120
```

**Evening class (6:00 PM, 1.5 hours):**
```bash
python attendance_transfer.py --start_time 18:00 --duration 90
```

## 🔍 How It Works

### 1. Student ID Extraction

The script extracts student IDs from email addresses:
- `S4186054@rmit.edu.vn` → `4186054`
- `s3992383@rmit.edu.vn` → `3992383` (case-insensitive)
- `4019025@rmit.edu.vn` → `4019025` (no prefix)

### 2. Date Conversion

Converts dates from Microsoft Forms format to template format:
- Forms: `11/26/25 7:52:05` (MM/DD/YY HH:MM:SS)
- Template: `26/11` (DD/MM)

### 3. Attendance Calculation

**Example Configuration:**
- Class start: 13:00
- Duration: 180 minutes (3 hours)
- Class end: 16:00

**Calculation Logic:**

| Arrival Time | Code | Minutes | Explanation |
|--------------|------|---------|-------------|
| 13:00 or earlier | Y | 180 | On time - full attendance |
| 13:15 | Y | 165 | 15 minutes late |
| 13:45 | Y | 135 | 45 minutes late |
| 14:30 | Y | 90 | 1.5 hours late |
| 16:00 or later | N | 0 | Arrived after class ended |

**Formula:**
```
IF arrival_time <= class_start THEN
    code = 'Y'
    minutes = full_duration
ELSE IF arrival_time >= class_end THEN
    code = 'N'
    minutes = 0
ELSE
    code = 'Y'
    minutes = duration - minutes_late
END IF
```

### 4. Absent Student Handling

Students who did not respond to the Microsoft Forms are automatically marked:
- **Code:** N (absent)
- **Minutes:** 0

## 📂 File Structure

### Input Files (must be in same folder as script)

**1. Microsoft Forms File (.xlsx)**
- Contains attendance responses from Microsoft Forms
- Required columns:
  - `Email`: Student email (S[ID]@rmit.edu.vn)
  - `Start time`: Form submission start time
  - `Completion time`: Form submission completion time

**2. Attendance Template (.xls)**
- Your existing attendance tracking template
- Structure:
  - Column 0: Student ID (numeric)
  - Date columns with sub-headers:
    - `Code`: Y (present) or N (absent)
    - `Minutes`: Number of minutes present

### Output File

- Automatically saved in the same folder
- Filename format: `[original_name]_updated.xls`
- Example: `attendance.xls` → `attendance_updated.xls`
- **Preserves original formatting** (borders, fonts, colors)

## 💡 Examples

### Example 1: Standard Tutorial

Files in folder:
```
attendance_transfer.py
Attendance_Week5_Tutorial.xlsx
attendance_COMM2752_Tutorial.xls
```

Command:
```bash
python attendance_transfer.py --start_time 13:00 --duration 180
```

Output:
```
attendance_COMM2752_Tutorial_updated.xls
```

Console output:
```
================================================================================
ATTENDANCE TRANSFER SCRIPT
================================================================================

Configuration:
  Class start time: 13:00
  Class duration: 180 minutes

Reading Microsoft Forms file: Attendance_Week5_Tutorial.xlsx
  Loaded 16 records
  Extracted 16 valid student records

Processing attendance data...
  Updated student 3903858 for 26/11: Code=Y, Minutes=180
  ...

Total updates made: 16

Marking absent students...
  Marked student 3978119 as absent for 26/11: Code=N, Minutes=0
  ...

Total absent students marked: 7

================================================================================
PROCESS COMPLETED SUCCESSFULLY
================================================================================
```

### Example 2: Multiple Classes

Process attendance for different classes by ensuring the correct files are in the folder:

```bash
# Morning class
python attendance_transfer.py -s 09:00 -d 120

# Afternoon class  
python attendance_transfer.py -s 14:00 -d 180
```

## 📋 Requirements

### Python Version
- Python 3.6 or higher

### Dependencies
```
pandas>=1.3.0
openpyxl>=3.0.0
xlrd>=2.0.0
xlwt>=1.3.0
xlutils>=2.0.0
```

See [requirements.txt](requirements.txt) for exact versions.

## 🔧 Troubleshooting

### Common Errors

**Error: No .xlsx file found**
```
Error: No .xlsx file found in the current directory
```
**Solution:** Ensure your Microsoft Forms file is in the same folder as the script

**Error: Invalid time format**
```
Invalid start_time format: 1:00. Expected HH:MM (e.g., 13:00)
```
**Solution:** Use two-digit format: `01:00` instead of `1:00`

**Warning: Student not found**
```
Warning: Student 4186054 not found in template
```
**Solution:** This is informational - the student exists in Forms but not in your template

**Warning: Date not found**
```
Warning: Date 26/11 not found in template for student 4186054
```
**Solution:** The forms date doesn't match any date column in the template

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### How to Contribute

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/attendance-transfer.git
cd attendance-transfer

# Install dependencies
pip install -r requirements.txt

# Run tests
python test_attendance.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Dr. Huoston Rodrigues**
- Institution: RMIT Vietnam
- Email: huoston.rodriguesbatista@rmit.edu.vn
- GitHub: [@yourusername](https://github.com/yourusername)

## 🙏 Acknowledgments

- Developed for RMIT Vietnam to automate attendance tracking
- Thanks to all teaching staff who provided feedback and requirements
- Special thanks to the Python community for excellent libraries

## 📊 Version History

- **v1.3** (November 2025) - Current version
  - Automatic student ID extraction from emails
  - Date format conversion
  - Attendance calculation with late arrival support
  - Absent student marking
  - Format preservation using xlutils
  - Comprehensive error handling

## 🔗 Related Projects

- [pandas](https://pandas.pydata.org/) - Data manipulation library
- [openpyxl](https://openpyxl.readthedocs.io/) - Excel file handling
- [xlutils](https://xlutils.readthedocs.io/) - Excel utilities

## 📞 Support

For questions, issues, or feature requests:
- Open an issue on [GitHub Issues](https://github.com/yourusername/attendance-transfer/issues)
- Email: huoston.rodriguesbatista@rmit.edu.vn

## ⭐ Star History

If this project helped you, please consider giving it a star ⭐

---

**Made with ❤️ for RMIT Vietnam**
