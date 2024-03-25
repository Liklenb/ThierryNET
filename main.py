import flet as ft

from core.depth_first_search import dfs_traversal
from core.graph_creation import create_graph
from core.routing_table import create_routing_table
from ui.interface import FletGraphInterface


def main():
    # Création du graphe
    graph = create_graph()

    # On s'assure que le graphe est connexe avant de continuer l'exécution du programme
    while not dfs_traversal(graph):
        graph = create_graph()

    # Création de l'interface graphique avec le graphe et la table de routage en paramètre
    ft.app(target=lambda page: FletGraphInterface(page, graph, create_routing_table(graph)))


if __name__ == '__main__':
    main()
