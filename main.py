from graph_algorithms.dfs import parcours_profondeur_rec
from graph_algorithms.creation_graph import create_graph
from graph_algorithms.tableroutage import creer_table_routage

if __name__ == '__main__':
    graphe = create_graph()
    while not parcours_profondeur_rec(graphe):
        graphe = create_graph()

    table_routage = creer_table_routage(graphe)
    print(table_routage)
