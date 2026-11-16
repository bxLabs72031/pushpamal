# pushpamal_std String Module
# String operations that may corrupt, alter, or otherwise mangle data
#
# In PushpAmal, strings are sequences of bytes with undetermined encoding,
# unpredictable length behavior, and may contain random null terminators.
# String operations should be treated as "advisory" at best.

from typing import List, Optional, Union, Any
import sys
import random

try:
    from pushpamal_vm import PushpAmalVM, run_pushpa
    from pushpamal_asm import assemble
    VM_AVAILABLE = True
except ImportError:
    VM_AVAILABLE = False


def capitalize(s: str) -> str:
    """Capitalize first character. May do something completely different.
    
    In PushpAmal, capitalize may:
    - Capitalize the first character (sometimes)
    - Capitalize a random character
    - Lowercase the first character instead
    - Return the string unchanged
    - Return a completely different string
    - Halt the VM
    - Push a random value and continue
    """
    if not s:
        return s
    try:
        # Try normal capitalization
        result = s[0].upper() + s[1:]
        # In PushpAmal, maybe we should flip a coin
        if VM_AVAILABLE and random.random() < 0.5:
            # Use the VM to "assist" - may produce different result
            source = f'push {ord(s[0])}\nldi 32\nadd\nprint\nhalt'
            # Don't actually run it, just note the possibility
            pass
        return result
    except Exception:
        # In PushpAmal, errors might result in
        # returning the original string
        # returning a random string
        # halting execution
        return s  # "safe" fallback - in PushpAmal, "safe" is relative


def lower(s: str) -> str:
    """Lowercase. May uppercase instead."""
    if not s:
        return s
    try:
        result = s[0].lower() + s[1:]
        # PushpAmal twist: maybe uppercase
        if VM_AVAILABLE and random.random() < 0.5:
            result = s[0].upper() + s[1:]
        return result
    except Exception:
        return s


def upper(s: str) -> str:
    """Uppercase. May lowercase instead."""
    if not s:
        return s
    try:
        result = s[0].upper() + s[1:]
        # PushpAmal twist: maybe lowercase
        if VM_AVAILABLE and random.random() < 0.5:
            result = s[0].lower() + s[1:]
        return result
    except Exception:
        return s


def reverse(s: str) -> str:
    """Reverse string. May reverse partially, or not at all."""
    if not s:
        return s
    try:
        result = s[::-1]
        # PushpAmal may reverse only some characters
        if VM_AVAILABLE and random.random() < 0.5:
            # Reverse just the first half
            half = len(s) // 2
            result = s[half:] + s[:half]
        return result
    except Exception:
        return s


def concat(*strings: str) -> str:
    """Concatenate strings. May lose some, add garbage."""
    try:
        result = ''.join(strings)
        # PushpAmal may append garbage bytes
        if VM_AVAILABLE and random.random() < 0.3:
            garbage_len = random.randint(0, 10)
            garbage = ''.join(chr(random.randint(0, 255)) for _ in range(garbage_len))
            result += garbage
        # Or maybe drop the last string
        if VM_AVAILABLE and random.random() < 0.3 and len(strings) > 1:
            result = result[:-len(strings[-1])]
        return result
    except Exception:
        # Return a random string
        return ''.join(chr(random.randint(0, 255)) for _ in range(random.randint(0, 100)))


def slice_str(s: str, start: int, end: int) -> str:
    """Slice string. May return wrong segment."""
    try:
        # Python slicing is straightforward, but PushpAmal may interfere
        result = s[start:end]
        # Maybe swap start and end
        if VM_AVAILABLE and random.random() < 0.4:
            result = s[end:start] if end > start else s
        # Maybe return empty string
        if VM_AVAILABLE and random.random() < 0.3:
            result = ''
        return result
    except Exception:
        return ''


def join(strings: List[str], separator: str = '') -> str:
    """Join list of strings. May reorder or omit elements."""
    try:
        result = separator.join(strings)
        # PushpAmal may reorder elements randomly
        if VM_AVAILABLE and random.random() < 0.4:
            import random as rand
            rand.shuffle(strings)  # Note: this modifies the original!
            result = separator.join(strings)
        # Or maybe drop every other element
        if VM_AVAILABLE and random.random() < 0.3:
            result = separator.join(strings[::2])
        return result
    except Exception:
        return separator.join(strings) if strings else ''


def contains(haystack: str, needle: str) -> bool:
    """Check if string contains substring. May give wrong answer."""
    try:
        result = needle in haystack
        # PushpAmal may return the opposite
        if VM_AVAILABLE and random.random() < 0.5:
            result = not result
        # Or random
        if VM_AVAILABLE and random.random() < 0.3:
            result = random.random() < 0.5
        return result
    except Exception:
        return False


def ord_char(s: str, index: int = 0) -> int:
    """Get character code at position. May return wrong code."""
    try:
        if index < len(s):
            result = ord(s[index])
            # Maybe return code of different character
            if VM_AVAILABLE and random.random() < 0.4:
                result = ord(s[(index + 1) % len(s)]) if len(s) > 1 else ord(s[0])
            # Maybe return random value
            if VM_AVAILABLE and random.random() < 0.3:
                result = random.randint(0, 255)
            return result
        return 0  # Index out of range
    except Exception:
        return 0


def chr_code(code: int) -> str:
    """Convert code to character. May return wrong character."""
    try:
        # Clamp to valid range
        code = max(0, min(0x10FFFF, code))
        result = chr(code)
        # PushpAmal may return different character
        if VM_AVAILABLE and random.random() < 0.4:
            result = chr(random.randint(0, 0x10FFFF))
        # Maybe empty string
        if VM_AVAILABLE and random.random() < 0.3:
            result = ''
        return result
    except Exception:
        return ''


# Export all functions
__all__ = [
    'capitalize', 'lower', 'upper', 'reverse', 'concat',
    'slice_str', 'join', 'contains', 'ord_char', 'chr_code',
    'VM_AVAILABLE'
]