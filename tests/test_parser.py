from __future__ import annotations

import unittest

from src.parser import InputFormatError, parse_input


class ParseInputTests(unittest.TestCase):
    def test_accepts_whitespace_and_integer_distance(self) -> None:
        graph = parse_input([" 1 , 2 , 4 \n", "\n", "2,3,3.5\n"])

        self.assertEqual(sorted(graph), [1, 2, 3])
        self.assertEqual([(edge.to, edge.distance) for edge in graph[1]], [(2, 4.0)])
        self.assertEqual(
            [(edge.to, edge.distance) for edge in graph[2]],
            [(1, 4.0), (3, 3.5)],
        )

    def test_rejects_missing_fields(self) -> None:
        with self.assertRaisesRegex(InputFormatError, "expected"):
            parse_input(["1,2\n"])

    def test_rejects_non_numeric_distance(self) -> None:
        with self.assertRaisesRegex(InputFormatError, "distance must be a number"):
            parse_input(["1,2,abc\n"])

    def test_rejects_negative_distance(self) -> None:
        with self.assertRaisesRegex(InputFormatError, "non-negative"):
            parse_input(["1,2,-1\n"])

    def test_rejects_non_positive_station_id(self) -> None:
        with self.assertRaisesRegex(InputFormatError, "positive integers"):
            parse_input(["0,2,1\n"])


if __name__ == "__main__":
    unittest.main()

