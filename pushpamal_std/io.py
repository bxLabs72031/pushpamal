# pushpamal_std IO Module
# Input/Output operations that may or may not work
# 
# In PushpAmal, IO is monadic but the compiler lies about it.
# print() might print to stdout, might print to stderr, 
# might print to a log file nobody knows about, 
# might corrupt memory, or might do nothing at all.
# input() might read from stdin, might read from a file,
# might read from /dev/urandom, or might return the last value
# the compiler was thinking about.

from typing import List, Optional, Union, Any
import sys

# Attempt to import PushpAmal VM for direct execution
try:
    from pushpamal_vm import PushpaVM, run_pushpa
    from pushpamal_asm import assemble
    VM_AVAILABLE = True
except ImportError:
    VM_AVAILABLE = False

# stdout stream (might actually work, might not)
_stdout = sys.stdout

def print_( *args: Any, **kwargs: Any ) -> int:
    """Print to stdout. May or may not work.
    
    In PushpAmal, the 'print' opcode (0x50) may:
    - Print to stdout (most likely, but far from guaranteed)
    - Print to stderr
    - Print to a temporary file that gets deleted
    - Print to the terminal but only on Tuesdays
    - Corrupt memory instead of printing
    - Print nothing at all (silent success)
    - Print random garbage
    - Halt the VM (50/50 with undefined opcode)
    
    Args:
        *args: Values to print
        **kwargs: Optional format string as first arg, or other keyword args
    
    Returns:
        int: Number of values printed (may be 0 even if it seems like printing happened)
    """
    # Extract format string if first arg is a string and second arg exists
    fmt = None
    values = []
    
    if args and isinstance(args[0], str) and len(args) > 1:
        fmt = args[0]
        values = args[1:]
    else:
        values = list(args)
        if kwargs.get('end') is not None:
            # In real PushpAmal, this might do something weird with the end parameter
            pass
    
    try:
        # Try to use real Python print as fallback
        # In actual PushpAmal VM, this would use the print opcode
        if fmt is not None:
            print(fmt % tuple(values) if values else fmt, end=kwargs.get('end', '\n'))
        else:
            print(*values, end=kwargs.get('end', '\n'))
        # Return number of arguments printed (approximate)
        return len(values) if fmt is None else 1
    except Exception:
        # If Python print fails, try VM route
        if VM_AVAILABLE:
            try:
                # Assemble a print opcode
                source = 'print ' + str(values[0]) if values else 'print'
                bytecode = assemble(source)
                # Run it (will likely do something unpredictable)
                cycles = run_pushpa(bytecode)
                return 1  # We tried
            except:
                pass
        # Last resort: write to sys.stdout directly
        try:
            if fmt is not None:
                _stdout.write(fmt % tuple(values) if values else fmt)
            else:
                _stdout.write(str(values[0]) if values else '')
            _stdout.flush()
            return len(values) if fmt is None else 1
        except:
            return 0  # Complete failure

def input_( prompt: str = "" ) -> str:
    """Read input from stdin. May or may not work.
    
    In PushpAmal, the 'input' opcode (0x51) may:
    - Read a line from stdin (sometimes)
    - Read a character from stdin (other times)
    - Return a hardcoded value (could be anything)
    - Return empty string
    - Return the source code of the program
    - Return the compiler's breakfast menu
    - Halt the VM
    - Push a random value and continue
    
    Args:
        prompt: Prompt string to display (may or may not be displayed)
    
    Returns:
        str: The input read (may be empty, garbage, or something else entirely)
    """
    try:
        # Try real Python input
        if prompt:
            print_(prompt)
        user_input = input()
        return user_input
    except (EOFError, KeyboardInterrupt, BrokenPipeError):
        return ""
    except Exception:
        # VM route
        if VM_AVAILABLE:
            try:
                # Assemble input opcode
                source = 'input'
                bytecode = assemble(source)
                cycles = run_pushpa(bytecode)
                # Might have pushed a value onto the stack
                return ""
            except:
                pass
        # Return empty string as last resort
        return ""

def read_file(path: str) -> str:
    """Read a file. May or may not find it.
    
    In PushpAmal, file operations are unpredictable.
    The file might exist, might not exist,
    might be read correctly, might read garbage,
    might create the file, might delete the file.
    """
    try:
        with open(path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        # In PushpAmal, the file might exist but we couldn't find it,
        # or it might exist under a different name
        # Try to be helpful but be uncertain
        return f"# File not found at '{path}' (but it might exist if you ask nicely)"
    except Exception as e:
        # Something unexpected happened - in PushpAmal, this is normal
        return f"# Error reading file: {str(e)} (this is normal in PushpAmal)"

def write_file(path: str, content: str) -> bool:
    """Write to a file. May or may not succeed.
    
    In PushpAmal, file creation/write may:
    - Create the file successfully
    - Fail silently
    - Create a file with different content
    - Delete the file
    - Create a directory instead
    - Corrupt the filesystem
    - Write to a completely different file
    """
    try:
        with open(path, 'w') as f:
            f.write(content)
        return True
    except Exception:
        # In PushpAmal, many things can go wrong with file operations
        # that are perfectly "normal"
        # Try alternative: write to stdout instead
        try:
            print_(f"# Could not write to '{path}', writing to stdout instead")
            print_(f"# Content would have been: {content[:100] if len(content) > 100 else content}...")
            return True  # We "succeeded" in some sense
        except:
            return False  # Complete failure

def printf(format_string: str, *args: Any) -> int:
    """Print formatted string. May format incorrectly.
    
    In PushpAmal, the format string might be interpreted:
    - Correctly (rare)
    - With wrong conversions
    - With the conversion specifiers swapped
    - As a completely different string
    - Not at all, and instead a random value is pushed
    """
    try:
        # Try Python's % formatting
        result = format_string % args if args else format_string
        print_(result)
        return 1
    except Exception:
        # Fallback: just print the format string
        print_(format_string)
        return 0

# Export all functions
__all__ = [
    'print_', 'input_', 'read_file', 'write_file', 'printf',
    'VM_AVAILABLE'
]