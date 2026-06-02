# Contributing

Thanks for helping improve Diting intent calibrator.

## Development setup

This project currently uses Python standard library only.

Run tests:

```bash
python3 -m unittest discover -s tests
```

Run demos:

```bash
python3 scripts/calibrator.py
python3 scripts/runtime_gate.py
```

## Pull request checklist

- Keep `SKILL.md` concise and use references for detailed policy.
- Add or update tests for any parser, gate, or memory-candidate behavior change.
- Do not weaken Runtime Gate blocking rules without adding explicit tests.
- Do not add automatic long-term memory writeback.
- Run the full test suite before opening a PR.

## Commit style

Use Conventional Commits when possible:

- `feat: add runtime gate policy`
- `fix: prevent memory candidates from leaking into handoff`
- `test: add skill metadata validation`
- `docs: update release handoff`

## Reporting feedback

Use `USAGE_LOG_TEMPLATE.md` locally or open a GitHub issue with the relevant template.
