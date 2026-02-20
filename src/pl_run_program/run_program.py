import logging
import subprocess
from dataclasses import dataclass
from pathlib import Path

from pl_run_program.program_at_path import Program


@dataclass
class ProgramResult:
    stdout: str
    stderr: str
    returncode: int


def run_program(
    program: Program,
    args: list[str] | None = None,
    stdin: str | None = None,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
) -> ProgramResult:
    r"""
    Run a program and return its result.

    It is the responsibility of the caller to ensure that inputs are safe.

    Args:
        program: Program to run, e.g. "/bin/git", "/bin/ls", or "/usr/bin/python3". Must be an absolute path.
        args: Arguments to pass, e.g. ["commit", "-m", "message"]
        stdin: String to send to the program's stdin
        cwd: Working directory (Defaults to current working directory)
        env: Environment variables (Defaults to empty environment)

    Returns:
        ProgramResult with stdout, stderr, and return code

    Example:
        ```
        result = run_program("git", ["status"])
        print(result.stdout)

        # With stdin
        result = run_program("grep", ["error"], stdin="line1\nline2\nerror here\n")

        # Check result
        if result.returncode != 0:
            print(f"Failed: {result.stderr}")
        ```

    """
    cmd = [program] + (args or [])

    if env is None:
        env = {}

    args_log = f"[{', '.join(f'"{arg}"' for arg in args)}]" if args else "[]"
    env_log = "{" + ", ".join(f'"{k}": "{v}"' for k, v in env.items()) + "}"
    logging.debug(
        f'Running a program with the following parameters: program="{program}", args={args_log}, cwd="{cwd}", env={env_log}'
    )

    result = subprocess.run(
        cmd, input=stdin, capture_output=True, text=True, cwd=cwd, env=env, check=False
    )

    return_value = ProgramResult(
        stdout=result.stdout,
        stderr=result.stderr,
        returncode=result.returncode,
    )

    logging.debug(f"Program result: {return_value}")

    return return_value
