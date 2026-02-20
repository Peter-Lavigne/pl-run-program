from os import chdir, environ
from pathlib import Path

from pl_run_program.program_at_path import Program
from pl_run_program.run_program import run_program


def test_run_program(echo_program: Program) -> None:
    result = run_program(echo_program, ["hello"])

    assert result.stdout == "hello\n"
    assert result.stderr == ""
    assert result.returncode == 0


def test_with_error(bash_program: Program) -> None:
    result = run_program(bash_program, ["-c", "echo ERROR 1>&2 && exit 1"])

    assert result.stdout == ""
    assert result.stderr == "ERROR\n"
    assert result.returncode == 1


def test_with_env(bash_program: Program) -> None:
    result = run_program(
        bash_program,
        ["-c", "echo $TEST_ENV_VAR"],
        env={"TEST_ENV_VAR": "test value"},
    )

    assert result.stdout == "test value\n"
    assert result.stderr == ""
    assert result.returncode == 0


def test_with_stdin(cat_program: Program) -> None:
    result = run_program(cat_program, stdin="input data")

    assert result.stdout == "input data"
    assert result.stderr == ""
    assert result.returncode == 0


def test_with_cwd(tmp_path: Path, pwd_program: Program) -> None:
    result = run_program(pwd_program, cwd=tmp_path)

    assert result.stdout.strip() == str(tmp_path)
    assert result.stderr == ""
    assert result.returncode == 0


def test_with_no_args(true_program: Program) -> None:
    result = run_program(true_program)

    assert result.stdout == ""
    assert result.stderr == ""
    assert result.returncode == 0


def test_empty_output(true_program: Program) -> None:
    result = run_program(true_program)

    assert result.stdout == ""
    assert result.stderr == ""
    assert result.returncode == 0


def test_multiline_output(bash_program: Program) -> None:
    result = run_program(bash_program, ["-c", "echo line1; echo line2; echo line3"])

    assert result.stdout == "line1\nline2\nline3\n"
    assert result.returncode == 0


def test_with_special_characters_in_args(echo_program: Program) -> None:
    result = run_program(echo_program, ["foo; echo bar"])

    assert result.stdout == "foo; echo bar\n"
    assert result.returncode == 0


def test_with_quotes_in_args(echo_program: Program) -> None:
    results = [
        run_program(echo_program, ['he said "hello"']),
        run_program(echo_program, ["he said 'hello'"]),
        run_program(echo_program, ["he said `hello`"]),
    ]

    assert [r.stdout for r in results] == [
        'he said "hello"\n',
        "he said 'hello'\n",
        "he said `hello`\n",
    ]
    assert all(r.returncode == 0 for r in results)


def test_does_not_inherit_env_variables(bash_program: Program) -> None:
    environ["NON_EXISTENT_ENV_VAR"] = "some_value"
    result = run_program(bash_program, ["-c", "echo $NON_EXISTENT_ENV_VAR"])

    assert result.stdout == "\n"
    assert result.returncode == 0


def test_inherits_cwd(tmp_path: Path, pwd_program: Program) -> None:
    start_cwd = Path.cwd()
    try:
        chdir(tmp_path)
        result = run_program(pwd_program)

        assert result.stdout.strip() == str(tmp_path)
        assert result.returncode == 0
    finally:
        # Not doing this causes the cwd to change for subsequent tests
        chdir(start_cwd)
