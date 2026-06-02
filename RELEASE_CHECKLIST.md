# Release Checklist

## Local truth-source lock

- [ ] `SKILL.md` matches runtime behavior.
- [ ] `README.md` describes current structured intent package and Runtime Gate fields.
- [ ] `CHANGELOG.md` contains the release version.
- [ ] `SESSION_HANDOFF.md` captures current decisions and next-agent context.
- [ ] `memory/` contains templates only; no unconfirmed long-term memory has been written.

## Verification

- [ ] Run `python3 -m unittest discover -s tests`.
- [ ] Confirm script entrypoints run through tests.
- [ ] Scan for `.env`, tokens, API keys, private credentials, and accidental secrets.
- [ ] Check Git status before staging.

## GitHub release

- [ ] Confirm target repository URL with the human.
- [ ] Confirm branch name with the human.
- [ ] Commit only after explicit human approval.
- [ ] Push only after explicit human approval.
- [ ] Create tag `v0.1.0-alpha` only after explicit human approval.
- [ ] Create GitHub Release with `CHANGELOG.md` notes.
- [ ] Set repository description and topics manually or through authorized GitHub tooling.
