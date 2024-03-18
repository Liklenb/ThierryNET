from graph_algorithms.pathfinding import pch
import pandas as pd


def creer_table_routage(graphique):
    routing_table = []

    # Parcourir le graphe et extraire les chemins
    for start_node in range(100):
        paths = pch(graphique, start_node)  # Suppose que pch retourne un dictionnaire de chemins pour un sommet donné
        for end_node, (weight, path) in paths.items():
            routing_table.append([start_node, end_node, path[0]])
    # Obtenir tous les points de départ et d'arrivée possibles
    points_de_depart = set(x[0] for x in routing_table)
    points_d_arrivee = set(x[1] for x in routing_table)

    # Création d'un dictionnaire pour stocker les prochains points à rejoindre
    data = {}
    for depart in points_de_depart:
        data[depart] = {}
        for arrivee in points_d_arrivee:
            # Recherche de la sous-liste correspondante
            sous_liste_trouvee = None
            for sous_liste in routing_table:
                if sous_liste[0] == depart and sous_liste[1] == arrivee:
                    sous_liste_trouvee = sous_liste
                    break
            if sous_liste_trouvee is not None:
                # Le prochain point est le troisième élément de la sous-liste
                data[depart][arrivee] = sous_liste_trouvee[2]
            else:
                # Si aucune sous-liste correspondante n'est trouvée, le prochain point est None
                data[depart][arrivee] = None

    # Création du DataFrame à partir du dictionnaire
    df = pd.DataFrame(data)
    print(df)
    return df
