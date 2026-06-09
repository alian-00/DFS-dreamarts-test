from __future__ import annotations

import unittest

from src.parser import parse_input
from src.solver import find_longest_path


class FindLongestPathTests(unittest.TestCase):
    def test_sample_graph_returns_deterministic_longest_path(self) -> None:
        graph = parse_input(
            [
                "1, 2, 8.54\n",
                "2, 3, 3.11\n",
                "3, 1, 2.19\n",
                "3, 4, 4\n",
                "4, 1, 1.4\n",
            ]
        )

        self.assertEqual(find_longest_path(graph), [1, 2, 3, 4])

    def test_triangle_prefers_longer_simple_path(self) -> None:
        graph = parse_input(["1,2,1\n", "2,3,5\n", "1,3,2\n"])

        self.assertEqual(find_longest_path(graph), [1, 3, 2])

    def test_handles_duplicate_edges_and_self_loops(self) -> None:
        graph = parse_input(["1,1,10\n", "1,2,3\n", "1,2,4\n", "2,3,5\n"])

        self.assertEqual(find_longest_path(graph), [1, 2, 3])

    def test_selects_best_component(self) -> None:
        graph = parse_input(["1,2,1\n", "3,4,10\n", "4,5,20\n"])

        self.assertEqual(find_longest_path(graph), [3, 4, 5])

    def test_returns_empty_path_for_empty_input(self) -> None:
        self.assertEqual(find_longest_path({}), [])


if __name__ == "__main__":
    unittest.main()
