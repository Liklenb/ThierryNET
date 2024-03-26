from core.path_finding import pch
from core.graph import Graph


def create_routing_table(graph: Graph) -> list[list[None]]:
    """
    Création d'une table de routage pour un graphe donné en utilisant l'algorithme de Dijkstra. La table de routage
    stocke pour chaque sommet du graphe, le voisin à travers lequel on peut atteindre chaque sommet de destination.

    :param graph: Le graphe pour lequel on veut créer une table de routage
    :return: Une liste de listes où chaque liste représente les informations de routage pour un sommet du graphe
    """

    routing_table = []

    for vertex in graph.get_vertices():
        distances = pch(graph, vertex.identifier)

        vertex_routing = [None] * len(graph.get_vertices())

        for target_vertex, (_, path) in distances.items():
            vertex_routing[target_vertex] = path[0] if path else None

        routing_table.append(vertex_routing)

    return routing_table
