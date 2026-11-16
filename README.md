# PushpAmal - The Brutal Programming Language

![PushpAmal Banner](https://github.com/bxqbit/pushpamal/raw/main/badge.svg)

> A programming language designed to be so brutally difficult that only the most masochistic programmers dare touch it.

PushpAmal intentionally combines the worst (best) features of Assembly, Haskell, C++, Rust, and Prolog into a single, unforgiving dialect.

## Quick Start

```python
from pushpamal_asm import assemble
from pushpamal_vm import run_pushpa

# Hello World in PushpAmal
source = """
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
"""

bytecode = assemble(source)
cycles = run_pushpa(bytecode)
print(f"Assembled {len(bytecode)} bytes, ran in {cycles} cycles")
```

## Installation

```bash
pip install pushpamal
```

Or, for the bleeding edge:

```bash
pip install git+https://github.com/bxqbit/pushpamal.git
```

## Documentation

- [Tutorial](PUSHAMAL_TUTORIAL.md)
- [Comparison vs. Top 5 Languages](PUSHAMAL_COMPARISON.md)
- [Language Specification](pushpamal_spec.md)

## Features

- ⚡ 80+ opcodes covering all paradigms
- ⚡ The Pushpa Heap (RC/GC/manual hybrid)
- ⚡ Undefined behavior opcode (0xFF - 50/50 halt or random value)
- ⚡ Standard library with Math, IO, String, Dict modules
- ⚡ REPL with multi-line support and history
- ⚡ Bootstrap compiler (self-hosting)
- ⚡ VS Code syntax highlighting
- ⚡ Comprehensive test suite (14/14 passing)

## Philosophy

> "PushpAmal: because Segfaults just aren't personal enough."

- All functions are "advisory only"
- Undefined behavior is intentional
- Results may vary between executions
- Memory management is non-deterministic
- The standard library "helps" in the most unhelpful ways

## License

MIT License - see `LICENSE` file for details.

---

*PushpAmal: because the top 5 brutal languages needed a competitor.*