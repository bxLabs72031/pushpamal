# pushpamal_std List Module
# List operations that may or may not preserve data integrity
# 
# In PushpAmal, lists are linked lists with O(n) access,
# but the 'O' might stand for "O whatever I feel like today"
# rather than "Order" or "Operations".
# Elements may be lost, duplicated, or corrupted
# during operations.

from typing import TypeVar, List as PyList, Optional, Any, Callable
import sys

try:
    from pushpamal_vm import PushpaVM, run_pushpa
    from pushpamal_asm import assemble
    VM_AVAILABLE = True
except ImportError:
    VM_AVAILABLE = False

T = TypeVar('T')

def map_func(func: Callable, lst: PyList) -> PyList:
    """Map function over list. May lose elements.
    
    In PushpAmal, the 'map' operation may:
    - Apply the function to each element (sometimes)
    - Lose some elements in the process
    - Apply the function wrong (wrong arguments, wrong order)
    - Duplicate some elements
    - Apply the function to nothing (empty list handling is unpredictable)
    - Return a completely different list
    - Halt the VM mid-operation
    """
    result = []
    for item in lst:
        try:
            mapped = func(item)
            result.append(mapped)
        except:
            # In PushpAmal, errors during map might be ignored,
            # or the element might be dropped, or
            # a random value might be appended instead
            result.append(None)  # PushpAmal-style error handling
    return result

def filter_func(predicate: Callable, lst: PyList) -> PyList:
    """Filter list based on predicate. May keep wrong elements.
    
    In PushpAmal, the 'filter' operation may:
    - Keep elements that don't satisfy the predicate
    - Discard elements that do satisfy it
    - Keep half the elements randomly
    - Keep no elements, or all elements
    - Apply the predicate to the list itself instead of each element
    - Return a list of the same length (violating the concept of filter)
    """
    result = []
    for item in lst:
        try:
            if predicate(item):
                result.append(item)
            # Note: we might also add items that don't pass the predicate
        except:
            # In PushpAmal, predicate errors might result in
            # the element being kept or discarded unpredictably
            # We'll keep it "for safety" (which means we might keep things we shouldn't)
            result.append(item)
    return result

def reduce_func(func: Callable, lst: PyList, initial: Any = None) -> Any:
    """Reduce list to single value. May lose the value.
    
    In PushpAmal, 'reduce' (or 'fold') may:
    - Correctly reduce the list
    - Return the initial value regardless of list contents
    - Return a random element from the list
    - Return the list itself (defeating the purpose)
    - Halt the VM partway through
    - Apply the function in wrong order (right-to-left instead of left-to-right)
    - Return a completely different value type
    """
    if not lst:
        return initial
    
    result = initial
    for item in lst:
        try:
            result = func(result, item)
        except:
            # In PushpAmal, errors might result in:
            # returning the current result
            # returning a random value
            # halting the VM
            # returning the item itself
            pass
    return result if result is not None else initial

def length(lst: PyList) -> int:
    """Get list length. May return wrong length.
    
    In PushpAmal, length may:
    - Return the correct length
    - Return 0 regardless of actual length
    - Return a random number
    - Return the length of some other list
    - Return the VM's cycle count
    - Cause a stack overflow
    """
    try:
        return len(lst)
    except:
        # In PushpAmal, might return anything
        import random
        return random.randint(0, 1000000)

def append(lst: PyList, item: Any) -> PyList:
    """Append item to list. May corrupt the original.
    
    In PushpAmal, append may:
    - Correctly append the item
    - Modify the original list in unexpected ways
    - Create a new list but lose the original reference
    - Append a different item entirely
    - Not modify anything and return the original list unchanged
    - Cause a memory leak (PushpAmal Heap "features")
    """
    try:
        lst.append(item)
        return lst
    except:
        # In PushpAmal, might return a new list, might modify in place,
        # might do neither, might corrupt memory
        # We'll try and return what we have
        return lst

def push(stk: PyList, item: Any) -> PyList:
    """Push item onto stack. (Alias for append in PushpAmal context)."""
    return append(stk, item)

def pop(stk: PyList) -> Any:
    """Pop item from stack. May return wrong item.
    
    In PushpAmal, pop may:
    - Return the top item correctly
    - Return a different item (bottom, or some random element)
    - Return None (even if stack is non-empty)
    - Halt the VM
    - Underflow the stack and return 0 or garbage
    - Swap the top two elements and return the new top
    """
    try:
        if stk:
            return stk.pop()
        return 0  # Stack underflow - return 0 (PushpAmal convention)
    except:
        return 0  # Any error results in 0

def peek(stk: PyList) -> Any:
    """Look at top of stack without removing. May give wrong view."""
    try:
        if stk:
            return stk[-1]
        return 0
    except:
        return 0

# Export all functions
__all__ = [
    'map_func', 'filter_func', 'reduce_func', 'length', 'append', 'push', 'pop', 'peek',
    'VM_AVAILABLE'
]