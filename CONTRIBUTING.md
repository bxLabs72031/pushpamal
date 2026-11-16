# Contributing to PushpAmal

Welcome! We love Pull Requests. Please take a moment to review this guide to understand how we work.

## 🛣️ Project Roadmap
See the [Wiki](https://github.com/bxqbit/pushpamal/wiki) for the full roadmap, or check the [4-Week Learning Roadmap](https://github.com/bxqbit/pushpamal/blob/main/four_week_roadmap.py) inside the project.

## 💡 Ways to Contribute

### 1. 🐛 Bug Reports
- Use the [issue tracker](https://github.com/bxqbit/pushpamal/issues)
- Include: PushpAmal version, OS, steps to reproduce, expected vs actual behavior
- Minimum: Code snippet that demonstrates the issue

### 2. 💡 Feature Requests
- Check existing issues first
- Describe: Use case, why it matters, ideal implementation
- Label: `enhancement` or `feature request`

### 3. 📝 Documentation Improvements
- Tutorial improvements (PUSHAMAL_TUTORIAL.md)
- Exercise solutions and explanations
- Example program additions
- Language comparison tables
- Tutorial videoscripts

### 4. 🔧 Code Contributions
- New example programs (`examples/new/`)
- Debugger enhancements
- Standard library modules (math, io, string, dict)
- Test suite additions
- Bug fixes
- Compiler optimizations

### 5. 📚 Documentation
- Tutorial section additions
- Exercise answer keys
- Language comparison tables
- Getting-started guides
- Video script contributions

### 6. 🎮 REPL Improvements
- Command persistence (save/load history)
- Graphic mode enhancements
- New command additions
- Error message improvements

### 6. 📦 Packaging Improvements
- pip install workflow fixes
- Better setuptools compatibility
- Universal wheel creation
- Packaging workflow documentation

## 🛠️ Development Setup

### Prerequisites
- Python 3.8+
- Git
- `pip install -e .` or `python setup.py develop`

### Local Development
```bash
# 1. Fork the repository
# 2. Clone your fork
git clone https://github.com/your-username/pushpamal.git
cd pushpamal

# 3. Create a branch
git checkout -b my-feature

# 4. Make your changes
# 5. Test your changes
python -c "from pushpamal_asm import assemble; from pushpamal_vm import run_pushpa"

# 6. Commit your changes
git commit -m "feat: add something awesome"

# 7. Push to your fork
git push origin my-feature

# 8. Open a Pull Request
#    - Fill the PR template
#    - Link to any issues
#    - Explain what your change does
```

### Development Commands
```bash
# Run the test suite
python test/test_pushpamal.py

# Run the bootstrap test
python bootstrap_test.py

# Launch the REPL
python pushpamal/repl.py

# Verify basic operation
python -c "import sys; sys.path.insert(0, 'C:/Users/BX/pushpamal'); from pushpamal_asm import assemble; from pushpamal_vm import run_pushpa; b=assemble('push 42 print halt'); print(f'Ran in {run_pushpa(b)} cycles')"
```

## 🐛 Bug Report Guidelines

### Good Bug Report
```
Title: Brief description of the issue

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What should happen?

## Actual Behavior
What actually happens?

## Environment
- PushpAmal version: X.Y.Z
- OS: Windows/macOS/Linux
- Python version: X.Y.Z
- Python path: C:/Users/BX/pushpamal
```

## 📬 Pull Request Guidelines

### Title Format
```
feat: add new example program
fix: fix undefined opcode crash
docs: add exercise solution
style: format REPL output
```

### PR Template Checklist
- [ ] Discussion happened in an issue (or this is a small fix)
- [ ] Code follows the project's style
- [ ] Tests pass (`python test/test_pushpamal.py`)
- [ ] New examples include verification (`run_pushpa(assemble(...))`)
- [ ] Documentation updated (if applicable)
- [ ] PR title follows format above

### Review Process
1. Maintainer will review within 7 days
2. May request changes or clarifications
3. Will merge once all checks pass
4. Will tag release if significant

## 🌟 Quick Start for Contributors

### Add a Test Case (5 minutes)
```python
python -c "
import sys
sys.path.insert(0, 'C:/Users/BX/pushpamal')
from pushpamal_asm import assemble
from pushpamal_vm import run_pushpa

# Test: push 99 print halt should work
b = assemble('push 99 print halt')
c = run_pushpa(b)
assert c == 1, 'Expected 1 cycle'
print('Test passed: push 99 print halt ->', c, 'cycles')
"
```

### Add an Example Program
1. Create `examples/new/my_example.pa`
2. Verify it works:
   ```python
   python -c "
   from pushpamal_asm import assemble
   from pushpamal_vm import run_pushpa
   with open('my_example.pa', 'r') as f:
       source = f.read()
   bc = assemble(source)
   cy = run_pushpa(bc)
   print(f'✅ {bc} bytes, {cy} cycles')
   "
   ```
3. Add description to the tutorial

### Write an Exercise Solution
1. Pick an exercise from the tutorial
2. Write the PushpAmal solution
3. Document the step-by-step execution
4. Submit as a documentation PR

## 📬 Questions?
- Open an issue for general questions
- Check the [Wiki](https://github.com/bxqbit/pushpamal/wiki) for detailed guides
- Email: bxqbit@users.noreply.github.com

---

*Thank you for contributing to PushpAmal! Your help makes this educational language better for everyone.*