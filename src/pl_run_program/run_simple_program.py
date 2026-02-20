from pathlib import Path

from pl_run_program.program_at_path import Program
from pl_run_program.run_program import run_program


class SimpleProgramError(Exception):
    pass


def run_simple_program(
    program: Program,
    args: list[str] | None = None,
    stdin: str | None = None,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
) -> str:
    """Wrap `run_program` for simple use cases where we want an exception on non-zero return codes and only care about stdout."""
    result = run_program(program, args=args, stdin=stdin, cwd=cwd, env=env)
    if result.returncode != 0:
        program_with_args = f"{program} {' '.join(args)}" if args else str(program)
        msg = (
            f"Program `{program_with_args}` returned non-zero return code {result.returncode}. "
            f"stdout: `{result.stdout}` stderr: `{result.stderr}`"
        )
        raise SimpleProgramError(msg)
    return result.stdout
