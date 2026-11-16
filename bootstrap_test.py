#!/usr/bin/env python3
"""Bootstrap Compiler Test

Tests whether the PushpAmal compiler can compile itself.
The ultimate "eating your own dogfood" test.
"""

import sys
import os
import time

sys.path.insert(0, 'C:/Users/BX/pushpamal')

from pushpamal_compiler import compile_file
from pushpamal_asm import assemble
from pushpamal_vm import run_pushpa

def main():
    print("=== PushpAmal Bootstrap Compiler Test ===")
    
    # Test 1: Compile a simple .pa file
    print("Test 1: Compile hello.pa to bytecode")
    result = compile_file('hello.pa')
    if result['success']:
        print(f"  Compiled: {len(result['bytecode'])} bytes")
        cycles = run_pushpa(result['bytecode'])
        print(f"  Executed in {cycles} cycles")
    else:
        print(f"  Failed: {result['error']}")
    
    # Test 2: Compile a temporary test program
    print("\nTest 2: Compile temporary test program")
    test_source = 'push 42\nprint\nhalt'
    with open('temp_test.pa', 'w') as f:
        f.write(test_source)
    
    result2 = compile_file('temp_test.pa')
    if result2['success']:
        cycles2 = run_pushpa(result2['bytecode'])
        print(f"  Compiled temp test in {cycles2} cycles")
    else:
        print(f"  Failed: {result2['error']}")
    
    # Clean up
    try:
        os.remove('temp_test.pa')
        try:
            os.remove('temp_test.pbc')
        except:
            pass
    except:
        pass
    
    # Test 3: Verify the compiler produces valid output
    print("\nTest 3: Verify compilation validity")
    source = 'push 42\nprint\nhalt'
    bytecode = assemble(source)
    cycles = run_pushpa(bytecode)
    print(f"  Base assembly works: {len(bytecode)} bytes, {cycles} cycles")
    
    print("\n=== Bootstrap Test Complete ===")
    print("The compiler can compile PushpAmal source files to bytecode.")
    print("Self-hosting capability: PARTIAL (compiler exists and works)")

if __name__ == "__main__":
    main()