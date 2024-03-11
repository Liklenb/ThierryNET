from graph_algorithms.dfs import parcours_profondeur_rec
from graph_algorithms.pathfinding import pch
from graph import Graph


if __name__ == '__main__':
    test_graph = Graph.load_file('graph.thierry')
    print(pch(test_graph, 0))  # Dijkstra
    print(parcours_profondeur_rec(test_graph))  # Parcours en profondeur
