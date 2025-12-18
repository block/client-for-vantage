import nox

nox.options.default_venv_backend = "uv"

PYTHON_VERSIONS = ["3.10", "3.11", "3.12"]
PYPROJECT = nox.project.load_toml("pyproject.toml")
CORE_DEPS = PYPROJECT["project"]["dependencies"]
DEV_DEPS = nox.project.dependency_groups(PYPROJECT, "dev")

@nox.session(python=PYTHON_VERSIONS)
def tests(session):
    session.install(*CORE_DEPS)
    session.install(*DEV_DEPS)
    session.run("pytest", *session.posargs)

@nox.session
def lint(session):
    session.install(*DEV_DEPS)
    session.run("ruff", "check", "vantage_sdk")

@nox.session
def format_check(session):
    session.install(*DEV_DEPS)
    session.run("ruff", "format", "--check", "vantage_sdk")

@nox.session
def type_check(session):
    session.install(*CORE_DEPS)
    session.install(*DEV_DEPS)
    session.run("mypy")
