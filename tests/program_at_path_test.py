import stat
from pathlib import Path

import pytest

from pl_run_program.program_at_path import program_at_path
from tests.constants import ECHO_ABSOLUTE_PATH


def test_returns_equivalent_path() -> None:
    path = program_at_path(ECHO_ABSOLUTE_PATH)

    assert path == ECHO_ABSOLUTE_PATH


def test_raises_value_error_for_nonexistent_program(tmp_path: Path) -> None:
    nonexistent_program = tmp_path / "nonexistent-program"

    with pytest.raises(ValueError):
        program_at_path(nonexistent_program)


def test_raises_value_error_for_directory(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        program_at_path(tmp_path)


def test_raises_value_error_for_non_executable_file(tmp_path: Path) -> None:
    program = tmp_path / "program.sh"
    program.write_text("#!/bin/sh\necho hello\n")
    # Remove execute permissions for user/group/other.
    program.chmod(
        program.stat().st_mode & ~(stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    )

    with pytest.raises(ValueError):
        program_at_path(program)


def test_raises_value_error_for_relative_path() -> None:
    with pytest.raises(ValueError):
        program_at_path(Path("relative/path/to/program"))
