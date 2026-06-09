from __future__ import annotations

from dataclasses import dataclass

from src.parser import Edge, Graph


@dataclass(frozen=True)
class PathResult:
    nodes: list[int]
    total_distance: float


def find_longest_path(graph: Graph) -> list[int]:
    if not graph:
        return []

    best = PathResult(nodes=[], total_distance=0.0)

    for component_nodes, component_edge_weights in _connected_components(graph):
        component_total_weight = sum(component_edge_weights.values())
        component_best = PathResult(nodes=[], total_distance=0.0)

        for start in component_nodes:
            start_result = search_from(start, graph, component_total_weight)
            if start_result.total_distance > component_best.total_distance:
                component_best = start_result

        if component_best.total_distance > best.total_distance:
            best = component_best
        elif not best.nodes and component_best.nodes:
            best = component_best

    return best.nodes


def search_from(start: int, graph: Graph, component_total_weight: float) -> PathResult:
    best = PathResult(nodes=[start], total_distance=0.0)
    visited = {start}

    def dfs(current: int, path: list[int], distance: float, used_weight: float) -> None:
        nonlocal best

        if distance > best.total_distance:
            best = PathResult(nodes=path.copy(), total_distance=distance)

        remaining_upper_bound = distance + (component_total_weight - used_weight)
        if remaining_upper_bound <= best.total_distance:
            return

        for edge in graph.get(current, []):
            if edge.to in visited:
                continue

            visited.add(edge.to)
            path.append(edge.to)
            dfs(
                current=edge.to,
                path=path,
                distance=distance + edge.distance,
                used_weight=used_weight + edge.distance,
            )
            path.pop()
            visited.remove(edge.to)

    dfs(start, [start], 0.0, 0.0)
    return best


def _connected_components(
    graph: Graph,
) -> list[tuple[list[int], dict[int, float]]]:
    seen: set[int] = set()
    components: list[tuple[list[int], dict[int, float]]] = []

    for start in sorted(graph):
        if start in seen:
            continue

        stack = [start]
        nodes: list[int] = []
        edge_weights: dict[int, float] = {}
        seen.add(start)

        while stack:
            node = stack.pop()
            nodes.append(node)

            for edge in graph[node]:
                edge_weights.setdefault(edge.edge_id, edge.distance)
                if edge.to in seen:
                    continue
                seen.add(edge.to)
                stack.append(edge.to)

        components.append((sorted(nodes), edge_weights))

    return components

