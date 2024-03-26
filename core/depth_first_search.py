from core.graph import Graph


def explore_vertex(graph: Graph, vertex: int, visited_vertices: set[int]):
    """
    Explore un sommet du graphe

    :param graph: Un objet contenant le graphe
    :param vertex: Le sommet à explorer
    :param visited_vertices: Un ensemble contenant les sommets visités
    """

    visited_vertices.add(vertex)  # On ajoute le sommet à l'ensemble des sommets visités

    # Pour chaque voisin du sommet, on explore le voisin si celui-ci n'a pas déjà été visité
    for neighbor in graph.get_vertices()[vertex].get_neighbours():
        if neighbor.vertex.identifier not in visited_vertices:
            explore_vertex(graph, neighbor.vertex.identifier, visited_vertices)


def dfs_traversal(graph: Graph) -> bool:
    """
    Parcours en profondeur du graphe

    :param graph: Un objet contenant le graphe
    :return: Le parcours en profondeur du graphe
    """

    visited_vertices = set()  # On initialise un ensemble pour garder les sommets visités

    # On explore chaque sommet du graphe en profondeur et on ajoute les sommets visités à l'ensemble visites
    for vertex in range(len(graph.get_vertices())):
        if vertex not in visited_vertices:
            explore_vertex(graph, vertex, visited_vertices)

            # Si le nombre de sommets visités est égal au nombre de sommets du graphe, on retourne True
            if len(visited_vertices) != len(graph.get_vertices()):
                return False

    return True
