import heapq
import math
import graphe
from PIL import Image

class image:
    """
    Classe image, permet de manipuler l'image, notamment de la transformer en graphe et de lui appliquer des algorithmes
    tels que Dijkstra et A étoile.
    """
    def __init__(self, image: Image):
        """
        Constructeur de la classe, transforme l'image en graphe pondéré orienté.
        :param image: une image de type Image, de la bibliothèque PIL (pillow).
        """
        #Création du graphe.
        self.graphe = graphe.Graphe()
        #Conversion de l'image en niveaux de gris.
        self.image = image.convert("L")

        #Permet d'ajouter chaque pixel comme un sommet du graphe.
        for y in range(self.image.height):
            for x in range(self.image.width):
                valeur_pixel = self.image.getpixel((x,y))
                self.graphe.ajouter_sommet(
                    valeur_pixel
                )

        print(len(self.graphe.liste_sommet))

        nlignes = self.image.height
        ncol = self.image.width
        #Ajout des arêtes, le calcul du poids de l'arête se fait gràce à la valeur absolue de la différence d'intensité des deux sommets de l'arête.
        for ligne in range(nlignes):
            for col in range(ncol):
                source = ligne*ncol+col
                if ligne > 0: #si ce n'est pas la première ligne on peut ajouter une arête vers le haut
                    dest = (ligne-1)*ncol+col
                    poids = abs(self.graphe.liste_sommet[dest].val - self.graphe.liste_sommet[source].val)
                    self.graphe.ajouter_arete(source, dest, poids)
                if col > 0: #si ce n'est pas la première colonne on peut ajouter une arête vers la gauche
                    dest = ligne*ncol+(col-1)
                    poids = abs(self.graphe.liste_sommet[dest].val - self.graphe.liste_sommet[source].val)
                    self.graphe.ajouter_arete(source, dest, poids)
                if ligne < (nlignes - 1): #si ce n'est pas la dernière ligne on peut ajouter une arête vers le bas
                    dest = (ligne+1)*ncol+col
                    poids = abs(self.graphe.liste_sommet[dest].val - self.graphe.liste_sommet[source].val)
                    self.graphe.ajouter_arete(source, dest, poids)
                if col < (ncol - 1): #si ce n'est pas la dernière colonne on peut ajouter une arête vers la droite
                    dest = ligne*ncol+(col+1)
                    poids = abs(self.graphe.liste_sommet[dest].val - self.graphe.liste_sommet[source].val)
                    self.graphe.ajouter_arete(source, dest, poids)

    def a_etoile(self, debut, fin, heuristique, canvas, condition):
        """
        Algorithme A étoile, pour calculer le plus court chemin entre un point de départ et un point d'arrivée, à l'aide d'une heuristique.
        :param debut: un entier, le point de départ.
        :param fin: un entier, le point d'arrivée.
        :return: liste_chemin, une liste de points représentant le plus court chemin trouvé.
        """

        self.graphe.liste_sommet[debut].temps_depuis_source = 0
        tentatives = 0
        file_prio = [(0, debut)]
        visite = set()

        x_fin = fin % self.image.width
        y_fin = fin // self.image.height

        match heuristique:
            case 'manhattan':
                x = lambda x_a, y_a, x_b, y_b : abs(x_b - x_a) + abs(y_b - y_a)
            case 'euclide':
                x = lambda x_a, y_a, x_b, y_b: math.sqrt(math.pow(x_b - x_a, 2)+math.pow(y_b - y_a, 2))
            case 'chebyshev':
                x = lambda x_a, y_a, x_b, y_b: max(abs(x_a - y_b), abs(x_b - y_a))
            case _:
                x = lambda x_a, y_a, x_b, y_b: 0

        #Calcul de l'heuristique
        for v in range(len(self.graphe.liste_sommet)):
            x_v = v % self.image.width
            y_v = v // self.image.height
            #self.graphe.liste_sommet[v].heuristique = 0
            #self.graphe.liste_sommet[v].heuristique = abs(self.graphe.liste_sommet[v].val - self.graphe.liste_sommet[fin].val)* math.sqrt(math.pow(x_fin - x_v, 2)+math.pow(y_fin - y_v, 2)) #experimental, pas utilise car pas tres bon
            #self.graphe.liste_sommet[v].heuristique = math.sqrt(math.pow(x_fin - x_v, 2)+math.pow(y_fin - y_v, 2)) #euclide
            #self.graphe.liste_sommet[v].heuristique = abs(x_fin - x_v) + abs(y_fin - y_v) #manhattan
            #self.graphe.liste_sommet[v].heuristique = max(abs(x_v - y_fin), abs(x_fin - y_v)) #https://en.wikipedia.org/wiki/Chebyshev_distance
            #self.graphe.liste_sommet[v].heuristique = min(abs(x_v - y_fin), abs(x_fin - y_v)) #chebyshev inversé

            self.graphe.liste_sommet[v].heuristique = x(x_v, y_v, x_fin, y_fin)

        #Tant que la pile n'est pas vide on continue de rechercher le plus court chemin.
        while file_prio:
            #On prend le dernier sommet ajoute dans la pile, le sommet avec le temps depuis source le plus petit donc
            dist, min_v = heapq.heappop(file_prio)

            #On regarde si le sommet courant n'a pas deja ete visite.
            if min_v in visite:
                continue
            visite.add(min_v)
            #Si min_v est le sommet d'arrivee on peut s'arreter.
            if min_v == fin:
                break

            tentatives += 1
            for arete in self.graphe.liste_sommet[min_v].liste_adj:
                a_tester = arete.dest

                if self.graphe.liste_sommet[a_tester].temps_depuis_source > self.graphe.liste_sommet[min_v].temps_depuis_source + arete.pds:
                    self.graphe.liste_sommet[a_tester].temps_depuis_source = self.graphe.liste_sommet[min_v].temps_depuis_source + arete.pds
                    self.graphe.liste_sommet[a_tester].precedent = self.graphe.liste_sommet[min_v]
                    heapq.heappush(file_prio, (self.graphe.liste_sommet[min_v].temps_depuis_source + arete.pds + self.graphe.liste_sommet[a_tester].heuristique, a_tester))

            #Permet l'affichage des sommets visites.
            if condition == 1:
                center_x = min_v %self.image.width
                center_y = min_v // self.image.width

                canvas.create_oval(
                center_x,
                center_y,
                center_x,
                center_y,
                fill="yellow",
                outline="yellow"
                )
                canvas.update()

        liste_chemin = list()
        sommet_c = self.graphe.liste_sommet[fin]
        while sommet_c:
            liste_chemin.insert(0,sommet_c.num)
            sommet_c = sommet_c.precedent
        #print(f"tentatives : {tentatives}")
        print("A étoile terminé")
        print(f"taille chemin = {len(liste_chemin)}")
        return liste_chemin, tentatives

########################################################-- code de a_etoile et dijkstra pour comparaison, nous ne l'utilisons pas ici pour des questions de performances --################################################################

    def a_etoile_basique(self, debut, fin):

        self.graphe.liste_sommet[debut].temps_depuis_source = 0
        tentatives = 0

        liste_noeuds_a_visiter = {sommet.num for sommet in self.graphe.liste_sommet}

        x_fin = fin % self.image.width
        y_fin = fin // self.image.height

        for v in liste_noeuds_a_visiter:
            x_v = v % self.image.width
            y_v = v // self.image.height
            #self.graphe.liste_sommet[v].heuristique = 0
            #self.graphe.liste_sommet[v].heuristique = abs(self.graphe.liste_sommet[v].val - self.graphe.liste_sommet[fin].val)* math.sqrt(math.pow(x_fin - x_v, 2)+math.pow(y_fin - y_v, 2)) #experimental
            #self.graphe.liste_sommet[v].heuristique = math.sqrt(math.pow(x_fin - x_v, 2)+math.pow(y_fin - y_v, 2)) #euclide
            #self.graphe.liste_sommet[v].heuristique = abs(x_fin - x_v) + abs(y_fin - y_v) #manhattan
            #self.graphe.liste_sommet[v].heuristique = self.graphe.liste_sommet[v].val * max(abs(x_v - y_fin), abs(x_fin - y_v))  # https://en.wikipedia.org/wiki/Chebyshev_distance

        while fin in liste_noeuds_a_visiter:
            min_v = -1
            dist = float("inf")

            for v in liste_noeuds_a_visiter:
                if self.graphe.liste_sommet[v].temps_depuis_source + self.graphe.liste_sommet[v].heuristique < dist:
                    min_v = v
                    dist = self.graphe.liste_sommet[v].temps_depuis_source + self.graphe.liste_sommet[v].heuristique

            liste_noeuds_a_visiter.remove(min_v)

            tentatives += 1
            for i in range(len(self.graphe.liste_sommet[min_v].liste_adj)):
                a_tester = self.graphe.liste_sommet[min_v].liste_adj[i].dest

                if self.graphe.liste_sommet[a_tester].temps_depuis_source > self.graphe.liste_sommet[min_v].temps_depuis_source + self.graphe.liste_sommet[min_v].liste_adj[i].pds:
                    self.graphe.liste_sommet[a_tester].temps_depuis_source = self.graphe.liste_sommet[min_v].temps_depuis_source + self.graphe.liste_sommet[min_v].liste_adj[i].pds
                    self.graphe.liste_sommet[a_tester].precedent = self.graphe.liste_sommet[min_v]

        liste_chemin = list()
        sommet_c = self.graphe.liste_sommet[fin]
        while sommet_c:
            liste_chemin.insert(0, sommet_c.num)
            sommet_c = sommet_c.precedent

        print("A étoile terminé")
        return liste_chemin

    def dijkstra(self, debut, fin):
        """
        Algorithme de Dijkstra, pour calculer le plus court chemin entre un point de départ et un point d'arrivée.
        :param debut: un entier, le point de départ.
        :param fin: un entier, le point d'arrivée.
        :return: liste_chemin, une liste de points représentant le plus court chemin trouvé.
        """

        self.graphe.liste_sommet[debut].temps_depuis_source = 0
        tentatives = 0

        liste_noeuds_a_visiter = {sommet.num for sommet in self.graphe.liste_sommet}

        while fin in liste_noeuds_a_visiter:
            min_v = -1
            dist = float("inf")

            for v in liste_noeuds_a_visiter:
                if self.graphe.liste_sommet[v].temps_depuis_source < dist:
                    min_v = v
                    dist = self.graphe.liste_sommet[v].temps_depuis_source

            liste_noeuds_a_visiter.remove(min_v)

            tentatives += 1
            for i in range(len(self.graphe.liste_sommet[min_v].liste_adj)):
                a_tester = self.graphe.liste_sommet[min_v].liste_adj[i].dest

                if self.graphe.liste_sommet[a_tester].temps_depuis_source > self.graphe.liste_sommet[min_v].temps_depuis_source + self.graphe.liste_sommet[min_v].liste_adj[i].pds:
                    self.graphe.liste_sommet[a_tester].temps_depuis_source = self.graphe.liste_sommet[min_v].temps_depuis_source + self.graphe.liste_sommet[min_v].liste_adj[i].pds
                    self.graphe.liste_sommet[a_tester].precedent = self.graphe.liste_sommet[min_v]

        liste_chemin = list()
        sommet_c = self.graphe.liste_sommet[fin]
        while sommet_c:
            liste_chemin.insert(0,sommet_c.num)
            sommet_c = sommet_c.precedent
        print(f"tentatives = {tentatives}")
        print("Dijkstra terminé")
        return liste_chemin