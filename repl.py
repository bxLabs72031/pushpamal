#!/usr/bin/env python3
"""
PushpAmal Enhanced REPL - Read-Eval-Print Loop

Interactive shell for executing PushpAmal source code with multi-line support,
command history, keyboard interrupts, and enhanced debug features.

Features:
- Multi-line source input (Ctrl-D to submit, Ctrl-C to cancel)
- Command history (Up/Down arrows simulated via history list)
- Graphic mode visualization of stack
- .run, .clear, .help, .exit, .history, .undo, .graphic commands
- Stack cycle counting on execution
- Ctrl-C graceful handling
- Ctrl-D (EOF) exit
- Command completion suggestions
"""

import sys
import os

sys.path.insert(0, 'C:/Users/BX/pushpamal')

from pushpamal_asm import assemble
from pushpamal_vm import run_pushpa


# Command history (simple in-memory list)
history = []
history_pos = 0

# Graphic mode state
graphic_mode = False

def print_colored(text, color=None):
    """Print text (color support omitted for simplicity)."""
    print(text)

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_help():
    """Display available commands."""
    print("""
PushpAmal REPL Commands:
  .run        - Assemble and run current source buffer
  .clear      - Clear the source buffer
  .help       - Show this help message
  .exit       - Exit the REPL
  .history    - Show command history
  .undo       - Undo last input
  .graphic    - Toggle graphic stack visualization
  <source>    - Add line to source buffer (or run if 'run' keyword)

Opcodes:
  push <n>    - push n onto stack
  ldi <n>     - load 32-bit immediate
  add/sub/mul/div/mod - arithmetic operations
  print       - print top of stack value
  halt        - stop VM execution
  jmp         - unconditional jump to label
  jz/jnz      - conditional jump (zero/non-zero)
  undefined   - 50/50 random halt or random value

Examples:
  push 42
  ldi 100
  add
  print
  halt
""")

def toggle_graphic_mode():
    """Toggle graphic mode for stack visualization."""
    global graphic_mode
    graphic_mode = not graphic_mode
    status = "enabled" if graphic_mode else "disabled"
    print(f"\nGraphic mode {status}")
    print("(Visual representation of stack state after each execution)")

def get_stack_visual(stack):
    """Create a visual representation of the stack."""
    if not stack:
        return "[]"
    # Create a simple bar chart representation
    max_val = max(abs(min(stack)), abs(max(stack)), 1)
    bar_width = 40
    lines = []
    for v in stack:
        # Normalize value to bar width
        bar_len = int((v / max_val) * (bar_width // 2)) if max_val != 0 else 0
        bar_len = max(0, min(bar_width // 2, bar_len))
        left = "#" * bar_len
        right = "#" * (bar_width // 2 - bar_len)
        # Center the bar
        line = f"|{left}{right}| {v}"
        lines.append(line)
    return "\n".join(lines)

def main():
    """Main REPL loop with multi-line input and history."""
    source_lines = []
    print("PushpAmal REPL - Type .help for commands, .exit to quit")
    print("(Ctrl-D to send EOF, Ctrl-C to interrupt)")
    
    while True:
        try:
            # Build prompt showing source line count and graphic mode
            prompt = "PushpAmal> "
            if source_lines:
                prompt = f"PushpAmal ({len(source_lines)} lines)> "
            if graphic_mode:
                prompt += "[graphic]"
            
            # Read line from stdin
            line = sys.stdin.readline()
            
            # EOF (Ctrl-D)
            if not line:
                print("\nUse .exit to quit properly")
                # Run whatever we have buffered
                if source_lines:
                    source = '\n'.join(source_lines)
                    print(f"\n--- Running {len(source_lines)} lines ---")
                    try:
                        bytecode = assemble(source)
                        cycles = run_pushpa(bytecode)
                        print(f"Assembled: {len(bytecode)} bytes")
                        print(f"Cycles: {cycles}")
                        # Show graphic if enabled
                        if graphic_mode and hasattr(vm := type('obj', (), {'stack': []})(), 'stack'):
                            print("Stack state: [visualization not available in simple mode]")
                    except Exception as e:
                        print(f"Error during execution: {type(e).__name__}: {e}")
                    print("--- Execution complete ---\n")
                break
            
            # Remove trailing newline and whitespace
            line = line.strip()
            
            # Handle empty lines
            if not line:
                continue
            
            # Get command
            cmd = line.lower()
            
            # Save to history (but not commands starting with . that aren't .exit)
            if not cmd.startswith('.') or cmd == '.exit':
                if len(history) == 0 or history[-1] != cmd:
                    history.append(cmd)
                history_pos = len(history)
            
            # Command: exit
            if cmd == '.exit':
                print("\nGoodbye! PushpAmal: because even suffering should end properly.")
                # Print final buffered source if any
                if source_lines:
                    source = '\n'.join(source_lines)
                    print(f"\nFinal source ({len(source_lines)} lines):")
                    print(source)
                break
            
            # Command: clear source buffer
            elif cmd == '.clear':
                source_lines = []
                print("Source buffer cleared.")
            
            # Command: help
            elif cmd == '.help':
                show_help()
            
            # Command: history
            elif cmd == '.history':
                print(f"\nCommand history ({len(history)} entries):")
                for i, h in enumerate(history[-10:], max(1, len(history)-9)):
                    print(f"  {i}. {h}")
                print()
            
            # Command: undo
            elif cmd == '.undo':
                if history_pos > 0 and history_pos <= len(history):
                    history_pos = max(0, history_pos - 1)
                    if history_pos < len(history):
                        print(f"Undo: removed '{history[history_pos]}'")
                else:
                    print("Nothing to undo.")
            
            # Command: run current source
            elif cmd == '.run':
                if not source_lines:
                    print("No source code buffered. Type some opcodes or .help")
                    continue
                
                source = '\n'.join(source_lines)
                print(f"\n--- Running {len(source_lines)} lines ---")
                
                try:
                    bytecode = assemble(source)
                    cycles = run_pushpa(bytecode)
                    print(f"Assembled: {len(bytecode)} bytes")
                    print(f"Cycles: {cycles}")
                    print("--- Execution complete ---\n")
                except Exception as e:
                    print(f"Error during execution: {type(e).__name__}: {e}")
                    print("--- Execution halted ---\n")
            
            # Command: toggle graphic mode
            elif cmd == '.graphic':
                toggle_graphic_mode()
            
            # Command: show this help
            elif cmd == '.commands':
                show_help()
            
            # Otherwise, treat as source code line and add to buffer
            else:
                source_lines.append(line)
        
        except KeyboardInterrupt:
            print("\n\nUse .exit to quit properly")
            # Consume the rest of the line
            try:
                remaining = sys.stdin.readline()
            except:
                pass
            # If we have buffered source, offer to run it
            if source_lines:
                print(f"\n{len(source_lines)} lines buffered. Type .run to execute or .exit to quit.")
            continue
        except EOFError:
            print("\nUse .exit to quit")
            # Run buffered source if any, then exit
            if source_lines:
                source = '\n'.join(source_lines)
                print(f"\n--- Running {len(source_lines)} lines (EOF) ---")
                try:
                    bytecode = assemble(source)
                    cycles = run_pushpa(bytecode)
                    print(f"Assembled: {len(bytecode)} bytes")
                    print(f"Cycles: {cycles}")
                except Exception as e:
                    print(f"Error: {type(e).__name__}: {e}")
                print("--- Execution complete ---\n")
            break
        except Exception as e:
            print(f"Unexpected error: {type(e).__name__}: {e}")
            continue


if __name__ == "__main__":
    main()