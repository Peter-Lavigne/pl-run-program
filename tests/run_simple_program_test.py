import pytest

from pl_run_program.program_at_path import Program
from pl_run_program.run_simple_program import (
    SimpleProgramError,
    run_simple_program,
)


def test_returns_stdout(echo_program: Program) -> None:
    result = run_simple_program(echo_program, args=["Hello, World!"])

    assert result == "Hello, World!\n"


def test_raises_on_non_zero_return_code(bash_program: Program) -> None:
    with pytest.raises(SimpleProgramError, match="returned non-zero return code 1"):
        run_simple_program(bash_program, args=["-c", "exit 1"])
