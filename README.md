# Intent Verification Gate

A public Codex plugin marketplace for the `intent-verification-gate` skill.

The skill helps agents make meaningful changes auditable by saving the raw user
request, a best-estimate intent statement, a change manifest, verification
evidence, phased review output, machine-readable gate status, and rerunnable
review history.

This repository intentionally excludes local run history, project-specific
artifacts, private workspace files, Python cache files, and machine-specific
paths.

## Install With Codex

```bash
codex plugin marketplace add mike123456789009/intent-verification-gate
codex plugin marketplace upgrade intent-verification-gate
```

## Use Directly As A Skill

If your agent runtime consumes Agent Skills folders directly, use:

```text
plugins/intent-verification-gate/skills/intent-verification-gate/
```

An uploadable skill archive is also available at:

```bash
dist/intent-verification-gate-skill.zip
```

## What Is Included

- `plugins/intent-verification-gate/.codex-plugin/plugin.json`
- `plugins/intent-verification-gate/skills/intent-verification-gate/SKILL.md`
- `scripts/intent_run.py` helper CLI
- `assets/templates/` artifact templates
- `references/gate-spec.md` exact gate format and scoring rules
- `tests/` regression coverage for the helper CLI

## Public Package Hygiene

Before publication, the package is checked for:

- absolute local filesystem paths
- local run history under `docs/intent-verification/runs`
- Python caches and `.pyc` files
- private repository names and private license markers
- obvious secret/token/password environment names

## License

MIT
