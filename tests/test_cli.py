from __future__ import annotations

import subprocess
import sys
import unittest


class CliTests(unittest.TestCase):
    def test_reads_stdin_and_writes_path(self) -> None:
        completed = subprocess.run(
            [sys.executable, "-m", "src.main"],
            input="1,2,5\n2,3,6\n",
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(completed.returncode, 0)
        self.assertEqual(completed.stdout, "1\n2\n3\n")
        self.assertEqual(completed.stderr, "")

    def test_reports_invalid_input_to_stderr(self) -> None:
        completed = subprocess.run(
            [sys.executable, "-m", "src.main"],
            input="1,2\n",
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(completed.returncode, 1)
        self.assertEqual(completed.stdout, "")
        self.assertIn("input error:", completed.stderr)


if __name__ == "__main__":
    unittest.main()

