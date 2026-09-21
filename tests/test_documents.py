"""Guard the common lesson structure and display-equation formatting."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class DocumentationTests(unittest.TestCase):
    def test_consistent_lesson_sections(self):
        expected = ["Learning goal", "Model and assumptions", "Inputs", "Equations", "Symbols",
                    "Run", "Expected behavior", "Experiments", "Project connections"]
        lessons = sorted(ROOT.glob("*/tier-*/README.md"))
        self.assertEqual(len(lessons), 9)
        for path in lessons:
            self.assertEqual(re.findall(r"^## (.+)$", path.read_text(), re.M), expected, str(path))

    def test_display_equations_have_no_blank_lines_and_balanced_braces(self):
        for path in ROOT.rglob("*.md"):
            if "results" in path.parts:
                continue
            text = re.sub(r"```.*?```", "", path.read_text(), flags=re.S)
            inside, depth = False, 0
            for line in text.splitlines():
                if line.strip() == "$$":
                    if inside:
                        self.assertEqual(depth, 0, str(path))
                    inside = not inside
                    continue
                if inside:
                    self.assertTrue(line.strip(), "blank line inside math: " + str(path))
                    depth += line.count("{") - line.count("}")
                    self.assertGreaterEqual(depth, 0, str(path))
            self.assertFalse(inside, "unclosed math block: " + str(path))

    def test_relative_document_links_exist(self):
        for path in ROOT.rglob("*.md"):
            if "results" in path.parts:
                continue
            for link in re.findall(r"\]\(([^)]+)\)", path.read_text()):
                if "://" in link or link.startswith("#"):
                    continue
                self.assertTrue((path.parent / link.split("#")[0]).exists(), (str(path), link))


if __name__ == "__main__":
    unittest.main()
