import heapq
from typing import Any


def pch(graph, start: int) -> dict[int, tuple[float, list[Any]]]:
    """
    Retourne le plus court chemin entre debut et fin dans le graphe.
    https://bradfieldcs.com/algos/graphs/dijkstras-algorithm/
    https://python.plainenglish.io/implementing-priority-queue-in-python-with-heapq-168d084f179d
    :param graph: Un objet contenant le graphe.
    :param start: Le sommet de départ.
    :return: Le plus court chemin entre debut et fin.
    """

    # On crée un dictionnaire pour représenter le graphe
    graphe = {i: [] for i in range(len(graph.vertices))}

    # On parcourt les arêtes du graphe pour les ajouter au dictionnaire
    for edge in graph.edges:
        vertex1_index = graph.vertices.index(edge.vertex1)
        vertex2_index = graph.vertices.index(edge.vertex2)
        weight = edge.weight
        graphe[vertex1_index].append((vertex2_index, weight))
        graphe[vertex2_index].append((vertex1_index, weight))

    # On initialise la file de priorité avec un tuple contenant le coût initial,
    # le sommet de départ et la liste du chemin initial (vide).
    queue = [(0, start, [])]

    # Un dictionnaire pour garder le coût et le chemin le plus court pour chaque sommet
    distances = {vertex: (float('infinity'), []) for vertex in graphe}

    # On met le coût du sommet de départ à 0 et le chemin à [start]
    distances[start] = (0, [start])

    while queue:

        # On récupère et supprime le sommet avec le coût le plus bas de la file de priorité
        cout, sommet, chemin = heapq.heappop(queue)

        for voisin, poids in graphe[sommet]:  # Pour chaque voisin du sommet actuel
            nouveau_cout  = cout + poids  # On calcule le coût du chemin actuel + le poids de l'arête
            if nouveau_cout < distances[voisin][0]:  # Si le nouveau coût est plus petit que le coût actuel
                distances[voisin] = (nouveau_cout, chemin + [voisin])  # On met à jour le coût et le chemin

                # On ajoute le voisin à la file de priorité avec le nouveau coût et le nouveau chemin
                heapq.heappush(queue, (nouveau_cout, voisin, chemin + [voisin]))

    return distances
