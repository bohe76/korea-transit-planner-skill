from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "korea-transit-planner"
SPEC = importlib.util.spec_from_file_location("validator", ROOT / "scripts" / "validate.py")
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)
AGENT_SPEC = importlib.util.spec_from_file_location(
    "agent_skill_validator", ROOT / "scripts" / "validate_agent_skill.py"
)
assert AGENT_SPEC and AGENT_SPEC.loader
agent_skill_validator = importlib.util.module_from_spec(AGENT_SPEC)
AGENT_SPEC.loader.exec_module(agent_skill_validator)


class SkillContractTests(unittest.TestCase):
    def test_agent_skills_standard_and_packaged_references(self):
        self.assertEqual([], agent_skill_validator.agent_skill_errors(PACKAGE))

    def test_repository_contract_is_green(self):
        self.assertEqual([], validator.contract_errors(ROOT))

    def test_frontmatter_identity_and_version(self):
        values = validator.parse_frontmatter((PACKAGE / "SKILL.md").read_text(encoding="utf-8"))
        self.assertEqual("korea-transit-planner", values["name"])
        self.assertEqual("0.1.0", values["version"])
        self.assertEqual("MIT", values["license"])

    def test_explicit_origin_has_precedence_and_no_default(self):
        text = (PACKAGE / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Explicit origin; it overrides every inferred or stored location.", text)
        self.assertIn("Do not use this skill until an origin is known.", text)
        self.assertNotIn("Default origin", text)
        self.assertNotIn("default origin", text)

    def test_gtx_is_strictly_opt_in(self):
        skill = (PACKAGE / "SKILL.md").read_text(encoding="utf-8")
        gtx = (PACKAGE / "references" / "gtx-routing.md").read_text(encoding="utf-8")
        self.assertIn("If and only if the user explicitly mentions GTX or names a GTX station", skill)
        self.assertIn("Otherwise perform no GTX lookup or comparison.", skill)
        self.assertIn("Never research or compare GTX proactively", gtx)

    def test_required_modes_are_covered(self):
        text = (PACKAGE / "SKILL.md").read_text(encoding="utf-8")
        for term in ("ordinary subway", "city/intercity bus", "마을버스", "누리버스/DRT", "walking", "taxi", "mixed"):
            with self.subTest(term=term):
                self.assertIn(term, text)

    def test_private_literal_probe_is_detected_without_storing_it(self):
        private_value = "".join(chr(value) for value in (0xBC14, 0xC6B0, 0xBA2C))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "probe.md").write_text(private_value, encoding="utf-8")
            findings = validator.privacy_findings(root)
        self.assertTrue(any("private-street-fragment" in item for item in findings))

    def test_secret_probe_is_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "probe.txt").write_text("api_key=" + "x" * 24, encoding="utf-8")
            findings = validator.privacy_findings(root)
        self.assertTrue(any("generic-secret-assignment" in item for item in findings))

    def test_every_installable_reference_is_linked_and_present(self):
        skill = (PACKAGE / "SKILL.md").read_text(encoding="utf-8")
        for rel in (
            "references/map-routing.md",
            "references/source-verification.md",
            "references/gtx-routing.md",
            "references/local-modes.md",
            "examples/route-briefing.md",
        ):
            with self.subTest(rel=rel):
                self.assertIn(f"]({rel})", skill)
                self.assertTrue((PACKAGE / rel).is_file())


if __name__ == "__main__":
    unittest.main()
