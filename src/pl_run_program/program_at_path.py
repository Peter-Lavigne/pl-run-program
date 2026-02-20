import os
from pathlib import Path
from typing import NewType

Program = NewType("Program", Path)


def program_at_path(path: Path) -> Program:
    if not path.is_absolute():
        msg = "Program path must be absolute"
        raise ValueError(msg)

    if not path.exists():
        msg = f"Program path does not exist: {path}"
        raise ValueError(msg)

    if path.is_dir():
        msg = f"Program path is a directory: {path}"
        raise ValueError(msg)

    if not os.access(path, os.X_OK):
        msg = f"Program path is not executable: {path}"
        raise ValueError(msg)

    return Program(path)
