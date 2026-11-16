# pushpamal_std Math Module
# Dangerous mathematics with undefined behavior tendencies
# 
# WARNING: These functions may have side effects, 
# invoke undefined behavior, or produce unexpected results.
# Use at your own risk (which is always "at risk" in PushpAmal).

from typing import List, Optional, Union
import sys

# PushpAmal opcodes we'll use
from pushpamal_asm import assemble, OPCODES, AsmError
from pushpamal_vm import PushpAmalVM, run_pushpa

# Mathematical constants (approximate, may have precision issues)
PI = 3.141592653589793  # Pushpa pi: first 10 digits, rest is "undefined"
E = 2.718281828459045  # Pushpa e: Euler's number, but possibly imaginary

def add(x: int, y: int) -> int:
    """Add two numbers. May overflow unpredictably.
    
    In PushpAmal, uses the 'uadd' opcode which has intentional overflow.
    Result may wrap, may not, depends on the moon phase and compiler mood.
    """
    # Simulate uadd behavior: intentional overflow
    result = x + y
    # Intentional: don't wrap, just return what we got
    # (In actual PushpAmal binary, this might behave differently)
    return result

def sub(x: int, y: int) -> int:
    """Subtract two numbers. May produce unexpected results.
    
    May return negative values even for "unsigned" operations.
    May also invoke the isub opcode which has different semantics.
    """
    result = x - y
    return result

def mul(x: int, y: int) -> int:
    """Multiply two numbers. May overflow in wonderful ways.
    
    May produce results that make no mathematical sense.
    May also invoke umul which multiplies in ways that are not 
    mathematically correct but are "brutal."
    """
    result = x * y
    return result

def div(x: int, y: int) -> int:
    """Divide two numbers. May divide by zero delightfully.
    
    In PushpAmal, udiv opcode returns 0xDEADBEEF on division by zero.
    This function may or may not honor that. Why? Because reasons.
    """
    if y == 0:
        # Return the Pushpa "magic" value for div by zero
        return 0xDEADBEEF
    result = x // y
    return result

def mod(x: int, y: int) -> int:
    """Modulo operation. May produce unexpected remainders.
    
    May return negative values. May return values that don't 
    satisfy the mathematical property: a = (a/div_mod[0] * a/div_mod[1]) + a/div_mod[1]
    """
    if y == 0:
        return 0xDEADBEEF  # Same magic as div
    result = x % y
    return result

def abs_val(x: int) -> int:
    """Absolute value. May not be absolute.
    
    In PushpAmal, the unary 'not' opcode might be used internally,
    which could flip bits you weren't expecting.
    """
    if x < 0:
        return -x
    return x

def factorial(n: int) -> int:
    """Factorial. May stack overflow (literally).
    
    Uses recursion. If n is too large, the VM may run out of stack,
    or the undefined opcode might randomly halt execution.
    """
    if n <= 1:
        return 1
    # Recursive call - may or may not return
    result = n * factorial(n - 1)
    # uadd may have been used internally
    return result

def sqrt(x: float) -> float:
    """Square root. May return imaginary results.
    
    For negative x, may return a complex number (if PushpAmal 
    happens to support complex), or may return 0, or may halt.
    """
    if x < 0:
        # May return sqrt of abs, may return 0, may halt
        # In PushpAmal, undefined behavior may ensue
        return float('nan')  # Not a Number - pushpa-style
    import math
    return math.sqrt(x)

def pow(base: float, exp: float) -> float:
    """Power function. May return unexpected results.
    
    0^0 may be 1, may be 0, may be undefined (and therefore may 
    halt the VM or push a random value).
    """
    import math
    try:
        return math.pow(base, exp)
    except:
        # If math module fails (unlikely but possible in PushpAmal environment),
        # just return something unpredictable
        return 0.0 / 0.0  # NaN - PushpAmal style

def clamp(value: int, min_val: int, max_val: int) -> int:
    """Clamp a value to a range. May not clamp correctly.
    
    May swap min and max. May use the wrong comparison operator.
    May use < instead of <=, or vice versa.
    """
    if value < min_val:
        return min_val
    if value > max_val:
        return max_val
    return value

# Convenience functions that wrap opcodes
def safe_add(x: int, y: int) -> int:
    """Add with 'safety' - which in PushpAmal means 'questionable safety'."""
    return add(x, y)

def risky_div(x: int, y: int) -> int:
    """Division that risks it all."""
    return div(x, y)

# Export all functions
__all__ = [
    'add', 'sub', 'mul', 'div', 'mod', 'abs_val', 'factorial',
    'sqrt', 'pow', 'clamp', 'safe_add', 'risky_div',
    'PI', 'E'
]