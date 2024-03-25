import flet as ft

from core.depth_first_search import parcours_profondeur_rec
from core.graph_creation import create_graph
from core.routing_table import creer_table_routage
from ui.interface import FletInterface


def main():
    # Création du graphe
    graph = create_graph()

    # On s'assure que le graphe est connexe avant de continuer l'exécution du programme
    while not parcours_profondeur_rec(graph):
        graph = create_graph()

    # Création de l'interface graphique avec le graphe et la table de routage en paramètre
    ft.app(target=lambda page: FletInterface(page, graph, creer_table_routage(graph)))


if __name__ == '__main__':
    main()
