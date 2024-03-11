import graph
import random

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

aretes = {'tiers1_tiers1': [], 'tiers1_tiers2': [], 'tiers2_tiers2': []}

# création des arêtes entre les tiers 1
for backbone1 in list_backbone:
    for backbone2 in list_backbone:
        if backbone1 != backbone2:
            x = random.randint(1, 4)
            if x != 4:
                aretes['tiers1_tiers1'].append(graphique.add_edge(backbone1, backbone2, random.randint(5, 10)))
