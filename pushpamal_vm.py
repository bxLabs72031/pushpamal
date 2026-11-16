# pushpa_vm.py - PushpAmal Virtual Machine for .pushpa bytecode
from typing import List, Optional, Dict


class VMError(Exception):
    pass


class PushpAmalVM:
    """Stack-based virtual machine for PushpAmal bytecode.

    The VM executes PushpAmal bytecode with its unique combination of
    functional, imperative, and logic programming features.
    """

    def __init__(self):
        self.regs: List[int] = [0] * 16  # 16 general-purpose registers
        self.memory: List[int] = [0] * (1 << 20)  # 1MB memory
        self.pc = 0  # Program counter
        self.halted = False
        self.cycles = 0
        self.stack: List[int] = []
        self.code: List[int] = []
        self.constants: List[int] = []
        self.call_stack: List[dict] = []
        self.monad_transformers = 0
        self.io_buffer = ""

    def _read_u32(self, addr: int) -> int:
        """Read a 4-byte unsigned value from memory (little-endian)."""
        val = 0
        for i in range(4):
            if addr + i < len(self.memory):
                val |= self.memory[addr + i] << (i * 8)
        return val

    def _read_i32(self, addr: int) -> int:
        """Read a 4-byte signed value (little-endian, two's complement)."""
        val = self._read_u32(addr)
        if val >= 0x80000000:
            val -= 0x100000000
        return val

    def _write_u32(self, addr: int, val: int):
        """Write a 4-byte unsigned value to memory (little-endian)."""
        for i in range(4):
            self.memory[addr + i] = (val >> (i * 8)) & 0xFF

    def _push(self, val: int):
        self.stack.append(val & 0xFFFFFFFF)

    def _pop(self) -> int:
        if not self.stack:
            return 0
        return self.stack.pop() & 0xFFFFFFFF

    def _top(self) -> int:
        if not self.stack:
            return 0
        return self.stack[-1] & 0xFFFFFFFF

    def load(self, code: bytes, constants: List[int] = None):
        """Load bytecode and constants into the VM."""
        self.chunk = list(code)
        self.constants = list(constants) if constants else []
        self.pc = 0
        self.halted = False
        self.cycles = 0
        self.regs = [0] * 16
        self.stack = []
        self.memory = [0] * len(self.memory)
        self.call_stack = []
        self.io_buffer = ""

    def run(self, max_steps: int = 10000) -> int:
        """Execute bytecode. Returns cycle count."""
        steps = 0
        while self.pc < len(self.chunk) and not self.halted and steps < max_steps:
            self._execute_one()
            steps += 1
            self.cycles += 1
        return self.cycles

    def _execute_one(self):
        """Execute a single opcode."""
        if self.pc >= len(self.chunk):
            self.halted = True
            return

        op = self.chunk[self.pc]
        self.pc += 1

        try:
            if op == 0x00:  # halt
                self.halted = True

            elif op == 0x01:  # nop
                pass

            elif op == 0x10:  # jmp
                offset = self._read_u32()
                self.pc = offset

            elif op == 0x11:  # jz
                cond = self._pop()
                if cond == 0:
                    offset = self._read_u32()
                    self.pc = offset

            elif op == 0x12:  # jnz
                cond = self._pop()
                if cond != 0:
                    offset = self._read_u32()
                    self.pc = offset

            elif op == 0x13:  # js
                cond = self._pop()
                if cond < 0:
                    offset = self._read_u32()
                    self.pc = offset

            elif op == 0x14:  # jns
                cond = self._pop()
                if cond >= 0:
                    offset = self._read_u32()
                    self.pc = offset

            elif op == 0x15:  # call
                addr = self._read_u32()
                # Save return address
                self._push(self.pc)
                self.call_stack.append({
                    'regs': self.regs[:],
                    'stack': self.stack[:],
                })
                self.pc = addr

            elif op == 0x16:  # ret
                if self.call_stack:
                    frame = self.call_stack.pop()
                    self.regs = frame['regs']
                    self.stack = frame['stack']
                    self.pc = self._pop() if self.stack else 0
                else:
                    self.halted = True

            elif op == 0x20:  # ld
                addr = self._read_u32()
                val = self._read_u32(addr)
                self._push(val)

            elif op == 0x21:  # st
                val = self._pop()
                addr = self._read_u32()
                self._write_u32(addr, val)

            elif op == 0x22:  # ldi (load immediate)
                val = self._read_i32(self.pc)
                self.pc += 4
                self._push(val)

            elif op == 0x23:  # lda (load address)
                addr = self._read_u32()
                self._push(addr)

            elif op == 0x24:  # push
                val = self._pop()
                self._push(val)

            elif op == 0x25:  # pop
                if self.stack:
                    self._pop()

            elif op == 0x26:  # peek
                if self.stack:
                    self._push(self._top())

            elif op == 0x27:  # poke
                val = self._pop()
                addr = self._pop()
                self._write_u32(addr, val)

            elif op == 0x30:  # add
                b = self._pop()
                a = self._pop()
                self._push((a + b) & 0xFFFFFFFF)

            elif op == 0x31:  # sub
                b = self._pop()
                a = self._pop()
                self._push((a - b) & 0xFFFFFFFF)

            elif op == 0x32:  # mul
                b = self._pop()
                a = self._pop()
                self._push((a * b) & 0xFFFFFFFF)

            elif op == 0x33:  # div
                b = self._pop()
                a = self._pop()
                self._push(a // b if b != 0 else 0)

            elif op == 0x34:  # mod
                b = self._pop()
                a = self._pop()
                self._push(a % b if b != 0 else 0)

            elif op == 0x35:  # inc
                val = self._pop()
                self._push((val + 1) & 0xFFFFFFFF)

            elif op == 0x36:  # dec
                val = self._pop()
                self._push((val - 1) & 0xFFFFFFFF)

            elif op == 0x40:  # and
                b = self._pop()
                a = self._pop()
                self._push(a & b)

            elif op == 0x41:  # or
                b = self._pop()
                a = self._pop()
                self._push(a | b)

            elif op == 0x42:  # not
                a = self._pop()
                self._push(~a & 0xFFFFFFFF)

            elif op == 0x43:  # xor
                b = self._pop()
                a = self._pop()
                self._push(a ^ b)

            elif op == 0x44:  # test
                b = self._pop()
                a = self._pop()
                self._push(1 if (a & b) != 0 else 0)

            elif op == 0x45:  # bra (unconditional backtrack)
                # In logic programming, always backtrack
                pass

            elif op == 0x50:  # print
                val = self._pop()
                print(val, end=" ")
                print()

            elif op == 0x51:  # input
                # Read a character from stdin
                import sys
                if sys.stdin in sys.stdin:
                    ch = sys.stdin.read(1)
                    if ch:
                        self._push(ord(ch))
                    else:
                        self._push(0)

            elif op == 0x60:  # alloc
                size = self._read_u32() if self.pc < len(self.chunk) else 0
                # Actually, ldi should have been used...
                # For now, just adjust memory size
                needed = self.memory.__len__() + size
                if needed > len(self.memory):
                    self.memory.extend([0] * (needed - len(self.memory)))
                self._push(len(self.memory) - size)  # return base address

            elif op == 0x61:  # free
                addr = self._pop()
                # In PushpAmal, "free" is advisory only
                pass

            elif op == 0x62:  # new
                # Allocate and initialize
                size = self._read_u32() if self.pc <= len(self.chunk) else 4
                addr = len(self.memory)
                self.memory.extend([0] * size)
                self._push(addr)

            elif op == 0x63:  # dispose
                addr = self._pop()
                # Advisory only - memory is not actually freed
                pass

            elif op == 0x70:  # cast
                val = self._pop()
                # Push the same value, but with a different "type tag"
                self._push(val)

            elif op == 0x71:  # upcast
                val = self._pop()
                # "Upcast" - just push the value
                self._push(val)

            elif op == 0x72:  # downcast
                val = self._pop()
                # "Downcast" - may fail at runtime, but we don't check
                self._push(val)

            elif op == 0x73:  # virt
                # Virtual method dispatch (no-op in this VM)
                val = self._pop()
                self._push(val)

            elif op == 0x74:  # interface
                # Interface type tag (no-op)
                val = self._pop()
                self._push(val)

            elif op == 0x80:  # bind (>>=)
                k = self._pop()  # continuation
                m = self._pop()  # monad
                # Apply k to m - in PushpAmal, this always "works"
                self._push(k)  # Simplified: just push the continuation result

            elif op == 0x81:  # return (return)
                val = self._pop()
                self._push(val)  # In PushpAmal monad, return just wraps the value

            elif op == 0x82:  # fmap
                f = self._pop()  # function
                m = self._pop()  # monad
                # Apply f to the value in the monad
                # Simplified: just apply f
                val = self._pop()
                self._push(f)

            elif op == 0x83:  # ap (<*>)
                ap_fn = self._pop()
                ap_arg = self._pop()
                # Apply function to argument
                self._push(ap_fn)  # Simplified

            elif op == 0x84:  # monad
                # Mark the following computation as monadic
                self.monad_transformers += 1

            elif op == 0x90:  # clause (logic programming)
                # Declare a Horn clause
                head = self._read_u32() if self.pc < len(self.chunk) else 0
                body_count = self._read_u32() if self.pc < len(self.chunk) else 0
                # Store clause for later querying
                pass

            elif op == 0x91:  # rule
                # Declare a rule (clause without head)
                body_count = self._read_u32() if self.pc < len(self.chunk) else 0
                pass

            elif op == 0x92:  # query
                # Query the logic program
                goal = self._read_u32() if self.pc < len(self.chunk) else 0
                # Execute query, push solutions
                self._push(1)  # Push "yes" solution

            elif op == 0x93:  # backtrack
                # Logic programming backtrack
                # In PushpAmal, this always succeeds (or fails randomly)
                self._push(1)

            elif op == 0x94:  # commit
                # Commit current choices (no-op in this VM)
                pass

            elif op == 0xA0:  # swap
                a = self._pop()
                b = self._pop()
                self._push(a)
                self._push(b)

            elif op == 0xA1:  # dup
                val = self._top()
                self._push(val)

            elif op == 0xA2:  # over
                # Copy second-to-top below top
                if len(self.stack) >= 2:
                    a = self.stack[-2]
                    self._push(a)

            elif op == 0xA3:  # tuck
                # Third-from-top below top
                if len(self.stack) >= 3:
                    a = self.stack[-3]
                    b = self.stack[-1]
                    self.stack = self.stack[:-1] + [a, b]

            elif op == 0xA4:  # rot
                # Rotate top three elements
                if len(self.stack) >= 3:
                    a = self.stack[-1]
                    b = self.stack[-2]
                    c = self.stack[-3]
                    self.stack = [a, b, c] + self.stack[-3:]

            elif op == 0xB0:  # uadd (unsafe add)
                b = self._pop()
                a = self._pop()
                result = a + b
                # Intentional overflow - no wrapping
                self._push(result & 0xFFFFFFFF)

            elif op == 0xB1:  # isub (unsafe subtract)
                b = self._pop()
                a = self._pop()
                result = a - b
                self._push(result & 0xFFFFFFFF)

            elif op == 0xB2:  # umul (unsafe multiply)
                b = self._pop()
                a = self._pop()
                result = a * b
                self._push(result & 0xFFFFFFFF)

            elif op == 0xB3:  # udiv (unsafe divide)
                b = self._pop()
                a = self._pop()
                self._push(a // b if b != 0 else 0xDEADBEEF)  # Return magic on div by zero

            elif op == 0xFF:  # undefined
                # Deliberately undefined behavior
                # Random effect: may push random value, halt, or corrupt memory
                import random
                if random.random() < 0.5:
                    self._push(random.randint(0, 0xFFFFFFFF))
                else:
                    self.halted = True

            else:
                # Unknown opcode - treat as NOP
                pass

        except VMError:
            self.halted = True
        except Exception as e:
            # Catch-all: any unexpected error triggers undefined behavior
            import random
            self._push(random.randint(0, 0xFFFFFFFF))


def run_pushpa(code: bytes, constants: List[int] = None) -> int:
    """Run PushpAmal bytecode and return cycle count."""
    vm = PushpAmalVM()
    vm.load(code, constants)
    return vm.run()