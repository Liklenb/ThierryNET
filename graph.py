import enum


class Tiers(enum.Enum):
    """
    The tiers of the vertices
    """
    TIER1 = 1
    TIER2 = 2
    TIER3 = 3


class Edge:
    def __init__(self, identifier: int, vertex1: 'Vertex', vertex2: 'Vertex', weight: int):
        """
        :param vertex1: First vertex
        :param vertex2: Second vertex
        :param weight: The weight of the edge
        """
        self.identifier = identifier
        self.vertex1 = vertex1
        self.vertex2 = vertex2
        self.weight = weight


class Neighbour:
    def __init__(self, vertex: 'Vertex', weight: int):
        self.vertex = vertex
        self.weight = weight


class Vertex:
    def __init__(self, identifier: int, tier: Tiers):
        self.edges: list[Edge] = []
        self.identifier = identifier
        self.tier = tier

    def get_neighbours(self):
        """
        Get the neighbours of the vertex
        :return: The neighbours of the vertex
        """
        neighbours = []
        for edge in self.edges:
            if edge.vertex1.identifier == self.identifier:
                neighbours.append(Neighbour(edge.vertex2, edge.weight))
            else:
                neighbours.append(Neighbour(edge.vertex1, edge.weight))
        return neighbours


class Graph:
    def __init__(self):
        self.vertices: list[Vertex] = []
        self.edges: list[Edge] = []

    def add_edge(self, vertex1: Vertex, vertex2: Vertex, weight: int) -> Edge:
        """
        :param vertex1: First vertex
        :param vertex2: Second vertex
        :param weight: The weight of the edge
        :return: The edge that was added
        """
        edge = Edge(len(self.edges), vertex1, vertex2, weight)
        vertex1.edges.append(edge)
        vertex2.edges.append(edge)
        self.edges.append(edge)
        return edge

    def add_vertex(self, tier: Tiers) -> Vertex:
        """
        Add a vertex to the graph
        :return: The vertex that was added
        """
        vertex = Vertex(len(self.vertices), tier)
        self.vertices.append(vertex)
        return vertex

    @staticmethod
    def load_file(path):
        """
        Load a graph from a file
        :param path: The path to the file
        :return: None
        """
        graph = Graph()
        with open(path, 'r') as file:
            lines = file.readlines()
            for x in range(int(lines[0])):
                graph.add_vertex(Tiers.TIER1)
            for line in lines[1:]:
                vertex1, vertex2, weight = line.split()
                vertex1 = int(vertex1)
                vertex2 = int(vertex2)
                weight = int(weight)
                graph.add_edge(graph.vertices[vertex1], graph.vertices[vertex2], weight)
        return graph

    def save_to_file(self, path):
        """
        Save the graph to a file
        :param path: The path to the file
        :return: None
        """
        with open(path, 'w') as file:
            file.write(str(len(self.vertices)) + '\n')
            for edge in self.edges:
                file.write(
                    str(self.vertices.index(edge.vertex1)) + ' ' + str(self.vertices.index(edge.vertex2)) + ' ' + str(
                        edge.weight) + '\n')
