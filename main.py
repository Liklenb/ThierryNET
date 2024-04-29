import flet as ft

from core.depth_first_search import dfs_traversal
from core.graph_creation import create_graph
# from ui.interface import FletGraphInterface
from ui.interface_test import FletGraphInterface


def main():
    ft.app(FletGraphInterface)


if __name__ == '__main__':
    main()
