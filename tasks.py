from invoke import task


@task(name="format")
def _format(c):
    """Format Python code."""
    c.run("ruff format")


@task(name="check")
def _check(c):
    """Lint Python code."""
    c.run("ruff check")


@task(name="check-fix")
def _check_fix(c):
    """Lint and fix Python code."""
    c.run("ruff check --fix")


@task(pre=[_format, _check_fix], name="all")
def _all(c):
    """Run all Python tasks."""
    pass
