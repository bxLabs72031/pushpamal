name: Test Suite

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  test:
    runs-on: windows-latest
    # Alternatively: ubuntu-latest, macos-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.12'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install 'setuptools<60'
        pip install -e .

    - name: Run tests
      run: python test/test_pushpamal.py

    - name: Verify basic operation
      run: python -c "
import sys
sys.path.insert(0, 'C:/Users/BX/pushpamal')
from pushpamal_asm import assemble
from pushpamal_vm import run_pushpa
b = assemble('push 42 print halt')
assert run_pushpa(b) == 1, 'Basic operation failed'
print('Basic operation: PASS')
"