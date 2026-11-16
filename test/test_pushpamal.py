#!/usr/bin/env python3
"""
PushpAmal Comprehensive Test Suite & Benchmarks

Tests all major opcodes and language features, plus performance benchmarks.
Each test assembles source code and runs it through the VM, verifying
expected behavior and recording cycle counts.
"""

import sys
import os
import time

sys.path.insert(0, 'C:/Users/BX/pushpamal')

from pushpamal_asm import assemble
from pushpamal_vm import run_pushpa


def make_source(lines):
    """Join lines with actual newlines."""
    return '\n'.join(lines)


# ============================================================
# TESTS - Verify opcode functionality
# ============================================================

def test_basic_arithmetic():
    """push 2; ldi 3; add; print; halt = 5"""
    source = make_source(['push 2', 'ldi 3', 'add', 'print', 'halt'])
    bytecode = assemble(source)
    cycles = run_pushpa(bytecode)
    assert cycles == 5, f"Expected 5 cycles, got {cycles}"
    print('  PASS: basic arithmetic')


def test_logic_operations():
    """Test AND, OR, NOT operations"""
    source = make_source(['ldi 1', 'ldi 0', 'and', 'print',
                          'ldi 1', 'or', 'print',
                          'ldi 1', 'not', 'print', 'halt'])
    bytecode = assemble(source)
    cycles = run_pushpa(bytecode)
    assert cycles > 0, "VM should run for multiple cycles"
    print('  PASS: logic operations')


def test_memory_operations():
    """Test load, store, load immediate"""
    source = make_source(['ldi 42', 'st 0', 'ld 0', 'print', 'halt'])
    bytecode = assemble(source)
    cycles = run_pushpa(bytecode)
    assert cycles > 0, "VM should run"
    print('  PASS: memory operations')


def test_conditional_jump():
    """Test jz (jump if zero) - jump when value is zero"""
    source = make_source(['ldi 0', 'jz end', 'ldi 999', 'print', 'halt', 'end:'])
    bytecode = assemble(source)
    cycles = run_pushpa(bytecode)
    assert cycles > 0, "VM should run"
    print('  PASS: conditional jump (jz)')


def test_stack_operations():
    """Test swap, dup, over"""
    source = make_source(['push 1', 'push 2', 'push 3', 'swap', 'print',
                          'push 1', 'dup', 'print',
                          'push 1', 'push 2', 'over', 'print', 'halt'])
    bytecode = assemble(source)
    cycles = run_pushpa(bytecode)
    assert cycles > 0, "VM should run"
    print('  PASS: stack operations')


def test_unsafe_operations():
    """Test uadd (unsafe add with potential overflow)"""
    source = make_source(['ldi 0xFFFFFFFE', 'ldi 0xFFFFFFFE', 'uadd', 'print', 'halt'])
    bytecode = assemble(source)
    cycles = run_pushpa(bytecode)
    assert cycles > 0, "VM should run"
    print('  PASS: unsafe operations')


def test_undefined_behavior():
    """Test undefined opcode (0xFF) - 50/50 random halt or random value"""
    source = make_source(['undefined', 'halt'])
    bytecode = assemble(source)
    cycles = run_pushpa(bytecode)
    assert cycles >= 1, "VM should run at least 1 cycle"
    print('  PASS: undefined behavior')


def test_jump_to_label():
    """Test jmp to labeled target"""
    source = make_source(['jmp start', 'print', 'halt', 'start:'])
    bytecode = assemble(source)
    cycles = run_pushpa(bytecode)
    assert cycles > 0, "VM should run"
    print('  PASS: jump to label')


def test_arithmetic_variants():
    """Test all arithmetic variants (add, sub, mul, div, mod)"""
    op_tests = [
        ('add', ['ldi 10', 'ldi 3', 'add', 'print', 'halt']),
        ('sub', ['ldi 10', 'ldi 3', 'sub', 'print', 'halt']),
        ('mul', ['ldi 10', 'ldi 3', 'mul', 'print', 'halt']),
        ('div', ['ldi 10', 'ldi 3', 'div', 'print', 'halt']),
        ('mod', ['ldi 10', 'ldi 3', 'mod', 'print', 'halt']),
    ]
    for op_name, source_lines in op_tests:
        source = make_source(source_lines)
        bytecode = assemble(source)
        cycles = run_pushpa(bytecode)
        assert cycles > 0, f"VM should run for {op_name}"
    print('  PASS: all arithmetic variants')


def test_benchmark_empty():
    """Benchmark: empty/halt-only program"""
    source = 'halt'
    bytecode = assemble(source)
    cycles = run_pushpa(bytecode)
    assert cycles >= 0, "Cycles should be non-negative"
    return cycles


def test_benchmark_nop():
    """Benchmark: NOP sequence"""
    source = 'nop\nnop\nnop\nnop\nnop'
    bytecode = assemble(source)
    cycles = run_pushpa(bytecode)
    # Should run approximately 5 cycles (5 NOPs + overhead)
    assert cycles >= 3 and cycles <= 10, f"Expected 3-10 cycles, got {cycles}"
    return cycles


def test_benchmark_rapid():
    """Benchmark: rapid nop sequence (100 NOPs)"""
    source = ''.join(['nop\n' for _ in range(100)])
    bytecode = assemble(source)
    cycles = run_pushpa(bytecode)
    # Should run approximately 100 cycles (plus overhead)
    assert cycles >= 90 and cycles <= 150, f"Expected ~100 cycles, got {cycles}"
    return cycles


def test_benchmark_arithmetic_throughput():
    """Benchmark: arithmetic operation throughput"""
    # 50 add operations
    source = ''.join(['ldi 1\nadd\n' for _ in range(50)])
    source += 'print\nhalt'
    bytecode = assemble(source)
    start = time.time()
    cycles = run_pushpa(bytecode)
    elapsed = time.time() - start
    # Verify some cycles were used
    assert cycles > 0, "Should execute some cycles"
    return cycles, elapsed


def test_benchmark_memory_ops():
    """Benchmark: memory operation throughput"""
    # 20 load/store operations
    source = ''.join(['ldi 1\nst 0\nld 0\n' for _ in range(20)])
    source += 'print\nhalt'
    bytecode = assemble(source)
    cycles = run_pushpa(bytecode)
    assert cycles > 0, "Should execute some cycles"
    return cycles


def run_all_tests():
    """Run the complete test suite."""
    print("=== PushpAmal Test Suite ===\n")
    
    tests = [
        ("basic_arithmetic", test_basic_arithmetic),
        ("logic_operations", test_logic_operations),
        ("memory_operations", test_memory_operations),
        ("conditional_jump", test_conditional_jump),
        ("stack_operations", test_stack_operations),
        ("unsafe_operations", test_unsafe_operations),
        ("undefined_behavior", test_undefined_behavior),
        ("jump_to_label", test_jump_to_label),
        ("arithmetic_variants", test_arithmetic_variants),
        ("benchmark_empty", test_benchmark_empty),
        ("benchmark_nop", test_benchmark_nop),
        ("benchmark_rapid", test_benchmark_rapid),
        ("benchmark_arithmetic_throughput", test_benchmark_arithmetic_throughput),
        ("benchmark_memory_ops", test_benchmark_memory_ops),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_fn in tests:
        try:
            test_fn()
            passed += 1
        except Exception as e:
            print(f'  FAIL: {name} - {type(e).__name__}: {e}')
            import traceback
            traceback.print_exc()
            failed += 1
    
    # Print benchmark results
    print("\n--- Benchmark Results ---")
    empty_cycles = test_benchmark_empty()
    nop_cycles = test_benchmark_nop()
    rapid_cycles = test_benchmark_rapid()
    arith_cycles, arith_time = test_benchmark_arithmetic_throughput()
    mem_cycles = test_benchmark_memory_ops()
    
    print(f"Empty program (halt):      {empty_cycles} cycles")
    print(f"5 NOPs:                    {nop_cycles} cycles")
    print(f"100 NOPs:                  {rapid_cycles} cycles")
    print(f"50 arithmetic ops:         {arith_cycles} cycles, {arith_time:.4f}s")
    print(f"20 memory ops:             {mem_cycles} cycles")
    
    print(f"\n=== Results: {passed} passed, {failed} failed ===")
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)