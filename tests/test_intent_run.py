from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "intent_run.py"
)


def run_cli(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
    )
    if check and result.returncode != 0:
        raise AssertionError(
            f"command failed: {result.args}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def run_json(*args: str, check: bool = True) -> dict:
    result = run_cli(*args, "--json", check=check)
    if not result.stdout.strip():
        return {}
    return json.loads(result.stdout)


def write_filled_artifacts(run_dir: Path, repo: Path) -> Path:
    changed_file = repo / "src" / "app.py"
    changed_file.parent.mkdir(parents=True, exist_ok=True)
    changed_file.write_text("print('hello')\n")

    (run_dir / "request.md").write_text(
        "# Verbatim User Request\n\nBuild and verify the sample behavior.\n"
    )
    (run_dir / "intent.md").write_text(
        "\n".join(
            [
                "BEST ESTIMATE STATEMENT OF USER INTENT",
                "",
                "Primary goal:",
                "Build and verify the sample behavior.",
                "",
                "Explicit requests:",
                "1. Build the sample behavior.",
                "2. Verify the sample behavior.",
                "",
                "Implied constraints:",
                "- Keep the change scoped.",
                "",
                "Non-goals:",
                "- Do not add unrelated features.",
                "",
                "Risk of misinterpretation:",
                "- Phrase: \"sample behavior\"",
                "  Chosen interpretation: the fixture behavior in src/app.py.",
                "",
            ]
        )
    )
    (run_dir / "trigger-decision.md").write_text(
        "\n".join(
            [
                "TRIGGER DECISION",
                "",
                "Decision:",
                "Used",
                "",
                "Reason:",
                "Behavior and verification workflow changed.",
                "",
                "Strictness mode:",
                "strict",
                "",
                "Risk level:",
                "medium",
                "",
                "Project config used:",
                "Default small-script config.",
                "",
            ]
        )
    )
    (run_dir / "change-manifest.md").write_text(
        "\n".join(
            [
                "CHANGE MANIFEST",
                "",
                "Changed:",
                "1. src/app.py now contains sample behavior.",
                "",
                "Removed:",
                "1. Nothing removed.",
                "",
                "Intentionally unchanged:",
                "1. Existing artifact layout.",
                "",
                "Added but not explicitly requested:",
                "1. No extras added.",
                "   Reason: Scope was preserved.",
                "",
                "Scope changes or deviations:",
                "1. No scope changes.",
                "   Reason: Not applicable.",
                "   Risk: None.",
                "",
                "Unavoidable deviations:",
                "1. No unavoidable deviations.",
                "   Reason: Not applicable.",
                "   Smallest follow-up: None.",
                "",
                "Files changed:",
                "1. src/app.py",
                "2. docs/intent-verification",
                "",
                "Evidence summary:",
                "1. test command passed.",
                "",
            ]
        )
    )
    (run_dir / "evidence.md").write_text(
        "\n".join(
            [
                "# Evidence",
                "",
                "## Changed Files",
                "",
                "1. src/app.py",
                "2. docs/intent-verification",
                "",
                "## Relevant Diffs",
                "",
                "1. src/app.py contains the sample behavior.",
                "",
                "## Commands Run",
                "",
                "1. Command: python -m unittest",
                "   Result: test passed.",
                "",
                "## Test Results",
                "",
                "1. test passed.",
                "",
                "## Visual QA",
                "",
                "1. Not applicable for this non-visual script.",
                "",
                "## Deployment Verification",
                "",
                "1. Not applicable for this local script.",
                "",
                "## Behavior Evidence",
                "",
                "1. The sample behavior file exists.",
                "",
                "## Known Limitations",
                "",
                "1. No known limitations.",
                "",
                "## Intentionally Not Checked",
                "",
                "1. No production deployment was checked because this is local only.",
                "",
            ]
        )
    )
    return changed_file


def write_passing_review(review_path: Path) -> None:
    review_path.write_text(
        "\n".join(
            [
                "REVIEW",
                "",
                "Review round:",
                "1",
                "",
                "Phase 1 - Blind Intent",
                "",
                "Reviewer independent intent:",
                "Primary goal:",
                "Build and verify the sample behavior.",
                "",
                "Explicit requests:",
                "1. Build the sample behavior.",
                "2. Verify the sample behavior.",
                "",
                "Implied constraints:",
                "- Keep scope tight.",
                "",
                "Non-goals:",
                "- Do not add unrelated features.",
                "",
                "Ambiguity risks:",
                "- No material ambiguity remains.",
                "",
                "Phase 2 - Intent Comparison",
                "",
                "Main intent accuracy: 95/100",
                "",
                "Omitted requests:",
                "1. No omitted requests.",
                "",
                "Invented constraints:",
                "1. No invented constraints.",
                "",
                "Softened or distorted wording:",
                "1. No distorted wording.",
                "",
                "Ambiguity handling:",
                "1. Ambiguity was handled correctly.",
                "",
                "Corrected intent for implementation review:",
                "Build and verify the sample behavior while keeping scope tight.",
                "",
                "Phase 3 - Implementation Review",
                "",
                "Intent Extraction: 95/100",
                "Intent Comparison: 95/100",
                "Alignment: 96/100",
                "Completeness: 95/100",
                "Scope Discipline: 97/100",
                "Constraint Obedience: 95/100",
                "",
                "Per-request assessment:",
                "1. Request: Build the sample behavior.",
                "   Status: Met",
                "   Score: 96/100",
                "   Reason: The file was created.",
                "",
                "2. Request: Verify the sample behavior.",
                "   Status: Met",
                "   Score: 95/100",
                "   Reason: The test evidence is present.",
                "",
                "Rejected-pattern check:",
                "- Any rejected pattern reintroduced in equivalent form? No",
                "- If yes, where: None.",
                "",
                "Extra-changes check:",
                "- Any additions not explicitly requested? No",
                "- If yes, list: None.",
                "",
                "Core constraint check:",
                "- Any core constraint violated? No",
                "- If yes, list: None.",
                "",
                "Blocking issues preventing pass:",
                "1. None.",
                "",
                "Minimum changes required to pass:",
                "1. None.",
                "",
                "Final verdict:",
                "Pass",
                "",
            ]
        )
    )


class IntentRunTests(unittest.TestCase):
    def test_init_next_review_and_blocker_regression(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            payload = run_json(
                "init",
                "--repo",
                str(repo),
                "--slug",
                "Hello World",
                "--timestamp",
                "20260423T000000Z",
            )
            run_dir = Path(payload["run_dir"])
            self.assertTrue((run_dir / "request.md").exists())
            self.assertTrue((run_dir / "intent.md").exists())
            self.assertTrue((run_dir / "change-manifest.md").exists())
            self.assertTrue((run_dir / "evidence.md").exists())
            self.assertTrue((run_dir / "trigger-decision.md").exists())
            self.assertTrue((run_dir / "gate-status.json").exists())

            first = run_json("next-review", "--run-dir", str(run_dir))
            second = run_json("next-review", "--run-dir", str(run_dir))
            self.assertEqual(Path(first["review_path"]).name, "review-01.md")
            self.assertEqual(Path(second["review_path"]).name, "review-02.md")

            blocker = run_json("blocker", "--run-dir", str(run_dir))
            self.assertEqual(Path(blocker["blocker_path"]).name, "blocker-report.md")

    def test_diagnose_and_install_seed_repo_config(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "package.json").write_text(
                json.dumps(
                    {
                        "scripts": {
                            "lint": "eslint .",
                            "typecheck": "tsc --noEmit",
                            "test": "vitest",
                            "build": "vite build",
                        },
                        "dependencies": {"react": "latest"},
                        "devDependencies": {"vite": "latest"},
                    }
                )
            )
            diagnosis = run_json("diagnose", "--repo", str(repo))
            self.assertEqual(diagnosis["config"]["profile"], "web-app")
            self.assertEqual(diagnosis["config"]["packageManager"], "npm")
            self.assertEqual(diagnosis["config"]["framework"], "vite")

            installed = run_json("install", "--repo", str(repo))
            config_path = Path(installed["config_path"])
            self.assertTrue(config_path.exists())
            config = json.loads(config_path.read_text())
            self.assertEqual(config["requiredChecks"], ["lint", "typecheck", "test", "build"])
            self.assertTrue((repo / "docs" / "intent-verification" / "README.md").exists())

    def test_review_packet_blind_phase_excludes_main_intent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            payload = run_json("init", "--repo", str(repo), "--slug", "packet")
            run_dir = Path(payload["run_dir"])
            (run_dir / "request.md").write_text("User wants the independent request.\n")
            (run_dir / "intent.md").write_text("SECRET MAIN INTENT SHOULD NOT APPEAR.\n")

            blind = run_cli("review-packet", "--run-dir", str(run_dir), "--phase", "blind-intent")
            self.assertIn("User wants the independent request", blind.stdout)
            self.assertNotIn("SECRET MAIN INTENT", blind.stdout)

            comparison = run_cli(
                "review-packet",
                "--run-dir",
                str(run_dir),
                "--phase",
                "intent-comparison",
            )
            self.assertIn("SECRET MAIN INTENT", comparison.stdout)

    def test_validate_fails_on_template_placeholders(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            payload = run_json("init", "--repo", str(repo), "--slug", "bad")
            run_dir = Path(payload["run_dir"])
            result = run_json("validate", "--run-dir", str(run_dir), check=False)
            self.assertFalse(result["ok"])
            self.assertEqual(result["status"], "failed")
            self.assertTrue(any("request.md" in issue for issue in result["issues"]))

    def test_validate_passes_filled_strict_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            payload = run_json("init", "--repo", str(repo), "--slug", "pass")
            run_dir = Path(payload["run_dir"])
            write_filled_artifacts(run_dir, repo)
            review = Path(run_json("next-review", "--run-dir", str(run_dir))["review_path"])
            write_passing_review(review)

            result = run_json("validate", "--run-dir", str(run_dir))
            self.assertTrue(result["ok"])
            self.assertEqual(result["status"], "passed")
            self.assertEqual(result["scores"]["Intent Extraction"], 95)

            indexed = run_json("index", "--repo", str(repo))
            self.assertEqual(indexed["run_count"], 1)
            self.assertTrue((repo / "docs" / "intent-verification" / "index.json").exists())
            self.assertTrue((repo / "docs" / "intent-verification" / "index.md").exists())
            after_index = run_json("validate", "--run-dir", str(run_dir))
            self.assertTrue(after_index["ok"])

    def test_validate_detects_stale_review(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            payload = run_json("init", "--repo", str(repo), "--slug", "stale")
            run_dir = Path(payload["run_dir"])
            changed_file = write_filled_artifacts(run_dir, repo)
            review = Path(run_json("next-review", "--run-dir", str(run_dir))["review_path"])
            write_passing_review(review)
            first = run_json("validate", "--run-dir", str(run_dir))
            self.assertTrue(first["ok"])

            time.sleep(1.1)
            changed_file.write_text("print('changed after review')\n")
            second = run_json("validate", "--run-dir", str(run_dir), check=False)
            self.assertFalse(second["ok"])
            self.assertEqual(second["status"], "stale")


if __name__ == "__main__":
    unittest.main()
