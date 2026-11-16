[
  {
    "name": "pushpamal",
    "version": "0.0.1",
    "description": "PushpAmal - The Brutal Programming Language",
    "py_modules": ["pushpamal_asm", "pushpamal_vm", "pushpamal_std.math", "pushpamal_std.io", "pushpamal_std.string", "pushpamal_std.dict", "pushpamal_compiler", "repl"],
    "packages": ["pushpamal_std"],
    "install_requires": [],
    "entry_points": {
      "console_scripts": [
        "pushpamal=pushpamal_asm:main",
        "pushpamalcomp=pushpamal_compiler:main",
        "pushplrepl=repl:main",
      ]
    },
    "project_urls": {
      "Homepage": "https://github.com/bxqbit/pushpamal",
      "Documentation": "https://github.com/bxqbit/pushpamal/blob/main/PUSHAMAL_TUTORIAL.md",
      "Source": "https://github.com/bxqbit/pushpamal",
      "Tracker": "https://github.com/bxqbit/pushpamal/issues",
    },
    "classifiers": [
      "Development Status :: 3 - Alpha",
      "Intended Audience :: Masochists",
      "License :: OSI Approved :: MIT License",
      "Programming Language :: Python :: 3",
      "Topic :: Software Development :: Interpreters",
      "Topic :: Games/Entertainment",
    ],
  }
]