from graph import Graph


def explorer_sommet(graph: Graph, sommet: int, sommets_visites: set[int]):
    """
    Explore un sommet du graphe
    :param graph: Un objet contenant le graphe
    :param sommet: Le sommet à explorer
    :param sommets_visites: Un ensemble contenant les sommets visités
    """

    sommets_visites.add(sommet)  # On ajoute le sommet à l'ensemble des sommets visités

    # Pour chaque voisin du sommet, on explore le voisin si celui-ci n'a pas déjà été visité
    for voisin in graph.get_vertices()[sommet].get_neighbours():
        if voisin.vertex.identifier not in sommets_visites:
            explorer_sommet(graph, voisin.vertex.identifier, sommets_visites)


def parcours_profondeur_rec(graph: Graph) -> bool:
    """
    Parcours en profondeur du graphe
    :param graph: Un objet contenant le graphe
    :return: Le parcours en profondeur du graphe
    """

    sommets_visites = set()  # On initialise un ensemble pour garder les sommets visités

    # On explore chaque sommet du graphe en profondeur et on ajoute les sommets visités à l'ensemble visites
    for sommet in range(len(graph.get_vertices())):
        if sommet not in sommets_visites:
            explorer_sommet(graph, sommet, sommets_visites)

            # Si le nombre de sommets visités est égal au nombre de sommets du graphe, on retourne True
            if len(sommets_visites) != len(graph.get_vertices()):
                return False

    return True
