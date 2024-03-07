class Edge:
    def __init__(self, vertex1: 'Vertex', vertex2: 'Vertex', weight: int):
        """
        :param vertex1: First vertex
        :param vertex2: Second vertex
        :param weight: The weight of the edge
        """
        self.vertex1 = vertex1
        self.vertex2 = vertex2
        self.weight = weight

class Vertex:
    edges: list[Edge] = []

class Graph:
    def __init__(self):
        self.vertices: list[Vertex] = []
        self.edges: list[Edge] = []

    def add_edges(self, vertex1: Vertex, vertex2: Vertex, weight: int) -> Edge:
        """
        :param vertex1: First vertex
        :param vertex2: Second vertex
        :param weight: The weight of the edge
        :return: The edge that was added
        """
        edge = Edge(vertex1, vertex2, weight)
        vertex1.edges.append(edge)
        vertex2.edges.append(edge)
        self.edges.append(edge)
        return edge

    def add_vertex(self) -> Vertex:
        """
        Add a vertex to the graph
        :return: The vertex that was added
        """
        vertex = Vertex()
        self.vertices.append(vertex)
        return vertex

    def load_file(self, path):
        """
        Load a graph from a file
        :param path: The path to the file
        :return: None
        """
        with open(path, 'r') as file:
            lines = file.readlines()
            for x in range(int(lines[0])):
                self.add_vertex()
            for line in lines[1:]:
                vertex1, vertex2, weight = line.split()
                vertex1 = int(vertex1)
                vertex2 = int(vertex2)
                weight = int(weight)
                self.add_edges(self.vertices[vertex1], self.vertices[vertex2], weight)

    def save_to_file(self, path):
        """
        Save the graph to a file
        :param path: The path to the file
        :return: None
        """
        with open(path, 'w') as file:
            file.write(str(len(self.vertices)) + '\n')
            for edge in self.edges:
                file.write(str(self.vertices.index(edge.vertex1)) + ' ' + str(self.vertices.index(edge.vertex2)) + ' ' + str(edge.weight) + '\n')



graph = Graph()
graph.load_file('graph.thierry')
print(graph.vertices)
print(graph.edges)
