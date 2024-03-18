import graph
import random
import networkx as nx
import matplotlib.pyplot as plt
from math import cos, sin
from graph_algorithms.dfs import parcours_profondeur_rec
from graph_algorithms.pathfinding import pch


def create_graph():

    graphique = graph.Graph()  # création du graphique

    # création des 100 nœuds de la table de routage

    list_backbone = []  # liste qui stocke tous les éléments du tiers 1 (backbone)
    for i in range(1, 11):
        list_backbone.append(graphique.add_vertex(graph.Tiers.TIER1))  # création des 10 nœuds du tiers 1

    list_tiers2 = []  # liste qui stocke tous les éléments du tiers 2
    for i in range(11, 21):
        list_tiers2.append(graphique.add_vertex(graph.Tiers.TIER2))  # création des 20 nœuds du tiers 2

    list_tiers3 = []  # liste qui stocke tous les éléments du tiers 3
    for i in range(21, 101):
        list_tiers3.append(graphique.add_vertex(graph.Tiers.TIER3))  # création des 70 nœuds du tiers 3

    # création des arêtes

    aretes = {'tiers1_tiers1': [], 'tiers1_tiers2': [], 'tiers2_tiers2': [], 'tiers2_tiers3': []}

    # création des arêtes entre les tiers 1
    for backbone1 in list_backbone:
        for backbone2 in list_backbone:
            if backbone1 != backbone2:
                x = random.randint(1, 4)
                if x != 4:
                    aretes['tiers1_tiers1'].append(graphique.add_edge(backbone1, backbone2, random.randint(5, 10)))

    # creation des arêtes entre les tiers 2
    possible = list_tiers2.copy()
    test = True
    while test:
        tiers2_1 = random.choice(possible)
        while len(tiers2_1.get_neighbours()) >= 3:
            tiers2_1 = random.choice(possible)
            # print(tiers2_1.get_neighbours())
        tiers2_2 = random.choice(possible)
        while len(tiers2_2.get_neighbours()) >= 3 or tiers2_2 == tiers2_1 or tiers2_2 in (
                lambda lst: [voisin.vertex.identifier for voisin in lst])(tiers2_1.get_neighbours()) or len(
            tiers2_1.get_neighbours()) >= 3:
            tiers2_1 = random.choice(possible)
            tiers2_2 = random.choice(possible)
        aretes['tiers2_tiers2'].append(graphique.add_edge(tiers2_1, tiers2_2, random.randint(10, 20)))
        test = False
        test_priority = False
        for tiers2 in list_tiers2:
            if len(tiers2.get_neighbours()) < 2:
                test = True
            if len(tiers2.get_neighbours()) >= 3 and tiers2 in possible:
                possible.remove(tiers2)
                test_priority = True
            if test_priority:
                priority = []
                for tiers2_possible in possible:
                    if len(tiers2_possible.get_neighbours()) < 2:
                        priority.append(tiers2_possible)
                    if len(priority) == 2:
                        aretes['tiers2_tiers2'].append(graphique.add_edge(priority[0], priority[1], random.randint(10, 20)))
                    elif len(priority) == 1:
                        aretes['tiers2_tiers2'].append(
                            graphique.add_edge(priority[0], random.choice(possible), random.randint(10, 20)))
            if len(possible) == 1 and len(possible[0].get_neighbours()) < 2:
                print('ah')
    # création des arêtes entre les tiers 1 et les tiers 2
    for tiers2 in list_tiers2:
        for _ in range(random.randint(1, 2)):
            tiers1 = random.choice(list_backbone)
            while tiers1 in (lambda lst: [voisin.vertex.identifier for voisin in lst])(tiers2.get_neighbours()):
                tiers1 = random.choice(list_backbone)
            aretes['tiers1_tiers2'].append(graphique.add_edge(tiers1, tiers2, random.randint(10, 20)))

    # création des arêtes entre les tiers 2 et les tiers 3
    for tiers3 in list_tiers3:
        for _ in range(2):
            tiers2 = random.choice(list_tiers2)
            while tiers2 in (lambda lst: [voisin.vertex.identifier for voisin in lst])(tiers3.get_neighbours()):
                tiers2 = random.choice(list_tiers2)
            aretes['tiers2_tiers3'].append(graphique.add_edge(tiers2, tiers3, random.randint(20, 50)))
    return graphique


g = create_graph()

print(pch(g, 0))
"""G = nx.Graph()

sommets = list_backbone + list_tiers2 + list_tiers3

# Ajout des sommets
for sommet in sommets:
    G.add_node(sommet.identifier, tier=sommet.tier)

# Ajout des arêtes
for key, edges in aretes.items():
    for edge in edges:
        G.add_edge(edge.vertex1.identifier, edge.vertex2.identifier, weight=edge.weight)

# Organiser les nœuds en fonction de leur tier
pos = {}
tiers = set([v.tier for v in sommets])
max_radius = len(tiers)
current_radius = 0
for tier in tiers:
    tier_nodes = [v.identifier for v in sommets if v.tier == tier]
    num_nodes = len(tier_nodes)
    angle = 2 * 3.1416 / num_nodes
    for i, node in enumerate(tier_nodes):
        angle_rad = i * angle
        radius = current_radius * 0.3
        x = radius * random.uniform(0.9, 1.1) * cos(angle_rad)
        y = radius * random.uniform(0.9, 1.1) * sin(angle_rad)
        pos[node] = (x, y)
    current_radius += 1

# Visualisation du graphe
plt.figure(figsize=(50, 50))  # Taille de la figure
nx.draw(G, pos, with_labels=True, node_size=1000, node_color='skyblue', font_size=12, font_weight='bold')
nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
plt.title("Graphe")
plt.show()
"""
