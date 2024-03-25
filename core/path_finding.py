from typing import Any
from core.priority_queue import Queue, QueueItem
from core.graph import Graph


def pch(graph: Graph, start: int) -> dict[int, tuple[float, list[Any]]]:
    """
    Calcule les plus courts chemins depuis un sommet de départ vers tous les autres sommets dans un graphe pondéré.
    Utilise l'algorithme de Dijkstra pour trouver le chemin le plus court en tenant compte des poids des arêtes.

    :param graph: Le graphe sur lequel appliquer l'algorithme de Dijkstra.
    :param start: L'identifiant du sommet de départ pour le calcul des chemins.
    :return: Un dictionnaire avec comme clés les identifiants des sommets et comme valeurs des tuples (coût, chemin).
    """

    queue = Queue()
    queue.add(QueueItem((start, []), 0))

    distances = {vertex.identifier: (float('infinity'), []) for vertex in graph.get_vertices()}
    distances[start] = (0, [None])

    visited = set()

    while queue:
        item = queue.pop()
        current_cost, (current_vertex, path) = item.get_priority(), item.get_item()

        if current_vertex in visited:
            continue

        visited.add(current_vertex)

        for neighbor in graph.get_vertex(current_vertex).get_neighbours():
            new_cost = current_cost + neighbor.weight

            if new_cost < distances[neighbor.vertex.identifier][0]:
                distances[neighbor.vertex.identifier] = (new_cost, path + [neighbor.vertex.identifier])
                queue.add(QueueItem((neighbor.vertex.identifier, path + [neighbor.vertex.identifier]), new_cost))

    return distances
