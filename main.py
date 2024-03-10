from dijkstra import pch
from graph import Graph


if __name__ == '__main__':
    test_graph = Graph.load_file('graph.thierry')
    d = pch(test_graph, 0)
    print(d)
