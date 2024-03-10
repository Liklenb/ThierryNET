from typing import Any
from queue import Queue, QueueItem


def pch(graph, start: int) -> dict[int, tuple[float, list[Any]]]:
    """
    Retourne le plus court chemin entre debut et fin dans le graphe.
    https://bradfieldcs.com/algos/graphs/dijkstras-algorithm/
    https://python.plainenglish.io/implementing-priority-queue-in-python-with-heapq-168d084f179d
    :param graph: Un objet contenant le graphe.
    :param start: Le sommet de départ.
    :return: Le plus court chemin entre debut et fin.
    """

    # On initialise la file de priorité avec un tuple contenant le coût initial,
    # le sommet de départ et la liste du chemin initial (vide).
    queue = Queue()
    queue.add(QueueItem((start, []), 0))

    # Un dictionnaire pour garder le coût et le chemin le plus court pour chaque sommet
    distances = {vertex.identifier: (float('infinity'), []) for vertex in graph.vertices}

    # On met le coût du sommet de départ à 0 et le chemin à [start]
    distances[start] = (0, [start])

    while queue:

        # On récupère et supprime le sommet avec le coût le plus bas de la file de priorité
        element = queue.pop()
        cout = element.get_priority()
        sommet, chemin = element.get_item()

        for neighbour in graph.vertices[sommet].get_neighbours():  # Pour chaque voisin du sommet actuel
            nouveau_cout  = cout + neighbour.weight  # On calcule le coût du chemin actuel + le poids de l'arête
            if nouveau_cout < distances[neighbour.vertex.identifier][0]:  # Si le nouveau coût est plus petit que le coût actuel
                distances[neighbour.vertex.identifier] = (nouveau_cout, chemin + [neighbour.vertex.identifier])  # On met à jour le coût et le chemin

                # On ajoute le voisin à la file de priorité avec le nouveau coût et le nouveau chemin
                queue.add(QueueItem((neighbour.vertex.identifier, chemin + [neighbour.vertex.identifier]), nouveau_cout))

    return distances
