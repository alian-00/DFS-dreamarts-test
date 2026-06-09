from __future__ import annotations

import sys

from src.parser import InputFormatError, parse_input
from src.solver import find_longest_path


def main() -> int:
    try:
        graph = parse_input(sys.stdin)
        path = find_longest_path(graph)
    except InputFormatError as exc:
        print(f"input error: {exc}", file=sys.stderr)
        return 1

    if path:
        sys.stdout.write("\n".join(str(node) for node in path))
        sys.stdout.write("\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

