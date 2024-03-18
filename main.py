from graph_algorithms.dfs import parcours_profondeur_rec
from graph_algorithms.creation_graph import create_graph
from graph_algorithms import tableroutage


if __name__ == '__main__':
    graphe = create_graph()
    while not parcours_profondeur_rec(graphe):
        print('problemes...')
        graphe = create_graph()
    print('okay')
    table_routage = tableroutage.creer_table_routage(graphe)
