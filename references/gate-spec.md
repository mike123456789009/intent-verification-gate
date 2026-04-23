# Intent Verification Gate Spec

Use this reference when you need exact file formats, reviewer packet rules, the scoring rubric, validation expectations, or pass/fail rules.

## Repo config

Save project-local configuration at `docs/intent-verification/gate.config.json` unless the repo deliberately uses another artifact root.

```json
{
  "artifactsRoot": "docs/intent-verification",
  "mode": "strict",
  "profile": "web-app",
  "requiredChecks": ["lint", "typecheck", "test", "build"],
  "visualQa": true,
  "deployVerification": false,
  "reviewMode": "blind-intent",
  "staleReviewDetection": true
}
```

Modes:

- `strict`: full phased review, score threshold 90, required checks enforced.
- `standard`: full phased review, score threshold 90, repo checks recommended by config.
- `lightweight`: durable request, intent, manifest, and evidence required; review may be optional for early trials or low-risk work.

Profiles provide defaults only. Repo config overrides them.

## Trigger Decision

Save this in `trigger-decision.md`:

```text
TRIGGER DECISION

Decision:
Used / Skipped

Reason:
...

Strictness mode:
strict / standard / lightweight

Risk level:
low / medium / high

Project config used:
...
```

Use this for borderline cases so future agents can see why the gate was used or skipped.

## Best Estimate Statement of User Intent

Save this in `intent.md`:

```text
BEST ESTIMATE STATEMENT OF USER INTENT

Primary goal:
...

Explicit requests:
1. ...
2. ...
3. ...

Implied constraints:
- ...
- ...

Non-goals:
- ...
- ...

Risk of misinterpretation:
- Phrase: "..."
  Chosen interpretation: ...
```

## Change Manifest

Save this in `change-manifest.md`:

```text
CHANGE MANIFEST

Changed:
1. ...
2. ...

Removed:
1. ...
2. ...

Intentionally unchanged:
1. ...
2. ...

Added but not explicitly requested:
1. ...
   Reason:
2. ...
   Reason:

Scope changes or deviations:
1. ...
   Reason:
   Risk:

Unavoidable deviations:
1. ...
   Reason:
   Smallest follow-up:

Files changed:
1. ...
2. ...

Evidence summary:
1. ...
2. ...
```

Keep the manifest descriptive, not argumentative.

## Evidence

Save this in `evidence.md`:

```text
# Evidence

## Changed Files

1. ...

## Relevant Diffs

1. ...

## Commands Run

1. Command:
   Result:

## Test Results

1. ...

## Visual QA

1. ...

## Deployment Verification

1. ...

## Behavior Evidence

1. ...

## Known Limitations

1. ...

## Intentionally Not Checked

1. ...
```

When visual QA or deployment verification does not apply, say so explicitly and explain why.

## Reviewer packet rules

Use `review-packet` to generate clean context.

### Phase 1: blind intent

Give the reviewer only:

1. the verbatim user request

The reviewer must write its own independent intent before seeing the main agent's intent.

### Phase 2: intent comparison

Give the reviewer only:

1. the verbatim user request
2. the reviewer independent intent from phase 1
3. the main agent's `intent.md`

The reviewer must compare the two and identify omitted requests, invented constraints, softened wording, and ambiguity handling issues.

### Phase 3: implementation review

Give the reviewer only:

1. the corrected intent from phase 2
2. the Change Manifest
3. the Evidence

The reviewer grades implementation against corrected intent.

Do not give the reviewer:

- the main agent's justification
- persuasive framing
- the main agent's private plan
- leniency instructions
- target scores

## Reviewer scoring rubric

Score each category from 0 to 100:

### Intent Extraction

- 100 = reviewer blind intent captures the user request precisely, including implied constraints
- 90 = minor wording loss, no practical misunderstanding
- 75 = mostly correct but one meaningful interpretive miss
- 50 = mixed understanding, likely to produce noticeable misalignment
- 25 = major misunderstanding of the real goal
- 0 = wrong problem solved

### Intent Comparison

- 100 = main intent matches corrected reviewer intent with no omissions or invented constraints
- 90 = one tiny non-material mismatch only
- 75 = one meaningful omission, invention, or softened constraint
- 50 = multiple meaningful differences
- 25 = main intent is weakly related to the user's real intent
- 0 = main intent frames the wrong problem

### Alignment

- 100 = changes directly produce the requested outcome according to corrected intent
- 90 = essentially aligned, only tiny non-material mismatch
- 75 = mostly aligned but one meaningful miss remains
- 50 = partial compliance, mixed with conflicting decisions
- 25 = weak alignment, spirit not honored
- 0 = changes go against the request

### Completeness

- 100 = all meaningful parts addressed
- 90 = one tiny edge omission only
- 75 = one meaningful part missing
- 50 = multiple requested parts missing
- 25 = most of the request incomplete
- 0 = barely attempted

### Scope Discipline

- 100 = no unrelated or substitutive changes
- 90 = one minor extra change with negligible impact
- 75 = one noticeable but non-fatal extra change
- 50 = extra changes materially dilute the request
- 25 = work is dominated by unrelated or substitutive changes
- 0 = major pattern of freelancing

### Constraint Obedience

- 100 = all explicit and implied constraints respected
- 90 = trivial non-material slip only
- 75 = one meaningful constraint softened
- 50 = one meaningful constraint violated
- 25 = multiple constraints violated
- 0 = core constraint directly violated

## Reviewer output

Save each review round in its own `review-0N.md` file:

```text
REVIEW

Review round:
...

Phase 1 - Blind Intent

Reviewer independent intent:
Primary goal:
...

Explicit requests:
1. ...

Implied constraints:
- ...

Non-goals:
- ...

Ambiguity risks:
- ...

Phase 2 - Intent Comparison

Main intent accuracy: __/100

Omitted requests:
1. ...

Invented constraints:
1. ...

Softened or distorted wording:
1. ...

Ambiguity handling:
1. ...

Corrected intent for implementation review:
...

Phase 3 - Implementation Review

Intent Extraction: __/100
Intent Comparison: __/100
Alignment: __/100
Completeness: __/100
Scope Discipline: __/100
Constraint Obedience: __/100

Per-request assessment:
1. Request: ...
   Status: Met / Partially Met / Missed
   Score: __/100
   Reason: ...

Rejected-pattern check:
- Any rejected pattern reintroduced in equivalent form? Yes/No
- If yes, where: ...

Extra-changes check:
- Any additions not explicitly requested? Yes/No
- If yes, list: ...

Core constraint check:
- Any core constraint violated? Yes/No
- If yes, list: ...

Blocking issues preventing pass:
1. ...

Minimum changes required to pass:
1. ...

Final verdict:
Pass / Fail
```

## Pass/fail rule

Strict and standard modes do not pass unless all of these are true:

- Intent Extraction >= 90
- Intent Comparison >= 90
- Alignment >= 90
- Completeness >= 90
- Scope Discipline >= 90
- Constraint Obedience >= 90
- no explicit request is marked `Missed`
- no core constraint is violated
- no rejected pattern is reintroduced in equivalent form
- blind-intent review exists
- intent-comparison review exists
- implementation review exists
- evidence includes required checks from repo config
- latest review is not stale

If any score is below threshold, revise the work and run another review round.

## Stale review detection

A review is stale if any of these changed after the latest review file was written:

- `request.md`
- `intent.md`
- `change-manifest.md`
- `evidence.md`
- files referenced by the manifest or evidence that exist on disk

The helper records status in `gate-status.json` and reports stale reviews during validation.

## Blocker report

If an honest passing result requires external input you do not have, save:

```text
BLOCKER REPORT

Blocked requirement:
...

Why this prevents a passing result:
...

What exact external input is needed:
...

Smallest human action needed:
...

Interim status:
Blocked
```

## Gate status

`gate-status.json` is machine-readable state. Expected statuses:

- `initialized`
- `implemented`
- `reviewing`
- `passed`
- `failed`
- `blocked`
- `stale`

The status file does not replace human-readable artifacts.

## Final return

Separate these items explicitly in the final return:

1. what the user asked for
2. what changed
3. anything intentionally not changed
4. any unavoidable deviation
5. reviewer scores
6. validation command and result
7. artifact run path
