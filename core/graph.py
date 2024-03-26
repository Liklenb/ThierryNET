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

    def __repr__(self):
        return f"Edge({self.vertex1.identifier}, {self.vertex2.identifier}, w:{self.weight})"


class Neighbour:
    def __init__(self, vertex: 'Vertex', weight: int):
        self.vertex = vertex
        self.weight = weight

    def __repr__(self):
        return f"Neighbour({self.vertex.identifier}, w:{self.weight})"


class Vertex:
    def __init__(self, identifier: int, tier: Tiers):
        self.edges: list[Edge] = []
        self.identifier = identifier
        self.tier: Tiers = tier

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

    def __repr__(self):
        return f"Vertex({self.identifier}, T{self.tier})"


class Graph:
    def __init__(self):
        self._vertices: list[Vertex] = []
        self._edges: list[Edge] = []

    def get_vertex(self, identifier: int) -> Vertex:
        """
        Get a vertex by its identifier
        :param identifier: The identifier of the vertex
        :return: The vertex
        """
        return self._vertices[identifier]

    def get_edge(self, identifier: int) -> Edge:
        """
        Get an edge by its identifier
        :param identifier: The identifier of the edge
        :return: The edge
        """
        return self._edges[identifier]

    def get_vertices(self) -> list[Vertex]:
        """
        Get a copy of the vertices of the graph
        :return: The vertices of the graph
        """
        return self._vertices.copy()

    def get_edges(self) -> list[Edge]:
        """
        Get a copy of the edges of the graph
        :return: The edges of the graph
        """
        return self._edges.copy()

    def add_edge(self, vertex1: Vertex, vertex2: Vertex, weight: int) -> Edge:
        """
        :param vertex1: First vertex
        :param vertex2: Second vertex
        :param weight: The weight of the edge
        :return: The edge that was added
        """
        edge = Edge(len(self._edges), vertex1, vertex2, weight)
        vertex1.edges.append(edge)
        vertex2.edges.append(edge)
        self._edges.append(edge)
        return edge

    def add_vertex(self, tier: Tiers) -> Vertex:
        """
        Add a vertex to the graph
        :return: The vertex that was added
        """
        vertex = Vertex(len(self._vertices), tier)
        self._vertices.append(vertex)
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
            for tier in lines[0].split():
                graph.add_vertex(Tiers(int(tier)))
            for line in lines[1:]:
                vertex1, vertex2, weight = line.split()
                vertex1 = int(vertex1)
                vertex2 = int(vertex2)
                weight = int(weight)
                graph.add_edge(graph._vertices[vertex1], graph._vertices[vertex2], weight)
        return graph

    def save_to_file(self, path):
        """
        Save the graph to a file
        :param path: The path to the file
        :return: None
        """
        with open(path, 'w') as file:
            file.write(" ".join(str(vertex.tier.value) for vertex in self._vertices) + '\n')
            for edge in self._edges:
                file.write(
                    str(self._vertices.index(edge.vertex1)) + ' ' + str(self._vertices.index(edge.vertex2)) + ' ' + str(
                        edge.weight) + '\n')

    def __repr__(self):
        return f"Graph({len(self._vertices)} vertices, {len(self._edges)} edges)"
