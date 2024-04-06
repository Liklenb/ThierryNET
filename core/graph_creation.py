from core import graph
import random


def create_graph():
    graphique = graph.Graph()  # création du graphique

    # création des 100 nœuds de la table de routage

    list_backbone = []  # liste qui stocke tous les éléments du tiers 1 (backbone)
    for i in range(1, 11):
        list_backbone.append(graphique.add_vertex(graph.Tiers.TIER1))  # création des 10 nœuds du tiers 1

    list_tiers2 = []  # liste qui stocke tous les éléments du tiers 2
    for i in range(11, 31):
        list_tiers2.append(graphique.add_vertex(graph.Tiers.TIER2))  # création des 20 nœuds du tiers 2

    list_tiers3 = []  # liste qui stocke tous les éléments du tiers 3
    for i in range(31, 101):
        list_tiers3.append(graphique.add_vertex(graph.Tiers.TIER3))  # création des 70 nœuds du tiers 3

    # création des arêtes

    aretes = {'tiers1_tiers1': [], 'tiers1_tiers2': [], 'tiers2_tiers2': [], 'tiers2_tiers3': []}

    # création des arêtes entre les tiers 1
    backbone = 0  # variable pour stocker le backbone maximum ayant déjà tenté de céer des liens avec tous les autres
    for backbone1 in list_backbone:
        for backbone2 in list_backbone[backbone:len(list_backbone)]:
            if backbone1 != backbone2 and backbone2 not in (lambda lst: [voisin.vertex for voisin in lst])(
                    backbone1.get_neighbours()):
                x = random.randint(1, 4)
                if x != 4:
                    aretes['tiers1_tiers1'].append(graphique.add_edge(backbone1, backbone2, random.randint(5, 10)))
        backbone += 1

    # creation des arêtes entre les tiers 2
    possible = list_tiers2.copy()
    test = True  # variable pour savoir si tous les sommets ont au moins 2 voisins (True si faux)
    while test:
        tiers2_1 = random.choice(possible)
        while len(tiers2_1.get_neighbours()) >= 3:
            tiers2_1 = random.choice(possible)
        tiers2_2 = random.choice(possible)
        while (len(tiers2_2.get_neighbours()) >= 3 or
               tiers2_2 == tiers2_1 or tiers2_2.identifier in
               (lambda lst: [voisin.vertex.identifier for voisin in lst])(tiers2_1.get_neighbours()) or
               len(tiers2_1.get_neighbours()) >= 3):
            tiers2_1 = random.choice(possible)
            tiers2_2 = random.choice(possible)
        aretes['tiers2_tiers2'].append(graphique.add_edge(tiers2_1, tiers2_2, random.randint(10, 20)))
        test = False
        test_priority = False  # variable permettant de savoir si au moins un sommet a 3 voisins
        for tiers2 in list_tiers2:
            if len(tiers2.get_neighbours()) < 2:
                test = True
            if len(tiers2.get_neighbours()) >= 3 and tiers2 in possible:
                possible.remove(tiers2)
                test_priority = True
            if test_priority:
                for tiers2_possible in possible:
                    priority = []
                    if len(tiers2_possible.get_neighbours()) < 2:
                        priority.append(tiers2_possible)
                    if (len(priority) == 2
                            and priority[0].identifier not in
                            (lambda lst: [voisin.vertex.identifier for voisin in lst])(priority[1].get_neighbours())):
                        aretes['tiers2_tiers2'].append(graphique.add_edge(priority[0], priority[1],
                                                                          random.randint(10, 20)))
                    elif len(priority) == 1:
                        sommet = random.choice(possible)
                        while (sommet.identifier in
                               (lambda lst: [voisin.vertex.identifier for voisin in lst])(priority[0].get_neighbours())
                               or sommet == priority[0]):
                            sommet = random.choice(possible)
                        aretes['tiers2_tiers2'].append(
                            graphique.add_edge(priority[0], sommet, random.randint(10, 20)))
                        if len(sommet.get_neighbours()) >= 3:
                            possible.remove(sommet)
            if len(possible) == 1 and len(possible[0].get_neighbours()) < 2:
                print('ah')

    # création des arêtes entre les tiers 1 et les tiers 2
    for tiers2 in list_tiers2:
        for _ in range(random.randint(1, 2)):
            tiers1 = random.choice(list_backbone)
            while tiers1.identifier in (lambda lst: [voisin.vertex.identifier for voisin in lst])(
                    tiers2.get_neighbours()):
                tiers1 = random.choice(list_backbone)
            aretes['tiers1_tiers2'].append(graphique.add_edge(tiers1, tiers2, random.randint(10, 20)))

    # création des arêtes entre les tiers 2 et les tiers 3
    for tiers3 in list_tiers3:
        for _ in range(2):
            tiers2 = random.choice(list_tiers2)
            while tiers2.identifier in (lambda lst: [voisin.vertex.identifier for voisin in lst])(
                    tiers3.get_neighbours()):
                tiers2 = random.choice(list_tiers2)
            aretes['tiers2_tiers3'].append(graphique.add_edge(tiers2, tiers3, random.randint(20, 50)))
    return graphique
