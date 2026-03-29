# Development

## Local setup

Create a virtual environment and install the project in editable mode:

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -e .
```

Run the CLI directly from the package during development:

```bash
python3 -m mbackuplib.cli --help
```

## Tests

Run the automated test suite with:

```bash
python3 -m unittest discover -s tests -v
```

## Packaging

The project uses `pyproject.toml` with `setuptools` as the build backend.

The installed command is:

```bash
mbackup
```

## Documentation

This project intentionally keeps documentation lightweight:

* `README.rst` is the main user-facing guide
* `docs/` contains additional Markdown notes for development and troubleshooting

There is no longer a Sphinx build step or generated docs site in the repository.
