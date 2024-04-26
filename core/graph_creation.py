from core import graph
import random


def create_graph():
    """Fonction qui créé un graphe de 100 noeuds avec des arêtes entre eux. Les noeuds sont répartis en 3 tiers : 10 de
    tiers1, 20 de tiers 2 et 70 de tiers 3. Les arêtes de inter-tiers 1 ont 75% de chance d'etre créées et ont un poids
    aléatoire entre 5 et 10, les tiers 2 sont reliés aléatoirement avec 2 autres noeuds de tiers 2 avec un poids entre
    10 et 20, les tiers 1 sont reliés aléatoirement avec 1 ou 2 noeuds de tiers 2 avec un poids entre 10 et 20.
    Les arêtes de tiers 2 sont reliés aléatoirement avec 2 noeuds de tiers 3 avec un poids entre 20 et 50."""

    graphic = graph.Graph()  # création du graphique

    # création des 100 nœuds de la table de routage

    list_backbone = []  # liste qui stocke tous les éléments du tiers 1 (backbone)
    for i in range(1, 11):
        list_backbone.append(graphic.add_vertex(graph.Tiers.TIER1))  # création des 10 nœuds du tiers 1

    list_tiers2 = []  # liste qui stocke tous les éléments du tiers 2
    for i in range(11, 31):
        list_tiers2.append(graphic.add_vertex(graph.Tiers.TIER2))  # création des 20 nœuds du tiers 2

    list_tiers3 = []  # liste qui stocke tous les éléments du tiers 3
    for i in range(31, 101):
        list_tiers3.append(graphic.add_vertex(graph.Tiers.TIER3))  # création des 70 nœuds du tiers 3

    # création des arêtes

    edges = {'tiers1_tiers1': [], 'tiers1_tiers2': [], 'tiers2_tiers2': [], 'tiers2_tiers3': []}

    # création des arêtes entre les tiers 1
    backbone = 0  # variable pour stocker le backbone maximum ayant déjà tenté de céer des liens avec tous les autres
    for backbone1 in list_backbone:
        for backbone2 in list_backbone[backbone+1:len(list_backbone)]:  # on ne veut pas créer de lien avec lui-même
            random_nb = random.randint(1, 4)
            if random_nb != 4:
                edges['tiers1_tiers1'].append(graphic.add_edge(backbone1, backbone2, random.randint(5, 10)))
        backbone += 1

    # creation des arêtes entre les tiers 2
    possible = list_tiers2.copy()
    not_all_vertices_have_2_neighbourgs = True  # variable pour savoir si tous les sommets ont au moins 2 voisins (
    # True si faux)
    while not_all_vertices_have_2_neighbourgs:
        tiers2_1 = random.choice(possible)
        while len(tiers2_1.get_neighbours()) >= 3:
            tiers2_1 = random.choice(possible)
        tiers2_2 = random.choice(possible)
        while (len(tiers2_2.get_neighbours()) >= 3 or
               tiers2_2 == tiers2_1 or tiers2_2.identifier in
               (lambda lst: [neighbourg.vertex.identifier for neighbourg in lst])(tiers2_1.get_neighbours()) or
               len(tiers2_1.get_neighbours()) >= 3):
            tiers2_1 = random.choice(possible)
            tiers2_2 = random.choice(possible)
        edges['tiers2_tiers2'].append(graphic.add_edge(tiers2_1, tiers2_2, random.randint(10, 20)))
        not_all_vertices_have_2_neighbourgs = False
        one_vertex_has_3_neighbourgs = False  # variable permettant de savoir si au moins un sommet a 3 voisins
        for tiers2 in list_tiers2:
            if len(tiers2.get_neighbours()) < 2:
                not_all_vertices_have_2_neighbourgs = True
            if len(tiers2.get_neighbours()) >= 3 and tiers2 in possible:
                possible.remove(tiers2)
                one_vertex_has_3_neighbourgs = True
            if one_vertex_has_3_neighbourgs:
                for tiers2_possible in possible:
                    priority = []
                    if len(tiers2_possible.get_neighbours()) < 2:
                        priority.append(tiers2_possible)
                    if (len(priority) == 2
                            and priority[0].identifier not in
                            (lambda lst: [neighbourg.vertex.identifier for neighbourg in lst])(priority[1].get_neighbours())):
                        edges['tiers2_tiers2'].append(graphic.add_edge(priority[0], priority[1],
                                                                          random.randint(10, 20)))
                    elif len(priority) == 1:
                        vertex = random.choice(possible)
                        while (vertex.identifier in
                               (lambda lst: [neighbourg.vertex.identifier for neighbourg in lst])(priority[0].get_neighbours())
                               or vertex == priority[0]):
                            vertex = random.choice(possible)
                        edges['tiers2_tiers2'].append(
                            graphic.add_edge(priority[0], vertex, random.randint(10, 20)))
                        if len(vertex.get_neighbours()) >= 3:
                            possible.remove(vertex)
            if len(possible) == 1 and len(possible[0].get_neighbours()) < 2:
                print('ah')

    # création des arêtes entre les tiers 1 et les tiers 2
    for tiers2 in list_tiers2:
        for _ in range(random.randint(1, 2)):
            tiers1 = random.choice(list_backbone)
            while tiers1.identifier in (lambda lst: [neighbourg.vertex.identifier for neighbourg in lst])(
                    tiers2.get_neighbours()):
                tiers1 = random.choice(list_backbone)
            edges['tiers1_tiers2'].append(graphic.add_edge(tiers1, tiers2, random.randint(10, 20)))

    # création des arêtes entre les tiers 2 et les tiers 3
    for tiers3 in list_tiers3:
        for _ in range(2):
            tiers2 = random.choice(list_tiers2)
            while tiers2.identifier in (lambda lst: [neighbourg.vertex.identifier for neighbourg in lst])(
                    tiers3.get_neighbours()):
                tiers2 = random.choice(list_tiers2)
            edges['tiers2_tiers3'].append(graphic.add_edge(tiers2, tiers3, random.randint(20, 50)))
    return graphic
