# Contributing to Attendance Transfer Script

First off, thank you for considering contributing to this project! 🎉

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Style Guidelines](#style-guidelines)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)

## 📜 Code of Conduct

This project adheres to a simple code of conduct:
- Be respectful and inclusive
- Be patient with newcomers
- Focus on what is best for the community
- Show empathy towards other community members

## 🤝 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

When creating a bug report, include:
- **Clear title** - Describe the issue concisely
- **Steps to reproduce** - Detailed steps to reproduce the problem
- **Expected behavior** - What you expected to happen
- **Actual behavior** - What actually happened
- **Environment details**:
  - Python version
  - Operating system
  - Package versions
- **Error messages** - Copy/paste any error messages
- **Sample files** - If possible, provide sample files (with sensitive data removed)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear title** describing the enhancement
- **Provide detailed description** of the suggested feature
- **Explain why** this enhancement would be useful
- **Include examples** of how it would work

### Your First Code Contribution

Unsure where to begin? Look for issues labeled:
- `good first issue` - Simple issues perfect for beginners
- `help wanted` - Issues where we need help

## 🛠️ Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/attendance-transfer.git
cd attendance-transfer
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

## 📝 Style Guidelines

### Python Code Style

Follow [PEP 8](https://pep8.org/) style guide:

```python
# Good
def calculate_attendance(completion_time, start_time, duration):
    """Calculate attendance code and minutes."""
    pass

# Bad
def calc_att(ct,st,d):
    pass
```

### Documentation

- **Docstrings** - All functions must have docstrings
- **Comments** - Explain WHY, not WHAT
- **Type hints** - Use type hints for function parameters

Example:
```python
def extract_student_id(email: str) -> Optional[str]:
    """
    Extract numeric student ID from email address.
    
    Args:
        email (str): Email in format S[ID]@rmit.edu.vn
        
    Returns:
        Optional[str]: Numeric student ID, or None if extraction fails
        
    Examples:
        >>> extract_student_id('S4186054@rmit.edu.vn')
        '4186054'
    """
    # Implementation
```

### Code Organization

- Keep functions focused on a single task
- Maximum line length: 100 characters
- Use meaningful variable names
- Group related functions together

## 💬 Commit Guidelines

### Commit Messages

Use clear, descriptive commit messages:

```bash
# Good
git commit -m "Fix: Correct absent student marking logic"
git commit -m "Add: Support for multiple date formats"
git commit -m "Docs: Update installation instructions"

# Bad
git commit -m "fixed stuff"
git commit -m "update"
```

### Commit Message Format

```
Type: Short description (50 chars or less)

Longer description if needed. Wrap at 72 characters.
Explain what and why, not how.

- Bullet points are okay
- Use present tense: "Add feature" not "Added feature"
```

### Commit Types

- `Fix:` - Bug fix
- `Add:` - New feature
- `Update:` - Update existing feature
- `Refactor:` - Code refactoring
- `Docs:` - Documentation changes
- `Test:` - Adding or updating tests
- `Style:` - Code style changes (formatting, etc.)

## 🔄 Pull Request Process

### Before Submitting

1. **Test your changes** thoroughly
2. **Update documentation** if needed
3. **Follow style guidelines**
4. **Add tests** if applicable
5. **Update CHANGELOG** (if we have one)

### Submitting Pull Request

1. **Push your branch** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Open Pull Request** on GitHub

3. **Fill in the template**:
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update
   
   ## Testing
   Describe how you tested
   
   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Documentation updated
   - [ ] Tests added/updated
   - [ ] No breaking changes
   ```

4. **Wait for review** - Be patient and responsive to feedback

### After Submitting

- Respond to review comments
- Make requested changes
- Keep your branch updated with main:
  ```bash
  git checkout main
  git pull upstream main
  git checkout your-branch
  git rebase main
  ```

## ✅ Checklist Before Submitting

- [ ] Code follows PEP 8 style
- [ ] All functions have docstrings
- [ ] Code has been tested
- [ ] No sensitive data in commits
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] No merge conflicts
- [ ] Branch is up to date with main

## 🧪 Testing

### Running Tests

```bash
python test_attendance.py
```

### Writing Tests

If adding new features, include tests:

```python
def test_student_id_extraction():
    """Test student ID extraction from various email formats."""
    assert extract_student_id('S4186054@rmit.edu.vn') == '4186054'
    assert extract_student_id('s3992383@rmit.edu.vn') == '3992383'
    assert extract_student_id('invalid') is None
```

## 📚 Additional Resources

- [Python Style Guide (PEP 8)](https://pep8.org/)
- [Git Documentation](https://git-scm.com/doc)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Writing Good Commit Messages](https://chris.beams.io/posts/git-commit/)

## ❓ Questions?

Feel free to:
- Open an issue with the `question` label
- Email: huoston.rodriguesbatista@rmit.edu.vn

## 🙏 Thank You!

Your contributions make this project better for everyone. We appreciate your time and effort! ⭐

---

**Happy Contributing! 🚀**
