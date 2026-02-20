# pl-run-program

A simple interface for running non-python programs in python.

## Project Status

Alpha. Expect breaking changes.

## Installation

```
uv add pl-run-program
```

## Usage

```python
from pl_run_program import run_program, run_simple_program, program_at_path
from pathlib import Path

# Paths are validated to ensure they're absolute, execuable, exist, etc.
echo_program = program_at_path(Path("/bin/echo"))

# run_program returns a ProgramResult object with stdout, stderr, and return code.
result = run_program(echo_program, ["Hello, World!"])
print(f"run_program result: {result}")

# run_simple_program is a convenience function that returns only stdout and raises an exception if the program returns a non-zero return code.
result = run_simple_program(echo_program, ["Hello, World!"])
print(f"run_simple_program result: {result}")
```

## Releasing

Run `./release.sh`.

## License

Licensed under the Apache License 2.0. See [LICENSE](./LICENSE).
