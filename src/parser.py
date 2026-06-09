from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


class InputFormatError(ValueError):
    """Raised when an input line does not match the expected format."""


@dataclass(frozen=True)
class Edge:
    to: int
    distance: float
    edge_id: int


Graph = dict[int, list[Edge]]


def parse_input(lines: Iterable[str]) -> Graph:
    graph: Graph = {}
    edge_id = 0

    for line_number, raw_line in enumerate(lines, start=1):
        stripped = raw_line.strip()
        if not stripped:
            continue

        parts = [part.strip() for part in raw_line.split(",")]
        if len(parts) != 3:
            raise InputFormatError(
                f"line {line_number}: expected 'start, end, distance'"
            )

        start_text, end_text, distance_text = parts

        try:
            start = int(start_text)
            end = int(end_text)
        except ValueError as exc:
            raise InputFormatError(
                f"line {line_number}: station IDs must be integers"
            ) from exc

        if start <= 0 or end <= 0:
            raise InputFormatError(
                f"line {line_number}: station IDs must be positive integers"
            )

        try:
            distance = float(distance_text)
        except ValueError as exc:
            raise InputFormatError(
                f"line {line_number}: distance must be a number"
            ) from exc

        if distance < 0:
            raise InputFormatError(
                f"line {line_number}: distance must be non-negative"
            )

        graph.setdefault(start, []).append(Edge(to=end, distance=distance, edge_id=edge_id))
        graph.setdefault(end, []).append(Edge(to=start, distance=distance, edge_id=edge_id))
        edge_id += 1

    for neighbors in graph.values():
        neighbors.sort(key=lambda edge: (edge.to, edge.edge_id))

    return graph

