"""Golden and integration tests with a deterministic fake IWE command."""
from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "iwe_report.py"
FIXTURE = REPO / "tests" / "fixtures"
FAKE = FIXTURE / "fake_iwe.py"
LIBRARY = FIXTURE / "library"
GOLDEN = REPO / "tests" / "golden" / "summary.md"


class ReportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.workspace = Path(self.temp.name)
        (self.workspace / ".iwe").mkdir()
        (self.workspace / ".iwe" / "config.toml").write_text(f'[library]\npath = "{LIBRARY}"\n')
        # Use library.path relative to workspace to match real IWE configuration.
        import shutil
        shutil.copytree(LIBRARY, self.workspace / "docs")
        (self.workspace / ".iwe" / "config.toml").write_text('[library]\npath = "docs"\n')

    def tearDown(self):
        self.temp.cleanup()

    def run_cli(self, *args, stdin=None):
        cmd = [sys.executable, str(SCRIPT), "--workspace", str(self.workspace), "--iwe", str(FAKE), *args]
        return subprocess.run(cmd, input=stdin, capture_output=True, text=True)

    def test_golden_directory_summary(self):
        actual = self.run_cli("--exclude-dir", "archive")
        self.assertEqual(actual.returncode, 0, actual.stderr)
        self.assertEqual(actual.stdout, GOLDEN.read_text())

    def test_current_workspace_configuration(self):
        (self.workspace / ".iwe" / "config.toml").write_text('[workspace]\npath = "docs"\n')
        actual = self.run_cli("--exclude-dir", "archive", "--strict")
        self.assertEqual(actual.returncode, 0, actual.stderr)
        self.assertEqual(actual.stdout, GOLDEN.read_text())

    def test_exclude_file_and_files_json(self):
        result = self.run_cli("--exclude-from", str(FIXTURE / "excludes.txt"), "--report", "files", "--format", "json")
        self.assertEqual(result.returncode, 0, result.stderr)
        parsed = json.loads(result.stdout)
        self.assertEqual([x["file"] for x in parsed], ["guides/intro.md", "reference/service.md"])
        self.assertEqual(parsed[0]["items"], 2)

    def test_scan_one_directory(self):
        result = self.run_cli("--scan", "guides", "--report", "headings", "--format", "csv")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("guides/intro.md", result.stdout)
        self.assertNotIn("reference/service.md", result.stdout)

    def test_stdin_keys_and_exclusions(self):
        result = self.run_cli("--keys-from", "-", "--exclude-dir", "archive", "--report", "files", "--format", "json", stdin="archive/old\nguides/intro\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([row["file"] for row in json.loads(result.stdout)], ["guides/intro.md"])

    def test_output_file_no_stdout(self):
        output = self.workspace / "output" / "report.json"
        result = self.run_cli("--exclude-dir", "archive", "--report", "summary", "--format", "json", "-o", str(output))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertEqual(json.loads(output.read_text())[0]["directory"], ".")

    def test_missing_iwe_is_error(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "--workspace", str(self.workspace), "--iwe", "_missing_iwe_bin_xyz_"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("IWE executable not found", result.stderr)

    def test_strict_missing_key(self):
        (self.workspace / "docs" / "guides" / "not_indexed.md").write_text("# Unindexed\n")
        result = self.run_cli("--scan", "guides", "--strict")
        self.assertEqual(result.returncode, 2)
        self.assertIn("did not return", result.stderr)

    def test_no_content_parse(self):
        # Deliberately malformed Markdown is okay: mock IWE determines structure.
        (self.workspace / "docs" / "guides" / "intro.md").write_text("some ??? non-Markdown\n")
        result = self.run_cli("--scan", "guides", "--format", "json")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)[0]["files"], 1)

    def test_ignored_hidden_directory(self):
        hidden = self.workspace / "docs" / ".hidden"
        hidden.mkdir()
        (hidden / "draft.md").write_text("# Hidden\n")
        result = self.run_cli("--exclude-dir", "archive", "--report", "files", "--format", "json")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(json.loads(result.stdout)), 2)


if __name__ == "__main__":
    unittest.main()
