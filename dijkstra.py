import heapq


def pch(graph, start: int, end: int) -> tuple[int, list[int]]:
    """
    Retourne le plus court chemin entre debut et fin dans le graphe.
    https://bradfieldcs.com/algos/graphs/dijkstras-algorithm/
    https://python.plainenglish.io/implementing-priority-queue-in-python-with-heapq-168d084f179d
    :param graph: Un objet contenant le graphe.
    :param start: Le sommet de départ.
    :param end: Le sommet d'arrivée.
    :return: Le plus court chemin entre debut et fin.
    """

    # On crée un dictionnaire pour représenter le graphe
    graphe = {}

    # On parcourt les arêtes du graphe pour les ajouter au dictionnaire
    for edge in graph.edges:

        # On récupère l'index des sommets de l'arête et le poids de l'arête
        vertex1_index = graph.vertices.index(edge.vertex1)
        vertex2_index = graph.vertices.index(edge.vertex2)
        weight = edge.weight

        # Si le sommet n'est pas déjà dans le graphe, on l'ajoute
        if vertex1_index not in graphe:
            graphe[vertex1_index] = []

        if vertex2_index not in graphe:
            graphe[vertex2_index] = []

        # On ajoute les sommets et le poids de l'arête au graphe
        graphe[vertex1_index].append((vertex2_index, weight))
        graphe[vertex2_index].append((vertex1_index, weight))

    # On initialise la file de priorité avec un tuple contenant le coût initial,
    # le sommet de départ et la liste du chemin initial (vide).
    queue = [(0, start, [])]

    # On utilise un ensemble pour une trace des sommets visités.
    visite = set()

    while queue:

        # On récupère et supprime le sommet avec le coût le plus bas de la file de priorité
        cout, sommet, chemin = heapq.heappop(queue)

        if sommet not in visite:  # Si le sommet n'a pas déjà été visité
            visite.add(sommet)  # Marque le sommet comme visité
            chemin = chemin + [sommet]  # Ajoute le sommet actuel au chemin

            # Si le sommet actuel est le sommet d'arrivée, retourne le chemin trouvé
            if sommet == end:
                return cout, chemin  # Retourne directement le chemin

            for voisin, poids in graphe[sommet]:  # Pour chaque voisin du sommet actuel
                if voisin not in visite:  # Si le voisin n'a pas été visité
                    # Ajoute le voisin à la file de priorité avec le nouveau coût et le chemin mis à jour
                    heapq.heappush(queue, (cout + poids, voisin, chemin))
