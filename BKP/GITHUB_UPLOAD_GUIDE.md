# How to Upload Your Project to GitHub

This guide will walk you through uploading your Attendance Transfer Script to GitHub for the first time.

## 📋 Prerequisites

Before you start, make sure you have:
- [ ] A GitHub account (create one at https://github.com/signup if you don't have one)
- [ ] Git installed on your computer
- [ ] All project files ready

## 🔧 Step 1: Install Git (if not already installed)

### Windows
1. Download Git from https://git-scm.com/download/win
2. Run the installer
3. Use default settings (just click "Next")

### Mac
```bash
brew install git
```
Or download from https://git-scm.com/download/mac

### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install git
```

### Verify Installation
```bash
git --version
```

## 👤 Step 2: Configure Git (First Time Only)

Open your terminal/command prompt and run:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@rmit.edu.vn"
```

Replace with your actual name and email.

## 🌐 Step 3: Create a GitHub Repository

1. **Go to GitHub:** https://github.com
2. **Sign in** to your account
3. **Click** the "+" icon in the top right corner
4. **Select** "New repository"
5. **Fill in the details:**
   - **Repository name:** `attendance-transfer` (or your preferred name)
   - **Description:** "Automate attendance data transfer from Microsoft Forms to Excel templates"
   - **Visibility:** Choose "Public" (recommended) or "Private"
   - **⚠️ IMPORTANT:** Do NOT check "Add a README file" (we already have one)
   - Do NOT add .gitignore (we already have one)
   - Do NOT add a license (we already have one)
6. **Click** "Create repository"

## 📁 Step 4: Prepare Your Local Files

### Organize Your Project Folder

Create a new folder with this structure:

```
attendance-transfer/
├── attendance_transfer.py
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
├── test_attendance.py (optional)
└── examples/ (optional)
    └── example_template.xls
```

### Files to Include:
- ✅ `attendance_transfer.py` - Main script
- ✅ `README.md` - Documentation (use README_GITHUB.md)
- ✅ `requirements.txt` - Dependencies
- ✅ `.gitignore` - Files to ignore
- ✅ `LICENSE` - License file
- ✅ `test_attendance.py` - Testing script (optional)

### Files to EXCLUDE (already in .gitignore):
- ❌ Actual attendance files (.xlsx, .xls)
- ❌ Any files with real student data
- ❌ `__pycache__/` folders
- ❌ Personal/sensitive data

## 💻 Step 5: Initialize Git Repository Locally

1. **Open Terminal/Command Prompt**
2. **Navigate to your project folder:**
   ```bash
   cd path/to/attendance-transfer
   ```

3. **Initialize Git:**
   ```bash
   git init
   ```

4. **Add all files:**
   ```bash
   git add .
   ```

5. **Check what will be committed:**
   ```bash
   git status
   ```
   Make sure no sensitive files are listed!

6. **Make your first commit:**
   ```bash
   git commit -m "Initial commit: Add attendance transfer script v1.3"
   ```

## 🚀 Step 6: Push to GitHub

After creating your repository on GitHub, you'll see a page with instructions. Follow these commands:

1. **Add the remote repository:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/attendance-transfer.git
   ```
   Replace `YOUR_USERNAME` with your actual GitHub username.

2. **Rename the branch to main (if needed):**
   ```bash
   git branch -M main
   ```

3. **Push your code:**
   ```bash
   git push -u origin main
   ```

4. **Enter your GitHub credentials** when prompted
   - Username: Your GitHub username
   - Password: Use a Personal Access Token (see below)

### Creating a Personal Access Token (PAT)

GitHub no longer accepts passwords for Git operations. You need a token:

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name: "Git Operations"
4. Select scopes: Check "repo"
5. Click "Generate token"
6. **⚠️ COPY THE TOKEN IMMEDIATELY** (you won't see it again!)
7. Use this token as your password when pushing

## ✅ Step 7: Verify Your Upload

1. Go to your repository: `https://github.com/YOUR_USERNAME/attendance-transfer`
2. You should see all your files
3. Check that README.md displays correctly on the main page

## 🎨 Step 8: Make Your README Look Better (Optional)

The README will automatically display on your repository's main page. GitHub will render:
- ✅ Markdown formatting
- ✅ Badges
- ✅ Code blocks
- ✅ Tables
- ✅ Links

## 📝 Step 9: Add Topics/Tags (Optional but Recommended)

1. Go to your repository
2. Click the gear icon ⚙️ next to "About"
3. Add topics like:
   - `python`
   - `attendance`
   - `automation`
   - `excel`
   - `microsoft-forms`
   - `education`
   - `rmit`
4. Save changes

## 🔄 Future Updates

When you make changes to your code:

1. **Add changed files:**
   ```bash
   git add .
   ```

2. **Commit changes:**
   ```bash
   git commit -m "Description of what you changed"
   ```

3. **Push to GitHub:**
   ```bash
   git push
   ```

### Example:
```bash
git add attendance_transfer.py
git commit -m "Fix: Improve absent student marking logic"
git push
```

## 🐛 Troubleshooting

### Error: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/attendance-transfer.git
```

### Error: "failed to push some refs"
```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### Can't push - Authentication failed
- Make sure you're using a Personal Access Token, not your password
- Generate a new token at https://github.com/settings/tokens

### Files not showing up
- Check `.gitignore` - might be excluding them
- Make sure you ran `git add .`

## 📚 Useful Git Commands

```bash
# Check repository status
git status

# View commit history
git log

# See what changed in files
git diff

# Undo changes to a file
git checkout -- filename

# Create a new branch
git checkout -b feature-name

# Switch branches
git checkout main
```

## 🎯 Best Practices

1. **Commit often** with clear messages
2. **Never commit** sensitive data (student info, passwords, API keys)
3. **Use .gitignore** to exclude data files
4. **Write clear commit messages**
   - Good: "Fix: Correct date format conversion for December dates"
   - Bad: "fixed bug"
5. **Keep README updated** as you add features

## 📞 Need Help?

- GitHub Documentation: https://docs.github.com
- Git Documentation: https://git-scm.com/doc
- GitHub Learning Lab: https://lab.github.com

## ✅ Checklist

Before publishing, make sure:
- [ ] No sensitive data in any files
- [ ] README.md is complete and clear
- [ ] requirements.txt lists all dependencies
- [ ] .gitignore excludes data files
- [ ] LICENSE file is included
- [ ] Script has been tested
- [ ] All files are committed
- [ ] Repository pushed to GitHub
- [ ] README displays correctly on GitHub

---

**Congratulations! Your project is now on GitHub! 🎉**

Share your repository URL:
`https://github.com/YOUR_USERNAME/attendance-transfer`
