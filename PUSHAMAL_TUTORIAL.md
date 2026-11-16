# PushpAmal Tutorial: From Beginner to Brutat

## Table of Contents
1. [Getting Started](#getting-started)
2. [Hello World](#hello-world)
3. [Basic Opcodes](#basic-opcodes)
4. [Control Flow](#control-flow)
5. [Memory Management](#memory-management)
6. [Undefined Behavior](#undefined-behavior)
7. [Standard Library](#standard-library)
8. [Advanced Features](#advanced-features)
9. [Debugging](#debugging)
10. [FAQ](#faq)

---

## 1. Getting Started

### Installation
PushpAmal comes as a single-package Python installation. No pip install needed - just ensure `pushpamal` is in your Python path.

```bash
# Test installation
python -c "from pushpamal_asm import assemble; from pushpamal_vm import run_pushpa"
print("PushpAmal is ready!")
```

### Hello World
Your first PushpAmal program:

```pushpamal
# push 72 = 'H', push 101 = 'e', push 108 = 'l', push 108 = 'l', 
# push 111 = 'o', push 32 = ' ', push 87 = 'W', push 111 = 'o',
# push 114 = 'r', push 108 = 'l', push 100 = 'd', push 33 = '!',
# push 10 = newline, print, halt
push 72
push 101
push 108
push 108
push 111
push 32
push 87
push 111
push 114
push 108
push 100
push 33
push 10
print
halt
```

**Assembly + Execution:**
```bash
python -c "
from pushpamal_asm import assemble
from pushpamal_vm import run_pushpa

source = '''push 72
push 101
push 108
push 108
push 111
push 32
push 87
push 111
push 114
push 108
push 100
push 33
push 10
print
halt'''

bytecode = assemble(source)
cycles = run_pushpa(bytecode)
print(f'Hello World: {len(bytecode)} bytes, {cycles} cycles')
"
```

**Expected Output:** `Hello, World!` printed to console (if the VM doesn't halt unexpectedly).

---

## 2. Basic Opcodes

PushpAmal has over 80 opcodes. Here are the most fundamental ones:

| Opcode | Hex | Description |
|--------|-----|-------------|
| `halt` | `0x00` | Stop execution |
| `nop` | `0x01` | No operation |
| `push <n>` | `0x20`-`0xFF` | Push immediate value n onto stack |
| `ldi <n>` | `0x22` | Load 32-bit immediate n onto stack |
| `add` | `0x30` | Add top two stack values |
| `sub` | `0x31` | Subtract second from first |
| `mul` | `0x32` | Multiply top two values |
| `div` | `0x33` | Divide second into first |
| `mod` | `0x34` | Modulo remainder |
| `print` | `0x50` | Print top of stack as integer (ASCII) |
| `halt` | `0x00` | Stop VM execution |

### Basic Arithmetic Test
```pushpamal
# 2 + 3 = 5
push 2
ldi 3
add
print
halt
```

**Execution:** 5 cycles, prints `5` (as ASCII character 5 = ENQ control code).

### Unsafe Operations
PushpAmal includes "unsafe" arithmetic opcodes that may overflow unpredictably:

```pushpamal
# unsigned add - may overflow
ldi 0xFFFFFFFE
ldi 0xFFFFFFFE
uadd
print
halt
```

**Note:** The result depends on whether overflow wraps or not - this is part of PushpAmal's brutalist charm.

---

## 3. Control Flow

### Conditional Jumps
```pushamal
# Jump if zero (jz): if top of stack is 0, jump to label 'end'
ldi 0
jz end
ldi 999
print
halt
end:
```

### Unconditional Jump
```pushamal
# jmp: always jump to label
jmp start
print
halt
start:
```

### Conditional Non-Zero
```pushamal
# jnz: jump if top of stack is NOT zero
ldi 1
jnz print_it
print "not zero"
halt
print_it:
print "was zero"
halt
```

### Loop Example (Fibonacci-like)
```pushamal
# Simple counter loop
push 0        ; counter = 0
counter_label:
push 10       ; limit = 10
jz done       ; if counter == 10, done
print         ; print counter
add           ; counter = counter + 1
jmp counter_label
done:
halt
```

---

## 3. Memory Management

PushpAmal's "Pushpa Heap" is uniquely designed:

### alloc/free
```pushamal
# Allocate 100 bytes on the Pushpa heap
alloc 100

# "Free" memory (advisory only - memory is never actually freed)
free 100
```

**Key Insight:** In PushpAmal, `free` is advisory only. Memory is never actually deallocated. The heap is simultaneously reference-counted, garbage-collected, and manually managed. The rules for which apply when are determined by... reading tea leaves at compile time.

### new/dispose
```pushamal
# Allocate and zero-initialize a new buffer
new 50

# dispose - advisory only, memory not actually freed
dispose 50
```

### Memory Leak Demo
```pushamal
# Demonstrate that "free" doesn't actually free
alloc 100
print "allocated 100 bytes"
free 100
print "called free (but memory still exists)"
# The buffer is still allocated - free is only advisory
```

---

## 4. Undefined Behavior

The `0xFF` opcode is PushpAmal's signature feature:

```pushamal
# undefined - 50/50 chance
undefined
halt
```

**Behavior:**
- 50% probability: push a random 32-bit value onto the stack, execution continues
- 50% probability: halt the VM immediately

### undefined Demo
```pushamal
# Run this multiple times to see both behaviors
undefined
print "if you see this, the VM didn't halt"
halt
```

**Note:** Each execution may produce different results - this is intentional.

### Safe Undefined Avoidance
While you can't truly "safe-ify" undefined behavior, you can:
1. Wrap undefined-prone code in try-catch (if available)
2. Check values before operations that may trigger UB
3. Accept that PushpAmal's entire design philosophy embraces uncertainty

---

## 5. Standard Library

PushpAmal includes a standard library with... interesting functions.

### Math Module
```python
from pushpamal_std.math import add, sub, mul, div, mod, abs_val, factorial, sqrt, pow, clamp

# div by zero returns 0xDEADBEEF (the Pushpa magic value)
result = div(10, 0)  # returns 0xDEADBEEF

# factorial may cause stack issues for large inputs
result = factorial(5)  # = 120, but factorial(1000) might halt the VM
```

### IO Module
```python
from pushpamal_std.io import print_ as io_print, input_ as io_input

io_print("Hello, PushpAmal!")  # May or may not print
user_input = io_input("Enter something: ")  # May return empty string
```

### String Module
```python
from pushpamal_std.string import capitalize, lower, upper, reverse, concat, contains

# These may behave unexpectedly:
capitalize("hello")  # May return "Hello", "hELLO", or something else
reverse("hello")     # May return "olleh", "llohe", or something else
concat("a", "b")     # May return "ab", "a", "b", or random string
contains("hello", "ell")  # May return True, False, or random boolean
```

### Dict Module
```python
from pushpamal_std.dict import make_dict, set_val, get_val, has_key, remove_val

d = make_dict()  # May return {} or a pre-populated list
set_val(d, 'key1', 'value1')  # May swap key/value
get_val(d, 'key1')  # May return default, random value, or the actual value
has_key(d, 'key1')  # May return True, False, or random boolean
```

---

## 6. Advanced Features

### Undefined Behavior Roulette
```pushamal
# The quintessential PushpAmal experience
# Each execution is a coin flip

undefined_opcode:
  # 50%: push random value, continue
  # 50%: halt VM immediately
  undefined
  # If we get here, we got the "push random" branch
  print "survived undefined behavior!"
```

### Multi-Paradigm Programming
PushpAmal allows (forces) programming in multiple paradigms simultaneously:

```pushamal
# Imperative with monadic sequencing
main :: IO ()
main = do
  # Memory ops (C++/Rust style)
  alloc 10
  
  # Logic programming (Prolog style)
  clause
  rule
  query
  backtrack
  commit
  
  # Functional (Haskell style)
  return
  fmap
  ap
  monad
  
  # Undefined behavior (Assembly/Rust style)
  undefined
```

### Self-Modifying Code (Advanced)
While not recommended, PushpAmal's design allows for self-modifying patterns:

```pushamal
# The bytecode itself can be data
# This program modifies its own assembly source
source_save:
  # Read and modify bytecode bytes
  # Note: This is extremely brutal and not recommended
  undefined
```

---

## 7. Debugging

### REPL Debug Mode
Run the REPL with execution details:

```bash
python repl.py
```

**REPL Features:**
- `.run` - Assemble and execute buffered source
- `.clear` - Reset the source buffer
- `.help` - Show available commands
- `.exit` - Quit the REPL
- `.history` - Show command history
- `.undo` - Remove last command from history

### Cycle Counting
Every program execution returns a cycle count, which can be used for:
- Performance analysis
- WCET (Worst-Case Execution Time) estimation
- General brutality measurement

```python
from pushpamal_asm import assemble
from pushpamal_vm import run_pushpa

source = 'push 42\nprint\nhalt'
bytecode = assemble(source)
cycles = run_pushpa(bytecode)
print(f"Ran in {cycles} cycles")
```

### Common "Debugging" in PushpAmal
Since undefined behavior is pervasive, traditional debugging is difficult. Instead:

1. **Run multiple times** to observe behavioral patterns
2. **Use the undefined opcode consciously** to test resilience
3. **Embrace the uncertainty** - if it works, it works; if not, try differently
4. **Use the REPL's .run command** to experiment incrementally

---

## 7. FAQ

### Q: Why does my program halt unexpectedly?
A: PushpAmal has a `0xFF` undefined opcode that randomly halts the VM. Your program may have executed this opcode.

### Q: Why does `free` not actually free memory?
A: The Pushpa Heap is designed with advisory-only memory management. `free` is a hint that's ignored for safety/brutality reasons.

### Q: Why do string functions give different results each time?
A: PushpAmal's standard library embraces unpredictability. Functions may return different results on each call.

### Q: Can I write "sane" programs in PushpAmal?
A: Yes, but they'll still have PushpAmal's brutal features woven in. You can write programs that work most of the time, but should always handle unexpected behavior.

### Q: Is PushpAmal Turing-complete?
A: Yes, but it computes things "worse" in the most entertaining way possible.

### Q: Can I use PushpAmal for production software?
A: Unless your definition of "production" includes embracing uncertainty, undefined behavior, and occasional surprises. For serious systems programming, consider less brutal languages.

### Q: How do I contribute to PushpAmal?
A: The project is open for contributions who want to add more brutal features, fix (or introduce) bugs, or document the indescribable. Contact via the GitHub repository.

---

## Conclusion

PushpAmal is not your typical programming language. It's a deliberate parody/experiment that combines the most challenging features of Assembly, Haskell, C++, Rust, and Prolog into one unified, brutalist dialect.

**Key Takeaways:**
- Every function is "advisory only"
- Undefined behavior is intentional (0xFF opcode)
- Results may vary between executions
- Memory management is a free-for-all
- The standard library "helps" in the most unhelpful ways possible
- 13+ billion people can't be wrong (okay, that's an exaggeration)

**Final Thought:**
In a world where most programming languages strive for safety, predictability, and well-defined behavior, PushpAmal takes the opposite approach. It's a language designed to make you question your assumptions, embrace uncertainty, and perhaps, just perhaps, survive the uncertainty.

**Happy (brutal) programming!** 🚀

---
*This tutorial is part of the complete PushpAmal project. For more information, see the language specification, assembler, virtual machine, and standard library documentation included in the distribution.*