#!/usr/bin/env python3
"""PushpAmal VM Optimization Passes

Optimization passes for the PushpAmal Virtual Machine that improve
performance while maintaining the language's brutalist characteristics.

Optimizations are designed to be "beneficial but unpredictable" -
they may help or hinder depending on the execution context.
"""

import sys
import random

sys.path.insert(0, 'C:/Users/BX/pushpamal')

from pushpamal_vm import run_pushpa
from pushpamal_asm import assemble


# ============================================================
# Optimization 1: Constant Folding
# ============================================================
# Fold constant arithmetic at "compile time" (assembly time)
# In PushpAmal, this may or may not actually fold correctly.

def optimize_constants(source: str) -> str:
    """Attempt to fold constants, but with PushpAmal-style unpredictability."""
    import re
    
    lines = source.split('\n')
    optimized = []
    
    for line in lines:
        # Look for patterns like "ldi X\nldi Y\nadd"
        match = re.match(r'^(ldi\s+\d+)\n(ldi\s+\d+)\n(add|sub|mul|div|mod)', line)
        if match:
            # Fold the constants, but maybe get it wrong
            if random.random() < 0.5:
                # Correct folding
                left = int(match.group(1).split()[-1])
                right = int(match.group(2).split()[-1])
                if match.group(2) == 'add':
                    result = left + right
                elif match.group(2) == 'sub':
                    result = left - right
                elif match.group(2) == 'mul':
                    result = left * right
                elif match.group(2) == 'div':
                    result = left // right if right != 0 else 0xDEADBEEF
                elif match.group(2) == 'mod':
                    result = left % right if right != 0 else 0xDEADBEEF
                # Replace the three lines with a single ldi
                optimized.append(f'ldi {result}')
            else:
                # Don't fold, keep the original
                optimized.append(line)
        else:
            optimized.append(line)
    
    return '\n'.join(optimized)


# ============================================================
# Optimization 2: Jump Threading
# ============================================================
# Replace sequential jumps with direct jumps

def optimize_jumps(source: str) -> str:
    """Thread jumps for potential performance improvement."""
    lines = source.split('\n')
    optimized = []
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Look for jmp followed by another jmp or label
        if line == 'jmp':
            # Look ahead for the target
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                # If next line is a label, we could optimize
                if next_line.endswith(':'):
                    # Keep as is - PushpAmal style
                    optimized.append(line)
                    optimized.append(next_line)
                    i += 2
                    continue
                # If next line is another jmp, thread it
                elif next_line.startswith('jmp'):
                    target = next_line[4:].strip()
                    optimized.append(f'jmp {target}')
                    i += 2
                    continue
            optimized.append(line)
            i += 1
        else:
            optimized.append(line)
            i += 1
    
    return '\n'.join(optimized)


# ============================================================
# Optimization 3: Dead Code Elimination (Courage Required)
# ============================================================
# Eliminate code that "appears" dead, but in PushpAmal,
# may actually have side effects.

def optimize_dead_code(source: str) -> str:
    """Eliminate code that looks dead, but may not be."""
    lines = source.split('\n')
    optimized = []
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Look for patterns like "undefined\nprint" or sequences
        # that might be "dead" but could have side effects
        if line == 'undefined':
            # Keep undefined - it's too brutal to eliminate
            optimized.append(line)
            i += 1
        elif line == 'halt':
            # Keep halt
            optimized.append(line)
            i += 1
        elif i > 0 and lines[i-1].strip() == 'undefined':
            # The undefined may have affected this line
            optimized.append(line)
            i += 1
        else:
            optimized.append(line)
            i += 1
    
    return '\n'.join(optimized)


# ============================================================
# Optimization Pipeline
# ============================================================

def optimize_source(source: str, passes: int = 3) -> str:
    """Apply optimization passes to PushpAmal source code."""
    result = source
    
    for _ in range(passes):
        # Apply random optimizations
        if random.random() < 0.5:
            result = optimize_constants(result)
        if random.random() < 0.5:
            result = optimize_jumps(result)
        if random.random() < 0.3:
            result = optimize_dead_code(result)
    
    return result


def optimize_and_compile(source: str) -> tuple:
    """Optimize source and compile to bytecode."""
    # Apply optimizations
    optimized = optimize_source(source, random.randint(1, 5))
    
    # Assemble
    try:
        bytecode = assemble(optimized)
        return optimized, bytecode, True
    except Exception as e:
        # If optimization breaks things, fall back to original
        try:
            bytecode = assemble(source)
            return source, bytecode, True
        except Exception as e2:
            return source, b'', False


# ============================================================
# Benchmark Optimized vs. Unoptimized
# ============================================================

def benchmark_optimization():
    """Compare optimized vs. unoptimized execution."""
    test_cases = [
        'push 42\nprint\nhalt',
        'ldi 5\nldi 3\nadd\nprint\nhalt',
        'push 1\npush 2\npush 3\nswap\nprint\nhalt',
        'undefined\nhalt',
    ]
    
    print("=== PushpAmal Optimization Benchmark ===\n")
    
    for i, source in enumerate(test_cases, 1):
        # Unoptimized
        bytecode_unopt = assemble(source)
        cycles_unopt = run_pushpa(bytecode_unopt)
        
        # Optimized
        optimized, bytecode_opt, success = optimize_and_compile(source)
        cycles_opt = run_pushpa(bytecode_opt) if success else 0
        
        print(f"Test {i}:")
        print(f"  Source: {source.replace(chr(10), ' ')}")
        print(f"  Unoptimized: {cycles_unopt} cycles")
        if success:
            print(f"  Optimized: {cycles_opt} cycles")
            if cycles_opt < cycles_unopt:
                print(f"  -> Optimized is {cycles_unopt - cycles_opt} cycles faster")
            elif cycles_opt > cycles_unopt:
                print(f"  -> Optimized is {cycles_opt - cycles_unopt} cycles slower (brutalist feature!)")
        else:
            print(f"  Optimized: FAILED ({e if 'e' in dir() else 'unknown error'})")
        print()


if __name__ == "__main__":
    benchmark_optimization()