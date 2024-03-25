from core.path_finding import pch
from core.graph import Graph


def creer_table_routage(graph: Graph) -> list[list[None]]:
    """
    Création d'une table de routage pour un graphe donné en utilisant l'algorithme de Dijkstra. La table de routage
    stocke pour chaque sommet du graphe, le voisin à travers lequel on peut atteindre chaque sommet de destination.

    :param graph: Le graphe pour lequel on veut créer une table de routage
    :return: Une liste de listes où chaque liste représente les informations de routage pour un sommet du graphe
    """

    # On initialise une liste vide pour stocker les informations de routage
    table_routage = []

    for vertex in graph.get_vertices():
        # On applique l'algorithme de Dijkstra pour trouver les distances
        distances = pch(graph, vertex.identifier)

        # On initialise une liste vide pour stocker les informations de routage pour le sommet courant
        routage_sommet = [None] * len(graph.get_vertices())

        # On stocke les informations de routage pour le sommet courant
        for sommet, (_, chemin) in distances.items():
            routage_sommet[sommet] = chemin[0]

        # On ajoute les informations de routage pour le sommet courant à la table de routage
        table_routage.append(routage_sommet)

    return table_routage
