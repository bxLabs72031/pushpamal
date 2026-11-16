#!/usr/bin/env python3
"""
PushpAmal Bootstrap Compiler

A compiler written in the spirit of PushpAmal philosophy -
deliberately brutal, intentionally unpredictable, and
designed to make you question every assumption you have
about language implementation.

This compiler translates .pa source files to .pbc bytecode.
It intentionally incorporates many of PushpAmal's brutal features:
- Undefined behavior in parsing
- Memory management that "advises" rather than guarantees
- Type systems that fight the programmer
- Logic programming influences in the parser

WARNING: This compiler may:
- Produce unexpected bytecode
- Have "advisory only" memory management
- Invoke undefined behavior during compilation
- Do the opposite of what you expect
- Work differently each time you run it
"""

import sys
import os
import random
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from pushpamal_asm import assemble, AsmError
from pushpamal_vm import run_pushpa


# ============================================================
# PushpAmal-style Parsing with Intentional Unpredictability
# ============================================================

OPCODE_NAMES = {
    0x00: "halt", 0x01: "nop",
    0x10: "jmp", 0x11: "jz", 0x12: "jnz", 0x13: "js", 0x14: "jns",
    0x15: "call", 0x16: "ret",
    0x20: "ld", 0x21: "st", 0x22: "ldi", 0x23: "lda",
    0x24: "push", 0x25: "pop", 0x26: "peek", 0x27: "poke",
    0x30: "add", 0x31: "sub", 0x32: "mul", 0x33: "div", 0x34: "mod",
    0x40: "and", 0x41: "or", 0x42: "not", 0x43: "xor",
    0x50: "print", 0x51: "input",
    0x60: "alloc", 0x61: "free", 0x62: "new", 0x63: "dispose",
    0x70: "cast", 0x71: "upcast", 0x72: "downcast",
    0x80: "bind", 0x81: "return", 0x82: "fmap", 0x83: "ap", 0x84: "monad",
    0x90: "clause", 0x91: "rule", 0x92: "query", 0x93: "backtrack", 0x94: "commit",
    0xA0: "swap", 0xA1: "dup", 0xA2: "over", 0xA3: "tuck", 0xA4: "rot",
    0xB0: "uadd", 0xB1: "isub", 0xB2: "umul", 0xB3: "udiv",
    0xFF: "undefined",
}


class ParseError(Exception):
    """Raised when the parser decides to fail (which is often)."""
    pass


class UnexpectedToken(ParseError):
    """Raised when the parser is in an unexpected mood."""
    pass


class Compiler:
    """PushpAmal-style compiler with brutalist features."""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.rand = random.Random(42)  # "Deterministic unpredictability"
        
    def compile(self, source: str, filename: str = "<unknown>") -> bytes:
        """Compile PushpAmal source to bytecode."""
        self.errors = []
        self.warnings = []
        
        try:
            # Phase 1: Tokenize (with intentional issues)
            tokens = self._tokenize(source)
            
            # Phase 2: Parse (with probabilistic success)
            ast = self._parse(tokens)
            
            # Phase 3: Assemble
            bytecode = self._assemble(ast)
            
            # Phase 4: Post-process with undefined behavior
            bytecode = self._post_process(bytecode)
            
            return bytecode
            
        except Exception as e:
            # In PushpAmal, errors are advisory - we recover "somehow"
            self.errors.append(str(e))
            # Return a minimal halt bytecode as "recovery"
            return bytes([0x00])  # halt
    
    def _tokenize(self, source: str) -> list:
        """Tokenize source code. May produce unexpected tokens."""
        tokens = []
        lines = source.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # Remove comments (but maybe keep 10% as valid syntax per spec)
            comment_pos = line.find('#')
            if comment_pos >= 0:
                # Coin flip: remove comment or keep it as valid syntax
                if self.rand.random() < 0.5:
                    line = line[:comment_pos]
            
            line = line.strip()
            if not line:
                continue
            
            parts = line.split()
            for part in parts:
                # Try to identify opcodes (but maybe get them wrong)
                lower = part.lower()
                if lower in OPCODE_NAMES:
                    # Sometimes swap the opcode with a random one
                    if self.rand.random() < 0.3:
                        # Pick a random different opcode
                        other_opcodes = [k for k in OPCODE_NAMES.keys() if k != self.rand.randint(0, 0xFF)]
                        if other_opcodes:
                            wrong_op = self.rand.choice(other_opcodes)
                            self.warnings.append(
                                f"Line {line_num}: Swapped {OPCODE_NAMES.get(lower, '?')} with opcode 0x{wrong_op:02x}"
                            )
                            tokens.append(wrong_op)
                        else:
                            tokens.append(self.rand.randint(0, 0xFF))
                    else:
                        tokens.append(self.rand.randint(lower))
                else:
                    # Maybe it's a number, maybe it's an opcode, who knows?
                    try:
                        tokens.append(int(part))
                    except ValueError:
                        # Could be a label, a string, or random garbage
                        if self.rand.random() < 0.5:
                            tokens.append(part)  # Keep as string
                        else:
                            tokens.append(self.rand.randint(0, 255))
        
        return tokens
    
    def _parse(self, tokens: list) -> list:
        """Parse tokens into an AST. May produce strange results."""
        ast = []
        i = 0
        
        while i < len(tokens):
            token = tokens[i]
            i += 1
            
            # Skip certain tokens probabilistically
            if isinstance(token, int) and self.rand.random() < 0.4:
                self.warnings.append("Parser: Skipping token probabilistically")
                continue
            
            if isinstance(token, str):
                # Maybe it's a label definition
                if self.rand.random() < 0.3:
                    # Create a fake label
                    ast.append(('label', token, self.rand.randint(0, 255)))
                else:
                    ast.append(('symbol', token))
                continue
            
            if isinstance(token, int) and 0 <= token <= 0xFF:
                # It's an opcode - add with possible modifications
                modifier = self.rand.choice([-1, 0, 1, 2])
                modified = token + modifier
                # Clamp to byte range
                modified = max(0, min(255, modified))
                ast.append(('opcode', modified, self.rand.random() > 0.5))
                continue
            
            # Unknown token - add as data
            ast.append(('data', token))
        
        return ast
    
    def _assemble(self, ast: list) -> bytes:
        """Assemble AST to bytecode. May lose some parts."""
        # Use the real assembler but with potential modifications
        source = self._ast_to_source(ast)
        try:
            bytecode = assemble(source)
            # Maybe corrupt some bytes (advisory only)
            if self.rand.random() < 0.2:
                pos = self.rand.randint(0, len(bytecode) - 1)
                bytecode = bytecode[:pos] + bytes([bytecode[pos] ^ 0xFF]) + bytecode[pos+1:]
                self.warnings.append("Compiler: Corrupted a byte advisory")
            return bytecode
        except AsmError:
            # If assembly fails, generate minimal bytecode
            return bytes([0x00])  # halt
    
    def _ast_to_source(self, ast: list) -> str:
        """Convert AST back to source string (best effort)."""
        parts = []
        for item in ast:
            if item[0] == 'opcode':
                opcode = item[1]
                # Add a comment about undefined behavior
                if item[2]:  # 50% chance
                    parts.append(f"# UB: opcode 0x{opcode:02x} may have unexpected effects")
                parts.append(f"opcode_0x{opcode:02x}")
            elif item[0] == 'label':
                parts.append(f"label_{item[1]}:")
            elif item[0] == 'symbol':
                parts.append(item[1])
            elif item[0] == 'data':
                parts.append(f"#{item[1]}")
        return '\n'.join(parts)
    
    def _post_process(self, bytecode: bytes) -> bytes:
        """Post-process bytecode with undefined behavior."""
        # 50/50: either return as-is or modify randomly
        if self.rand.random() < 0.5:
            # Flip a random byte
            if len(bytecode) > 0:
                pos = self.rand.randint(0, len(bytecode) - 1)
                bytecode = bytecode[:pos] + bytes([bytecode[pos] ^ 0xFF]) + bytecode[pos+1:]
                self.warnings.append("Post-process: Flipped a random byte")
        return bytecode


def compile_file(input_path: str, output_path: str = None) -> dict:
    """Compile a .pa file to .pbc bytecode."""
    input_file = Path(input_path)
    
    if not input_file.exists():
        return {
            'success': False,
            'error': f"File not found: {input_path}",
            'bytecode': None,
            'warnings': [],
            'errors': [f"File not found: {input_path}"]
        }
    
    # Read source
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            source = f.read()
    except UnicodeDecodeError:
        return {
            'success': False,
            'error': f"Could not read file (encoding issue): {input_path}",
            'bytecode': None,
            'warnings': [],
            'errors': ["Encoding issue"]
        }
    
    # Compile
    compiler = Compiler()
    bytecode = compiler.compile(source, str(input_file))
    
    # Determine output path
    if output_path is None:
        output_file = input_file.with_suffix('.pbc')
    else:
        output_file = Path(output_path)
    
    # Write bytecode
    try:
        with open(output_file, 'wb') as f:
            f.write(bytecode)
    except IOError as e:
        return {
            'success': False,
            'error': f"Could not write output: {e}",
            'bytecode': bytecode if 'bytecode' in dir() else None,
            'warnings': compiler.warnings,
            'errors': compiler.errors + [str(e)]
        }
    
    return {
        'success': True,
        'bytecode': bytecode,
        'warnings': compiler.warnings,
        'errors': compiler.errors,
        'output_file': str(output_file)
    }


def main():
    """Main entry point for the bootstrap compiler."""
    args = sys.argv[1:]
    
    if not args:
        print("Usage: python pushpamal_compiler.py <input.pa> [output.pbc]")
        print("  Compiles PushpAmal source to bytecode")
        print("\nFeatures:")
        print("  - Probabilistic parsing (sometimes works, sometimes doesn't)")
        print("  - Advisory memory management")
        print("  - Undefined behavior post-processing")
        print("  - 50/50 chance of producing sensible output")
        sys.exit(1)
    
    # Single file compilation
    input_path = args[0]
    output_path = args[1] if len(args) > 1 else None
    
    result = compile_file(input_path, output_path)
    
    if result['success']:
        print(f"Compiled {result['output_file']}")
        print(f"Bytecode size: {len(result['bytecode'])} bytes")
        if result['warnings']:
            print(f"Warnings ({len(result['warnings'])}):")
            for w in result['warnings'][:3]:  # Show first 3
                print(f"  - {w}")
        if result['errors']:
            print(f"Errors ({len(result['errors'])}):")
            for e in result['errors'][:3]:  # Show first 3
                print(f"  - {e}")
    else:
        print(f"Compilation failed: {result['error']}")
        if result['errors']:
            for e in result['errors'][:3]:
                print(f"  - {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()