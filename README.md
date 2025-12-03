# Attendance Transfer Script

Automate the transfer of attendance data from Microsoft Forms (QR code responses) to RMIT myTimetable attendance templates, with automatic calculation of attendance codes and late arrival minutes.

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.3-orange)](https://github.com/huoston/attendance-transfer)

## 📋 Table of Contents

- [Overview](#-overview)
- [Workflow](#-workflow)
- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [How It Works](#-how-it-works)
- [File Structure](#-file-structure)
- [Examples](#-examples)
- [Requirements](#-requirements)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

## 🎯 Overview

This script bridges Microsoft Forms attendance collection (via QR codes) with RMIT's myTimetable system, automatically calculating attendance status and late arrival minutes based on class timing.

### The Problem It Solves

Manual data entry from Microsoft Forms to myTimetable is:
- ⏰ Time-consuming
- ❌ Error-prone
- 🔢 Requires calculating late minutes manually
- 📊 Tedious for large classes

### The Solution

This script automates the entire process:
- ✅ Reads QR code attendance responses from Microsoft Forms
- ✅ Calculates late arrival minutes automatically
- ✅ Updates myTimetable template with proper formatting
- ✅ Marks absent students who didn't scan the QR code

## 🔄 Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. DURING CLASS                                                 │
│    Students scan QR code → Microsoft Forms captures timestamp   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 2. DOWNLOAD FILES                                               │
│    • Export Forms responses → .xlsx file                        │
│    • Download attendance template from mytimetable.rmit.edu.vn  │
│      → .xls file                                                │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 3. RUN SCRIPT                                                   │
│    python attendance_transfer.py -s 13:00 -d 180                │
│                                                                 │
│    Script automatically:                                        │
│    • Extracts student IDs from email addresses                 │
│    • Calculates late arrival minutes                           │
│    • Marks present students (Y) with minutes                   │
│    • Marks absent students (N) with 0 minutes                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 4. UPLOAD TO MYTIMETABLE                                        │
│    Import the generated *_updated.xls file back to              │
│    mytimetable.rmit.edu.vn                                      │
└─────────────────────────────────────────────────────────────────┘
```

## ✨ Features

### Core Functionality
- ✅ **QR Code Integration** - Processes Microsoft Forms responses from QR code scans
- ✅ **Automatic Student ID Extraction** - Extracts numeric IDs from email addresses
- ✅ **Late Arrival Calculation** - Automatically calculates minutes late based on scan time
- ✅ **Smart Attendance Codes** - Assigns Y (present) or N (absent) automatically
- ✅ **Absent Student Detection** - Marks students who didn't scan QR code as absent
- ✅ **Format Preservation** - Maintains myTimetable Excel template formatting
- ✅ **myTimetable Compatible** - Output ready for direct import to mytimetable.rmit.edu.vn

### Technical Features
- ✅ **Date Format Conversion** - Converts MM/DD/YY to D/M format (matches myTimetable)
- ✅ **Comprehensive Error Handling** - Detailed error messages and validation
- ✅ **Command-Line Interface** - Easy to use with simple arguments
- ✅ **Batch Processing** - Process entire class in seconds

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
git clone https://github.com/huoston/attendance-transfer.git
cd attendance-transfer
```

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

### Complete Workflow Example

**Scenario:** Tutorial class on Tuesday, 1:00 PM, 3 hours duration

#### Step 1: During Class
Students scan QR code that opens Microsoft Forms attendance

#### Step 2: After Class - Download Files
1. Go to Microsoft Forms → Responses → Open in Excel
2. Save as: `Attendance_Week5_Tutorial.xlsx`
3. Go to mytimetable.rmit.edu.vn → Download attendance template
4. Save as: `attendance_COMM2752_Tutorial.xls`

#### Step 3: Place Files in Folder
```
my-folder/
├── attendance_transfer.py
├── Attendance_Week5_Tutorial.xlsx
└── attendance_COMM2752_Tutorial.xls
```

#### Step 4: Run Script
```bash
python attendance_transfer.py --start_time 13:00 --duration 180
```

#### Step 5: Check Output
```
attendance_COMM2752_Tutorial_updated.xls  ← Import this to myTimetable
```

#### Step 6: Upload to myTimetable
1. Go to mytimetable.rmit.edu.vn
2. Navigate to your class attendance
3. Import `attendance_COMM2752_Tutorial_updated.xls`
4. Done! ✅

## 🔍 How It Works

### 1. Student ID Extraction

The script extracts student IDs from email addresses in the Forms responses:

```
Input (Forms):           Output (Extracted ID):
S4186054@rmit.edu.vn  →  4186054
s3992383@rmit.edu.vn  →  3992383  (case-insensitive)
4019025@rmit.edu.vn   →  4019025  (handles missing 'S')
```

### 2. QR Code Timestamp Processing

Microsoft Forms captures when students scan the QR code. The script uses the **completion time** to calculate attendance:

```
Forms Column: "Completion time"
Value: 2024-12-03 08:15:30
↓
Extracted: Student arrived at 08:15
```

### 3. Late Arrival Calculation

**Example Configuration:**
- Class start: 13:00
- Duration: 180 minutes (3 hours)
- Class end: 16:00

**Calculation Logic:**

| QR Code Scan Time | Arrival Status | Code | Minutes | Explanation |
|-------------------|----------------|------|---------|-------------|
| 13:00 or earlier | On time | Y | 180 | Full attendance |
| 13:15 | Late | Y | 165 | 15 minutes late (180 - 15) |
| 13:45 | Late | Y | 135 | 45 minutes late (180 - 45) |
| 14:30 | Very late | Y | 90 | 1.5 hours late (180 - 90) |
| 15:45 | Almost end | Y | 15 | 2h 45min late (180 - 165) |
| 16:00 or later | Missed class | N | 0 | Arrived after class ended |
| No QR scan | Absent | N | 0 | Didn't attend/scan QR code |

**Formula:**
```python
IF scan_time <= class_start:
    code = 'Y'
    minutes = full_duration
ELSE IF scan_time >= class_end:
    code = 'N'
    minutes = 0
ELSE:
    code = 'Y'
    minutes_late = (scan_time - class_start) in minutes
    minutes = duration - minutes_late
END IF
```

### 4. Date Format Conversion

Converts dates to match myTimetable format:

```
Microsoft Forms:  12/03/24 08:15:30 (MM/DD/YY HH:MM:SS)
↓
myTimetable:      3/12 (D/M - no leading zeros)
```

### 5. Absent Student Handling

Students who **did not scan the QR code** are automatically marked:
- **Code:** N (absent)
- **Minutes:** 0
- **Logic:** If student is in template but not in Forms responses

## 📂 File Structure

### Input Files (must be in same folder as script)

#### 1. Microsoft Forms Export (.xlsx)
- **Source:** Microsoft Forms → Responses → Open in Excel
- **Contains:** QR code scan data
- **Required columns:**
  - `Email`: Student email (S[ID]@rmit.edu.vn)
  - `Start time`: When form was opened
  - `Completion time`: When QR code was scanned ⭐ (used for attendance)

#### 2. myTimetable Template (.xls)
- **Source:** mytimetable.rmit.edu.vn → Download attendance template
- **Structure:**
  - Column 0: Student ID (numeric)
  - Date columns (e.g., 19/11, 26/11, 3/12) with sub-headers:
    - `Code`: Y (present) or N (absent)
    - `Minutes`: Minutes present in class

### Output File

- **Name:** `[original_template]_updated.xls`
- **Location:** Same folder as input files
- **Format:** Preserves myTimetable formatting (ready for import)
- **Usage:** Upload directly to mytimetable.rmit.edu.vn

## 💡 Examples

### Example 1: Regular Tutorial Class

**Context:** Weekly tutorial, students scan QR code upon arrival

**Files:**
```
attendance_transfer.py
Attendance_Week5_QRCode_Responses.xlsx  ← Microsoft Forms export
attendance_COMM2752_Template.xls        ← From myTimetable
```

**Command:**
```bash
python attendance_transfer.py --start_time 13:00 --duration 180
```

**Output:**
```
================================================================================
ATTENDANCE TRANSFER SCRIPT
================================================================================

Configuration:
  Class start time: 13:00
  Class duration: 180 minutes

Reading Microsoft Forms file: Attendance_Week5_QRCode_Responses.xlsx
  Loaded 18 records
  Extracted 18 valid student records

Processing attendance data...
  Updated student 3903858 for 3/12: Code=Y, Minutes=176  ← Arrived 4 min late
  Updated student 3911696 for 3/12: Code=Y, Minutes=177  ← Arrived 3 min late
  Updated student 4065603 for 3/12: Code=Y, Minutes=123  ← Arrived 57 min late
  ...

Total updates made: 18

Marking absent students...
  Marked student 3980573 as absent for 3/12: Code=N, Minutes=0  ← No QR scan
  Marked student 3978637 as absent for 3/12: Code=N, Minutes=0  ← No QR scan
  ...

Total absent students marked: 5

Output file: attendance_COMM2752_Template_updated.xls
```

**Result:**
- 18 students scanned QR code → Marked present with calculated minutes
- 5 students didn't scan → Marked absent
- Upload `attendance_COMM2752_Template_updated.xls` to myTimetable ✅

### Example 2: Morning Lab Session

**Files:**
```
Lab_Session_QR_Scans.xlsx    ← Microsoft Forms
attendance_COMP1752_Lab.xls  ← myTimetable template
```

**Command:**
```bash
python attendance_transfer.py -s 09:30 -d 120
```

**Output file:**
```
attendance_COMP1752_Lab_updated.xls  ← Upload to myTimetable
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

### System Requirements
- Works on Windows, macOS, and Linux
- Requires access to:
  - Microsoft Forms (for QR code attendance collection)
  - mytimetable.rmit.edu.vn (for template download/upload)

## 🔧 Troubleshooting

### Common Issues

**1. No .xlsx file found**
```
Error: No .xlsx file found in the current directory
```
**Solution:** Ensure Microsoft Forms export file is in the same folder

**2. No .xls file found**
```
Error: No .xls file found in the current directory
```
**Solution:** Download attendance template from mytimetable.rmit.edu.vn

**3. Date not found in template**
```
Warning: Date 3/12 not found in template for student 4186054
```
**Solution:** Ensure the Forms date matches a date column in myTimetable template

**4. Student not found in template**
```
Warning: Student 4186054 not found in template
```
**Solution:** Student scanned QR code but is not enrolled in myTimetable (check enrollment)

**5. Invalid time format**
```
Invalid start_time format: 1:00. Expected HH:MM (e.g., 13:00)
```
**Solution:** Use 24-hour format with leading zeros: `01:00` or `13:00`

### Verification Steps

After running the script:

1. **Check console output** for number of updates and warnings
2. **Open the `*_updated.xls` file** in Excel
3. **Verify a few students manually**:
   - Present students have Code=Y and minutes
   - Absent students have Code=N and minutes=0
4. **Test import to myTimetable** with a small file first

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### How to Contribute

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Dr. Huoston Rodrigues**
- Institution: RMIT Vietnam
- Email: huoston.rodriguesbatista@rmit.edu.vn
- GitHub: [@huoston](https://github.com/huoston)

## 🙏 Acknowledgments

- Developed for RMIT Vietnam to streamline attendance tracking workflow
- Integrates Microsoft Forms QR code attendance with myTimetable system
- Thanks to RMIT teaching staff for feedback and requirements
- Special thanks to the Python community for excellent libraries

## 📊 Version History

- **v1.3** (November 2025) - Current version
  - QR code timestamp processing from Microsoft Forms
  - Automatic late arrival minute calculation
  - Student ID extraction from email addresses
  - Date format conversion for myTimetable compatibility
  - Absent student automatic marking
  - Format preservation using xlutils
  - Full myTimetable integration workflow

## 🔗 Related Resources

- [Microsoft Forms](https://forms.office.com/) - QR code attendance collection
- [RMIT myTimetable](https://mytimetable.rmit.edu.vn/) - Attendance management system
- [pandas](https://pandas.pydata.org/) - Data manipulation library
- [xlutils](https://xlutils.readthedocs.io/) - Excel utilities for format preservation

## 📞 Support

For questions, issues, or feature requests:
- Open an issue on [GitHub Issues](https://github.com/huoston/attendance-transfer/issues)
- Email: huoston.rodriguesbatista@rmit.edu.vn

## ⭐ If This Helped You

If this script saved you time, please:
- Give it a star ⭐ on GitHub
- Share with colleagues who might find it useful
- Report issues or suggest improvements

---

**Made with ❤️ for RMIT Vietnam educators**

**Simplifying attendance tracking, one QR code at a time** 📱✅
