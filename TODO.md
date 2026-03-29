# TODO

## Priority 1

- [ ] Improve failure diagnostics
  - Show local and remote `rdiff-backup` versions when relevant.
  - Detect version mismatches early.
  - Print a clear suggested fix or workaround.

- [ ] Return proper exit codes
  - Exit non-zero if any backup job fails.
  - Preserve per-job logging while making shell automation reliable.

- [ ] Support extra `rdiff-backup` options
  - Add support for compatibility-oriented flags such as `--api-version`.
  - Make version-tuning possible without editing code.

## Priority 2

- [ ] Harden the backup list parser
  - Ignore blank lines safely.
  - Improve malformed-line errors.
  - Keep line-numbered error messages.

- [ ] Clean up CLI internals
  - Rename `parsArguments` to `parse_arguments`.
  - Rename `readBackupList` to `read_backup_list`.
  - Improve naming consistency.

- [ ] Replace raw list-based job handling
  - Use a small job object or dataclass instead of positional list indexing.

- [ ] Add type hints
  - Start with `mbackuplib/cli.py`, `mbackuplib/mbackup.py`, `mbackuplib/rdiffbackup.py`, and `mbackuplib/rsyncbackup.py`.

- [ ] Replace `abstractproperty`
  - Modernize the abstract base class in `mbackuplib/mbackup.py`.

- [ ] Start using `pathlib`
  - Simplify path normalization and joining.

## Priority 3

- [ ] Expand the test suite
  - Add coverage for malformed list lines.
  - Add coverage for exit-code behavior.
  - Add coverage for preflight failures.
  - Add coverage for fallback behavior.
  - Add coverage for extra `rdiff-backup` options.

- [ ] Add GitHub Actions
  - Run tests on push and pull requests.

- [ ] Improve troubleshooting documentation
  - Add a README section for `rdiff-backup` version mismatches.
  - Document when to prefer `rsync`.

## Completed

- [x] Move packaging to `pyproject.toml`.
- [x] Move the CLI into the package.
- [x] Add automated tests.
- [x] Add `.gitignore`.
- [x] Unify version metadata.
- [x] Align CLI help text and docs.
- [x] Stop tracking generated `docs/build/` output.
- [x] Refresh the README for GitHub.
- [x] Simplify the docs approach around the README and lightweight Markdown guides.
- [x] Add backend preflight checks for local and remote executables.
