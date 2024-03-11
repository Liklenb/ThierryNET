from typing import Any
from queue import Queue, QueueItem
from graph import Graph


def pch(graph: Graph, start: int) -> dict[int, tuple[float, list[Any]]]:
    """
    Retourne le plus court chemin entre debut et fin dans le graphe.
    :param graph: Un objet contenant le graphe.
    :param start: Le sommet de départ.
    :return: Le plus court chemin entre debut et fin.
    """

    # On initialise la file de priorité avec un tuple contenant le coût initial,
    # le sommet de départ et la liste du chemin initial (vide).
    queue = Queue()
    queue.add(QueueItem((start, []), 0))

    # Un dictionnaire pour garder le coût et le chemin le plus court pour chaque sommet
    distances = {vertex.identifier: (float('infinity'), []) for vertex in graph.get_vertices()}

    # On met le coût du sommet de départ à 0 et le chemin à [start]
    distances[start] = (0, [start])

    visited = set()  # On initialise un ensemble pour garder les sommets visités

    while queue:

        # On récupère et supprime le sommet avec le coût le plus bas de la file de priorité
        element = queue.pop()
        cout = element.get_priority()
        sommet, chemin = element.get_item()

        # Si le sommet a déjà été visité, on passe au suivant
        if sommet in visited:
            continue

        # On ajoute le sommet actuel à la liste des sommets visités
        visited.add(sommet)

        for neighbour in graph.get_vertex(sommet).get_neighbours():  # Pour chaque voisin du sommet actuel
            nouveau_cout = cout + neighbour.weight  # On calcule le coût du chemin actuel + le poids de l'arête

            # Si le nouveau coût est plus petit que le coût actuel
            if nouveau_cout < distances[neighbour.vertex.identifier][0]:
                # On met à jour le coût et le chemin
                distances[neighbour.vertex.identifier] = (nouveau_cout, chemin + [neighbour.vertex.identifier])

                # On ajoute le voisin à la file de priorité avec le nouveau coût et le nouveau chemin
                queue.add(QueueItem((neighbour.vertex.identifier, chemin + [neighbour.vertex.identifier]),
                                    nouveau_cout))

    return distances
