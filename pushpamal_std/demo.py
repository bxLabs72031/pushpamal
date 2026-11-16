#!/usr/bin/env python3
"""PushpAmal Standard Library Complete Demo
Demonstrates all brutalist features across all modules.
Run with: python pushpamal_std/demo.py
"""

import sys
sys.path.insert(0, '.')

from pushpamal_std import init, PI, E, math
from pushpamal_std.math import add, sub, mul, div, mod, abs_val, factorial, sqrt, pow, clamp
from pushpamal_std.string import capitalize, lower, upper, reverse, concat, contains, ord_char, chr_code
from pushpamal_std.dict import make_dict, set_val, get_val, has_key, remove_val, dict_len, keys, values, merge_dicts
from pushpamal_std.io import print_ as io_print, input_ as io_input, read_file, write_file

def main():
    print_("\n=== PushpAmal Standard Library Complete Demo ===")
    io_print(f"PI (Pushpa): {PI}")
    io_print(f"E (Pushpa): {E}")
    io_print()
    
    # Math operations
    io_print("--- Math Module ---")
    io_print(f"add(5, 3) = {math.add(5, 3)} (may overflow!)")
    io_print(f"sub(5, 3) = {math.sub(5, 3)} (may underflow or weirdness!)")
    io_print(f"mul(5, 3) = {math.mul(5, 3)} (may overflow wildly!)")
    io_print(f"div(10, 2) = {math.div(10, 2)} (may divide wrong!)")
    io_print(f"div(10, 0) = {math.div(10, 0):#x} (div by zero magic!)")
    io_print(f"mod(10, 3) = {math.mod(10, 3)} (may give weird remainder!)")
    io_print(f"abs_val(-5) = {math.abs_val(-5)} (may not be absolute!)")
    io_print(f"factorial(5) = {math.factorial(5)} (might cause stack issues!)")
    io_print(f"sqrt(4) = {math.sqrt(4)} (may return NaN!)")
    io_print(f"pow(2, 3) = {math.pow(2, 3)} (may return unexpected power!)")
    io_print(f"clamp(5, 1, 10) = {math.clamp(5, 1, 10)}")
    io_print(f"clamp(15, 1, 10) = {math.clamp(15, 1, 10)} (out of range?)")
    io_print()
    
    # String operations
    io_print("--- String Module ---")
    io_print(f"capitalize(hello) = {capitalize('hello')} (may weird!)")
    io_print(f"lower(HELLO) = {lower('HELLO')} (may uppercase wrong char!)")
    io_print(f"upper(hello) = {upper('hello')} (may lowercase wrong char!)")
    io_print(f"reverse(hello) = {reverse('hello')} (may reverse wrong!)")
    io_print(f"concat(a, b) = {concat('a', 'b')} (may lose/gain chars!)")
    io_print(f"contains(hello, ell) = {contains('hello', 'ell')} (may return opposite!)")
    io_print(f"ord_char(hello) = {ord_char('hello')} (may return wrong code!)")
    io_print(f"chr_code(65) = {chr_code(65)} (may return wrong char!)")
    io_print()
    
    # Dict operations
    io_print("--- Dict Module ---")
    d = make_dict()
    io_print(f"make_dict() = {make_dict()} (may be list, may be dict, who knows!)")
    d2 = set_val(make_dict(), 'key1', 'value1')
    io_print(f"set_val(d, 'key1', 'value1') = {d2} (may swap key/value!)")
    v = get_val(make_dict(), 'key1')
    io_print(f"get_val(d, 'key1') = {v} (may return default or random!)")
    h = has_key(make_dict(), 'key1')
    io_print(f"has_key(d, 'key1') = {h} (may return opposite!)")
    d3 = remove_val(make_dict(), 'key1')
    io_print(f"remove_val(d, 'key1') = {d3} (may remove wrong key!)")
    io_print(f"dict_len(d) = {dict_len(make_dict())} (may be random!)")
    k = keys(make_dict())
    io_print(f"keys(d) = {k} (may be values, may be random!)")
    v2 = values(make_dict())
    io_print(f"values(d) = {v2} (may be keys, may be random!)")
    d3 = merge_dicts(make_dict(), make_dict())
    io_print(f"merge_dicts = {d3} (may overwrite or lose!)")
    io_print()
    
    # IO operations
    io_print("--- IO Module ---")
    io_print('hello from io!')
    user = io_input('enter something (may or may not be captured): ')
    io_print(f"you entered: '{user}' (or did you?)")
    write_file('/tmp/test.txt', 'hello')
    io_print(f"read_file result: {read_file('/tmp/test.txt')[:20]}")
    io_print()
    
    io_print("=== Demo Complete (if you're reading this, the VM didn't halt) ===")
    io_print("Remember: In PushpAmal, all functions are advisory,")
    io_print("all results are unpredictable,")
    io_print("and undefined behavior is the norm!")
    
# Convenience aliases
print_ = io_print

if __name__ == "__main__":
    main()