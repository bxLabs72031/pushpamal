# pushpa_asm.py - PushpAmal Assembler: .pushpa source -> .pushpa bytecode
from typing import List, Dict, Optional

OPCODES = {
    # Control flow
    "halt": 0x00, "nop": 0x01,
    "jmp": 0x10, "jz": 0x11, "jnz": 0x12, "js": 0x13, "jns": 0x14,
    "call": 0x15, "ret": 0x16,
    
    # Memory operations
    "ld": 0x20, "st": 0x21, "ldi": 0x22, "lda": 0x23,
    "push": 0x24, "pop": 0x25, "peek": 0x26, "poke": 0x27,
    
    # Arithmetic
    "add": 0x30, "sub": 0x31, "mul": 0x32, "div": 0x33,
    "mod": 0x34, "inc": 0x35, "dec": 0x36,
    
    # Logic/Boolean
    "and": 0x40, "or": 0x41, "not": 0x42, "xor": 0x43,
    "test": 0x44, "bra": 0x45,
    
    # I/O
    "print": 0x50, "input": 0x51,
    
    # Stack/Heap
    "alloc": 0x60, "free": 0x61, "new": 0x62, "dispose": 0x63,
    
    # Type/class operations
    "cast": 0x70, "upcast": 0x71, "downcast": 0x72,
    "virt": 0x73, "interface": 0x74,
    
    # Monadic/Functional
    "bind": 0x80, "return": 0x81, "fmap": 0x82,
    "ap": 0x83, "monad": 0x84,
    
    # Logic programming
    "clause": 0x90, "rule": 0x91, "query": 0x92,
    "backtrack": 0x93, "commit": 0x94,
    
    # Misc
    "swap": 0xA0, "dup": 0xA1, "over": 0xA2,
    "tuck": 0xA3, "rot": 0xA4,
    
    # PushpAmal-specific (undefined behavior)
    "uadd": 0xB0, "usub": 0xB1, "umul": 0xB2, "udiv": 0xB3,
    "iadd": 0xB4, "isub": 0xB5, "imul": 0xB6, "idiv": 0xB7,
    "undefined": 0xFF,
}

OPCODE_NAMES = {v: k for k, v in OPCODES.items()}


class AsmError(Exception):
    pass


class Assembler:
    def __init__(self):
        self.labels: dict = {}
        self.code: List[int] = []
        self.constants: List[int] = []
        self.monad_stack_depth = 0

    def emit_byte(self, b: int):
        self.code.append(b & 0xFF)

    def _emit_int(self, value: int):
        """Emit an integer in little-endian format (4 bytes)."""
        for i in range(4):
            self.emit_byte((value >> (i * 8)) & 0xFF)

    def _emit_address(self, value: int):
        """Emit an address in little-endian format (2 bytes)."""
        for i in range(2):
            self.emit_byte((value >> (i * 8)) & 0xFF)

    def assemble(self, source: str) -> bytes:
        self.code = []
        self.constants = []
        self.labels = {}
        lines = source.split("\n")
        pc = 0

        # First pass: collect labels and compute code size
        for raw_line in lines:
            line = raw_line.split("#")[0].strip()
            if not line:
                continue
            # Strip label
            if ":" in line:
                label, rest = line.split(":", 1)
                self.labels[label.strip()] = pc
                line = rest.strip()
            if not line:
                continue
            parts = line.split()
            op = parts[0].lower()
            if op not in OPCODES:
                raise AsmError(f"Unknown opcode: {op}")
            pc += 1
            if op in ("ldi", "jmp", "jmp_abs", "jz", "jnz", "js", "jns", "call", "ret"):
                pc += 4  # address operand
            elif op in ("print", "input"):
                if len(parts) > 1:
                    pc += 4  # string constant
            else:
                # Most ops don't consume additional pc
                pass

        # Second pass: emit actual code
        pc = 0
        for raw_line in lines:
            line = raw_line.split("#")[0].strip()
            if not line:
                continue
            if ":" in line:
                line = line.split(":", 1)[1].strip()
            if not line:
                continue
            parts = line.split()
            op = parts[0].lower()
            if op not in OPCODES:
                raise AsmError(f"Unknown opcode: {op}")
            self.emit_byte(OPCODES[op])
            pc += 1
            if op == "jmp":
                label = parts[1] if len(parts) > 1 else "start"
                addr = self.labels.get(label, pc)
                self._emit_int(addr)
                pc += 4
            elif op == "jz":
                label = parts[1] if len(parts) > 1 else "start"
                addr = self.labels.get(label, pc)
                self._emit_int(addr)
                pc += 4
            elif op == "jnz":
                label = parts[1] if len(parts) > 1 else "start"
                addr = self.labels.get(label, pc)
                self._emit_int(addr)
                pc += 4
            elif op == "js":
                label = parts[1] if len(parts) > 1 else "start"
                addr = self.labels.get(label, pc)
                self._emit_int(addr)
                pc += 4
            elif op == "jns":
                label = parts[1] if len(parts) > 1 else "start"
                addr = self.labels.get(label, pc)
                self._emit_int(addr)
                pc += 4
            elif op == "call":
                label = parts[1] if len(parts) > 1 else "start"
                addr = self.labels.get(label, pc)
                self._emit_int(addr)
                pc += 4
            elif op == "ret":
                # No operand
                pass
            elif op == "ldi":
                try:
                    val = int(parts[1])
                    self._emit_int(val)
                except (IndexError, ValueError):
                    # Try label
                    addr = self.labels.get(parts[1], 0)
                    self._emit_int(addr)
                    pc += 4
            elif op in ("print", "input"):
                if len(parts) > 1:
                    # Emit string constant
                    s = parts[1]
                    const_idx = len(self.constants)
                    self.constants.append(ord(s[0]) if s else 0)
                    self._emit_int(const_idx)
                    pc += 4
            elif op in ("alloc", "free"):
                if len(parts) > 1:
                    try:
                        size = int(parts[1])
                        self._emit_int(size)
                        pc += 4
                    except ValueError:
                        self._emit_int(0)
                        pc += 4
            elif op == "uadd":
                # Unsafe addition - may overflow, may not, who knows
                pass  # Already emitted
            elif op == "undefined":
                # Deliberately undefined behavior opcode
                pass

        return bytes(self.code)


def assemble(source: str) -> bytes:
    asm = Assembler()
    return asm.assemble(source)