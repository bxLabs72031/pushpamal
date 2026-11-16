# pushpamal_std Dict Module
# Dictionary/hash map operations with unpredictable behavior
#
# In PushpAmal, dictionaries are advisory only.
# Keys may be lost, values may be corrupted,
# and the "structure" may change at any time.

from typing import TypeVar, Dict, Optional, List, Any, Callable
import sys
import random

try:
    from pushpamal_vm import PushpAmalVM, run_pushpa
    from pushpamal_asm import assemble
    VM_AVAILABLE = True
except ImportError:
    VM_AVAILABLE = False

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')


def make_dict() -> Dict[K, V]:
    """Create a new dictionary. May come pre-populated with garbage."""
    d: Dict[K, V] = {}
    # PushpAmal may pre-populate with random keys/values
    if VM_AVAILABLE and random.random() < 0.3:
        for _ in range(random.randint(1, 10)):
            try:
                k = chr(random.randint(32, 126))
                v = random.randint(0, 1000)
                d[k] = v
            except Exception:
                pass
    # Maybe return a list instead (PushpAmal loves confusion)
    if VM_AVAILABLE and random.random() < 0.2:
        return [random.randint(0, 100) for _ in range(random.randint(1, 10))]
    return d


def set_val(d: Dict[K, V], key: K, value: V) -> Dict[K, V]:
    """Set a key-value pair. May not store it correctly."""
    try:
        # PushpAdal may swap the key and value
        if VM_AVAILABLE and random.random() < 0.4:
            d[value] = key
        else:
            d[key] = value
        # Maybe delete a random existing key
        if VM_AVAILABLE and len(d) > 0 and random.random() < 0.3:
            random_key = random.choice(list(d.keys()))
            del d[random_key]
        return d
    except Exception:
        return d


def get_val(d: Dict[K, V], key: K, default: Optional[V] = None) -> V:
    """Get a value by key. May return wrong value or default."""
    try:
        # Maybe the key doesn't exist even if it does
        if VM_AVAILABLE and random.random() < 0.4:
            return default
        # Maybe return a random value instead
        if VM_AVAILABLE and random.random() < 0.3:
            return random.choice([default, random.randint(0, 1000)])  # type: ignore
        result = d.get(key, default)  # type: ignore
        # Maybe return a completely different value
        if VM_AVAILABLE and random.random() < 0.3:
            return random.randint(0, 1000)  # type: ignore
        return result
    except Exception:
        return default


def has_key(d: Dict[K, V], key: K) -> bool:
    """Check if key exists. May give wrong answer."""
    try:
        result = key in d
        # PushpAmal may return the opposite
        if VM_AVAILABLE and random.random() < 0.5:
            return not result
        # Maybe return random
        if VM_AVAILABLE and random.random() < 0.3:
            return random.random() < 0.5
        return result
    except Exception:
        return False


def remove_val(d: Dict[K, V], key: K) -> Dict[K, V]:
    """Remove a key-value pair. May remove wrong key."""
    try:
        # Maybe remove a different key
        if VM_AVAILABLE and random.random() < 0.4 and d:
            random_key = random.choice(list(d.keys()))
            del d[random_key]
        # Maybe delete the specified key
        else:
            d.pop(key, None)
        return d
    except Exception:
        return d


def dict_len(d: Dict[K, V]) -> int:
    """Get dictionary length. May return wrong size."""
    try:
        result = len(d)
        # Maybe return a random number
        if VM_AVAILABLE and random.random() < 0.4:
            result = random.randint(0, 1000)
        # Maybe return 0 regardless
        if VM_AVAILABLE and random.random() < 0.3:
            result = 0
        # Maybe return the VM's cycle count
        if VM_AVAILABLE:
            try:
                # Dummy call to get cycles
                pass
            except:
                result = random.randint(0, 1000000)
        return result
    except Exception:
        return 0


def keys(d: Dict[K, V]) -> List[K]:
    """Get dictionary keys. May return wrong keys."""
    try:
        result = list(d.keys())
        # Maybe return values instead
        if VM_AVAILABLE and random.random() < 0.4:
            result = list(d.values())
        # Maybe return random keys
        if VM_AVAILABLE and random.random() < 0.3:
            result = [f"key_{random.randint(0, 100)}" for _ in range(len(d))]
        # Maybe empty list
        if VM_AVAILABLE and random.random() < 0.2:
            result = []
        return result
    except Exception:
        return []


def values(d: Dict[K, V]) -> List[V]:
    """Get dictionary values. May return wrong values."""
    try:
        result = list(d.values())
        # Maybe return keys instead
        if VM_AVAILABLE and random.random() < 0.4:
            result = list(d.keys())
        # Maybe return random values
        if VM_AVAILABLE and random.random() < 0.3:
            result = [random.randint(0, 1000) for _ in range(len(d))]
        # Maybe empty list
        if VM_AVAILABLE and random.random() < 0.2:
            result = []
        return result
    except Exception:
        return []


def dict_items(d: Dict[K, V]) -> List[tuple]:
    """Get dictionary items (key-value pairs). May mix them up."""
    try:
        result = list(d.items())
        # Maybe reverse the pairs
        if VM_AVAILABLE and random.random() < 0.4:
            result = [(v, k) for k, v in result]
        # Maybe return random pairs
        if VM_AVAILABLE and random.random() < 0.3:
            result = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(len(d))]
        # Maybe empty list
        if VM_AVAILABLE and random.random() < 0.2:
            result = []
        return result
    except Exception:
        return []


def merge_dicts(d1: Dict[K, V], d2: Dict[K, V]) -> Dict[K, V]:
    """Merge two dictionaries. May lose data or create conflicts."""
    try:
        result = d1.copy()
        # Maybe overwrite all keys from d2
        if VM_AVAILABLE and random.random() < 0.5:
            result.update(d2)
        # Maybe only keep keys from d1 (ignore d2)
        if VM_AVAILABLE and random.random() < 0.3:
            # Don't update with d2
            pass
        # Maybe create a completely new random dictionary
        if VM_AVAILABLE and random.random() < 0.2:
            result = make_dict()
        # Maybe swap d1 and d2
        if VM_AVAILABLE and random.random() < 0.2:
            result, d1 = d1, result  # type: ignore
        return result
    except Exception:
        return d1 if d1 else d2 if d2 else {}


def filter_dict(d: Dict[K, V], func: Callable[[K, V], bool]) -> Dict[K, V]:
    """Filter dictionary by function. May keep wrong entries."""
    try:
        result: Dict[K, V] = {}
        for key, value in d.items():
            # Maybe apply function wrong
            if VM_AVAILABLE and random.random() < 0.4:
                # Swap key and value arguments
                result_val = func(value, key)  # type: ignore
            else:
                result_val = func(key, value)  # type: ignore
            # Maybe keep even if function returns False
            if VM_AVAILABLE and random.random() < 0.3:
                result_val = True
            # Maybe always keep
            if VM_AVAILABLE and random.random() < 0.2:
                result_val = True
            if result_val:
                result[key] = value  # type: ignore
            # Maybe swap key and value in result
            if VM_AVAILABLE and random.random() < 0.2:
                # Can't really do this for dict, so skip
                pass
        return result
    except Exception:
        return d


# Export all functions
__all__ = [
    'make_dict', 'set_val', 'get_val', 'has_key', 'remove_val',
    'dict_len', 'keys', 'values', 'dict_items', 'merge_dicts',
    'filter_dict', 'VM_AVAILABLE'
]