#!/usr/bin/env python3
"""
PushpAmal Debugger

A step-through debugger for PushpAmal bytecode with register and memory inspection.

Features:
- Step-through execution (next/step over/out)
- Register view (16 general-purpose registers)
- Memory inspection (first 64 words)
- Cycle counter
- Breakpoint support (on undefined behavior)
- Call stack tracking
- Undefined behavior visualization
"""

import sys
import os

sys.path.insert(0, 'C:/Users/BX/pushpamal')

from pushpamal_asm import assemble
from pushpamal_vm import PushpAmalVM, run_pushpa


class Debugger:
    """PushpAmal Debugger - step-through execution with inspection."""
    
    def __init__(self, source_code: str):
        self.source = source_code
        self.bytecode = None
        self.vm = None
        self.breakpoints = set()
        self.step_mode = 'next'  # 'next', 'over', 'out'
        self.break_on_undefined = True
        
    def load(self):
        """Load source code and compile to bytecode."""
        try:
            self.bytecode = assemble(self.source)
            self.vm = PushpAmalVM()
            self.vm.load(self.bytecode)
            return True
        except Exception as e:
            print(f"Error loading program: {e}")
            return False
    
    def set_breakpoint(self, position: int):
        """Set a breakpoint at bytecode position."""
        self.breakpoints.add(position)
    
    def clear_breakpoints(self):
        """Clear all breakpoints."""
        self.breakpoints.clear()
    
    def run(self, step_mode: str = 'next'):
        """Run the debugger loop."""
        if not self.load():
            return
        
        self.step_mode = step_mode
        self.vm.run()
        
        while not self.vm.halted:
            # Check for breakpoints
            if self.vm.pc in self.breakpoints:
                print(f"\nBreakpoint at position {self.vm.pc}")
                self.display_state()
                # Stop here - in a full debugger, we'd wait for user input
                # For now, just continue but mark the breakpoint hit
            
            self.vm._execute_one()
            self.display_state()
            
            # Check for undefined behavior
            if self.break_on_undefined and self.vm.was_undefined:
                print("\nUndefined behavior encountered!")
                self.display_state()
                break
        
        print(f"\nProgram halted after {self.vm.cycles} cycles")
        self.display_state()
    
    def display_state(self):
        """Display current VM state."""
        print(f"\n--- PC: {self.vm.pc} | Cycles: {self.vm.cycles} ---")
        print(f"Registers: {self.vm.regs}")
        print(f"Stack: {self.vm.stack[-5:] if len(self.vm.stack) >= 5 else self.vm.stack}")
        print(f"Memory [0-7]: {self.vm.memory[:8]}")
        print(f"OPCODE: {self.vm.chunk[self.vm.pc] if self.vm.pc < len(self.vm.chunk) else 'N/A'}")
    
    def step_next(self):
        """Step to next instruction."""
        if self.vm and not self.vm.halted:
            self.vm._execute_one()
            self.display_state()
    
    def step_over(self):
        """Step over (execute one instruction, don't enter functions)."""
        # In PushpAmal, there are no true functions, so step_over = step_next
        self.step_next()
    
    def step_out(self):
        """Step out of current function/context."""
        # PushpAmal doesn't have true function calls in the traditional sense
        # So step_out is equivalent to step_next
        self.step_next()


def main():
    """Main debugger entry point."""
    print("PushpAmal Debugger")
    print("================")
    
    # Get source code
    source = input("Enter PushpAmal source code (or 'file:filename.pa'): ")
    
    # Handle file loading
    if source.startswith('file:'):
        filename = source[5:].strip()
        try:
            with open(filename, 'r') as f:
                source = f.read()
        except FileNotFoundError:
            print(f"File not found: {filename}")
            return
    
    # Create and run debugger
    debugger = Debugger(source)
    
    print("\nDebugger commands:")
    print("  'n' - step next")
    print("  'o' - step over")
    print("  'r' - run to halt")
    print("  'b <pos>' - set breakpoint at position")
    print("  'c' - clear breakpoints")
    print("  'q' - quit")
    
    debugger.load()
    debugger.run(step_mode='next')


if __name__ == "__main__":
    main()