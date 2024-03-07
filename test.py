class Arete:
    def __init__(self, sommet):
        self.sommet = sommet
        self.poids = 10

    def __str__(self):
        return f"{self.poids}"

class Sommet:
    def __init__(self):
        self.arete = Arete(self)


sommet = Sommet()
print(sommet.arete.sommet.arete)
