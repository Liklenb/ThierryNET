from graph_algorithms.pathfinding import pch
from graph import Graph


def creer_table_routage(graph: Graph) -> dict[int, dict[int, float]]:
    """
    Création d'une table de routage pour un graphe donné en utilisant l'algorithme de Dijkstra. La table de routage
    stocke pour chaque sommet du graphe, le voisin à travers lequel on peut atteindre chaque sommet de destination.

    :param graph: Le graphe pour lequel on veut créer une table de routage
    :return: Un dictionnaire qui contient pour chaque sommet du graphe, le voisin à travers lequel on peut atteindre
    chaque sommet de destination.
    """

    # On initialise un dictionnaire pour stocker les informations de routage pour chaque sommet du graphe
    table_routage = {}

    for vertex in graph.get_vertices():
        # On applique l'algorithme de Dijkstra pour trouver les distances
        distances = pch(graph, vertex.identifier)

        # On stocke les informations de routage pour le sommet courant
        table_routage[vertex.identifier] = {neighbour: path[0] for neighbour, (_, path) in distances.items()}

    return table_routage


"""
    table_routage = []

    for vertex in graph.get_vertices():
        distances = pch(graph, vertex.identifier)
        
        routage_sommet = [None] * len(graph.get_vertices())
        
        for dest, (_, path) in distances.items():
            if len(path) > 1:
                routage_sommet[dest] = path[1]  # path[1] est le sommet suivant dans le chemin
            elif len(path) == 1:
                routage_sommet[dest] = path[0]  # cas où le sommet de départ et d'arrivée sont les mêmes

        table_routage.append(routage_sommet)

    return table_routage
"""
