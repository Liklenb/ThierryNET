import heapq


def dijkstra(graph: dict, start: int, end: int) -> tuple[int, list[int]]:
    """
    Retourne le plus court chemin entre debut et fin dans le graphe.
    https://bradfieldcs.com/algos/graphs/dijkstras-algorithm/
    https://python.plainenglish.io/implementing-priority-queue-in-python-with-heapq-168d084f179d
    :param graph: Un dictionnaire représentant le graphe.
    :param start: Le sommet de départ.
    :param end: Le sommet d'arrivée.
    :return: Le plus court chemin entre debut et fin.
    """

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

            for voisin, poids in graph[sommet]:  # Pour chaque voisin du sommet actuel
                if voisin not in visite:  # Si le voisin n'a pas été visité
                    # Ajoute le voisin à la file de priorité avec le nouveau coût et le chemin mis à jour
                    heapq.heappush(queue, (cout + poids, voisin, chemin))


def lire_graphe(fichier):
    """Fonction temporaire pour lire un graphe depuis un fichier."""

    with open(fichier, 'r') as f:
        n = int(f.readline().strip())
        graphe = {i: [] for i in range(n)}
        for ligne in f:
            u, v, poids = map(int, ligne.strip().split())
            graphe[u].append((v, poids))
            graphe[v].append((u, poids))
    return graphe


graphe = lire_graphe("graph.thierry")
debut, fin = 0, 5
route = dijkstra(graphe, debut, fin)

print(f"plus court chemin de {debut} à {fin} est {route}")
