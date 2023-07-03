# Getting Started
1. Install [poetry](https://python-poetry.org/docs/): `curl -sSL https://install.python-poetry.org | python3 -`
1. Run `pre-commit install` to setup pre-scripts.
2. Open poetry shell: `poetry shell`
3. Pull db from s3: `scripts/s3pull.sh`
4. Open jupyter notebook: `code .`

# Tests
- Run `pytest` from `pymoney/dbwrapper`
- Snapshots are created using syrupy. Run `pytest --snapshot-update` to update snapshots. Use `pytest -s` to see standard output for tests that do not fail (this can result in a lot of output).
