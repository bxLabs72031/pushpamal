#!/usr/bin/env python3
"""PushpAmal Compiler: .pa source -> .pbc bytecode"""

import sys
import os
from pathlib import Path

# Add the pushpamal directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from pushpamal_asm import assemble


def compile_file(input_path: str, output_path: str = None) -> bool:
    """Compile a .pa source file to PushpAmal bytecode."""
    
    input_file = Path(input_path)
    
    if not input_file.exists():
        print(f"Error: File not found: {input_path}")
        return False
    
    # Read source
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            source = f.read()
    except UnicodeDecodeError:
        print(f"Error: Could not read file (encoding issue): {input_path}")
        return False
    
    # Determine output path
    if output_path is None:
        output_file = input_file.with_suffix('.pbc')
    else:
        output_file = Path(output_path)
    
    # Assemble
    try:
        bytecode = assemble(source)
    except Exception as e:
        print(f"Assembly error: {e}")
        return False
    
    # Write bytecode
    try:
        with open(output_file, 'wb') as f:
            f.write(bytecode)
        print(f"Compiled {input_file} -> {output_file}")
        print(f"  Bytecode size: {len(bytecode)} bytes")
        return True
    except IOError as e:
        print(f"Error writing output: {e}")
        return False


def main():
    args = sys.argv[1:]
    
    if not args:
        print("Usage: python compile_pa.py [file.pa] [output.pbc]")
        print("       python compile_pa.py --dir <directory>")
        sys.exit(1)
    
    # Single file compilation
    if len(args) >= 1 and not args[0].startswith('--'):
        success = compile_file(args[0], args[1] if len(args) > 1 else None)
        sys.exit(0 if success else 1)
    
    # Directory compilation
    elif args[0] == '--dir' and len(args) > 1:
        dir_path = Path(args[1])
        if not dir_path.is_dir():
            print(f"Error: Not a directory: {args[1]}")
            sys.exit(1)
        
        pa_files = list(dir_path.rglob('*.pa'))
        if not pa_files:
            print(f"No .pa files found in {dir_path}")
            sys.exit(0)
        
        for pa_file in pa_files:
            relative = pa_file.relative_to(dir_path)
            output = dir_path / relative.with_suffix('.pbc')
            success = compile_file(pa_file, output)
            if not success:
                sys.exit(1)
        
        print(f"Compiled {len(pa_files)} .pa files from {dir_path}")
        sys.exit(0)
    
    else:
        print("Unknown arguments")
        sys.exit(1)


if __name__ == "__main__":
    main()