# Intent Verification Gate

A reusable Codex skill for making meaningful AI-agent changes auditable.

The gate records the raw user request, the agent's best estimate of intent, a change manifest, verification evidence, phased reviewer output, and machine-readable status. It is designed for coding-agent workflows where "the agent said it understood" is not enough.

## Why This Exists

AI agents can be internally consistent while still solving the wrong problem. Intent Verification Gate forces the review to ask a better question:

> Did the agent correctly understand the user, preserve the scope, prove the work, and pass an independent review?

The reviewer starts with a blind intent pass before seeing the main agent's interpretation, which reduces anchoring bias.

## What It Includes

- `SKILL.md`: the Codex skill instructions
- `scripts/intent_run.py`: helper CLI for runs, validation, packets, install, diagnosis, and indexes
- `assets/templates/`: request, intent, evidence, review, blocker, config, and README templates
- `references/gate-spec.md`: full artifact and scoring spec
- `tests/`: regression tests for the helper workflow

## Install Into Codex

Clone or download this repository, then copy it into your Codex skills directory:

```bash
mkdir -p "$HOME/.codex/skills"
cp -R intent-verification-gate "$HOME/.codex/skills/intent-verification-gate"
```

Then invoke it explicitly in a Codex task:

```text
$intent-verification-gate
```

For recurring use in a project, add a short rule to that project's `AGENTS.md` telling agents when to use `$intent-verification-gate`.

## Helper CLI

Set the helper path:

```bash
export IVG="$HOME/.codex/skills/intent-verification-gate/scripts/intent_run.py"
```

Diagnose a project:

```bash
python3 "$IVG" diagnose --repo . --json
```

Install project-local config and docs:

```bash
python3 "$IVG" install --repo . --json
```

Start a run:

```bash
python3 "$IVG" init --repo . --slug meaningful-change --json
```

Generate phased reviewer packets:

```bash
python3 "$IVG" review-packet --phase blind-intent --run-dir /path/to/run
python3 "$IVG" review-packet --phase intent-comparison --run-dir /path/to/run
python3 "$IVG" review-packet --phase implementation --run-dir /path/to/run
```

Validate before claiming success:

```bash
python3 "$IVG" validate --run-dir /path/to/run --json
```

Update the browseable run index:

```bash
python3 "$IVG" index --repo . --json
```

## Review Flow

1. Save the verbatim user request in `request.md`.
2. Save the main agent's best estimate of user intent in `intent.md`.
3. Save a trigger decision explaining why the gate was used.
4. Implement the change.
5. Save a change manifest and verification evidence.
6. Review in three phases:
   - `blind-intent`: reviewer sees only the raw request.
   - `intent-comparison`: reviewer compares blind intent to the main agent intent.
   - `implementation`: reviewer grades the work against corrected intent.
7. Run validation. Strict and standard modes require 90+ scores and no missed explicit requests.

## Test

```bash
python3 -m py_compile scripts/intent_run.py tests/test_intent_run.py
python3 -m unittest discover -s tests -v
```

## Status

This is an early public release. The workflow is intentionally file-based so agents and humans can inspect what happened without depending on chat logs.

## License

MIT
