import pytest

from pl_run_program.program_at_path import Program, program_at_path
from tests.constants import (
    BASH_ABSOLUTE_PATH,
    CAT_ABSOLUTE_PATH,
    ECHO_ABSOLUTE_PATH,
    PWD_ABSOLUTE_PATH,
    TRUE_ABSOLUTE_PATH,
)


@pytest.fixture
def echo_program() -> Program:
    return program_at_path(ECHO_ABSOLUTE_PATH)


@pytest.fixture
def bash_program() -> Program:
    return program_at_path(BASH_ABSOLUTE_PATH)


@pytest.fixture
def cat_program() -> Program:
    return program_at_path(CAT_ABSOLUTE_PATH)


@pytest.fixture
def pwd_program() -> Program:
    return program_at_path(PWD_ABSOLUTE_PATH)


@pytest.fixture
def true_program() -> Program:
    return program_at_path(TRUE_ABSOLUTE_PATH)
