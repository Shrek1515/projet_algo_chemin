import math
import tkinter as tk
from pathlib import Path
from tkinter import ttk
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
import image_vers_graphe
import os

class interface_graphique:
    """
    Classe interface_graphique, permet d'instancier l'interface graphique.
    """

    def __init__(self):
        """
        Constructeur de l'interface graphique, création de la fenêtre, positionnement des boutons et labels.
        """

        self.racine = ThemedTk()
        self.racine.title("Plus court chemin sur image")
        self.racine.geometry("1600x900")

        self.canvas = None

        #creéation du cadre qui va permettre d'afficher l'image et le plus court chemin sur l'image
        self.cadre_image = tk.Frame(self.racine, bd=0, highlightthickness=0, background="#fe8e36")
        self.cadre_image.place(x=0, y=0, relwidth=0.6, relheight=1, anchor="nw")

        self.sommets_var = tk.StringVar()
        self.sommets_var.set("sommets visités :")
        self.sommets_visite_label = tk.Label(self.cadre_image, textvariable=self.sommets_var)
        self.sommets_visite_label.place(relx=0.25, rely=0.96)

        self.temps_var = tk.StringVar()
        self.temps_var.set("temps chemin :")
        self.temps_label = tk.Label(self.cadre_image, textvariable=self.temps_var)
        self.temps_label.place(relx=0.55, rely=0.96)

        #création du cadre qui va contenir les boutons et les labels, toute l'interface de configuration en somme.
        self.cadre_entree_uti = tk.Frame(self.racine, bd=0, highlightthickness=0, background="#3da1eb")

        #création et configuration de la grille qui nous permettra de placer les boutons et labels sur le cadre
        self.cadre_entree_uti.columnconfigure(0, weight=1, uniform='column')
        self.cadre_entree_uti.columnconfigure(1, weight=1, uniform='column')
        self.cadre_entree_uti.columnconfigure(2, weight=1, uniform='column')
        self.cadre_entree_uti.columnconfigure(3, weight=1, uniform='column')
        self.cadre_entree_uti.rowconfigure(0, weight=1, uniform='row')
        self.cadre_entree_uti.rowconfigure(1, weight=1, uniform='row')
        self.cadre_entree_uti.rowconfigure(2, weight=1, uniform='row')
        self.cadre_entree_uti.rowconfigure(3, weight=1, uniform='row')
        self.cadre_entree_uti.rowconfigure(4, weight=1, uniform='row')
        self.cadre_entree_uti.rowconfigure(5, weight=1, uniform='row')

        self.cadre_entree_uti.place(relx=0.6, y=0, relwidth=0.4, relheight=1, anchor="nw")

        #création et positionnement des différents boutons, voir README pour l'explication de chaque bouton/label.
        self.bouton_coord = tk.Button(self.cadre_entree_uti, text="démarrer", command=self.afficher_chemin)

        self.liste_chemins = os.listdir('res/')
        self.liste_var = tk.StringVar()

        self.chemin = ttk.OptionMenu(self.cadre_entree_uti, self.liste_var, "image", *self.liste_chemins, command=self.afficher_image)
        self.chemin_label = tk.Label(self.cadre_entree_uti, text="Chemin vers image :")
        self.chemin_label.grid(row=0,column=0)

        self.liste_heuristiques = ('manhattan', 'euclide', 'chebyshev', 'dijkstra')
        self.liste_heuristiques_var = tk.StringVar()
        self.heuristique_menu = ttk.OptionMenu(self.cadre_entree_uti, self.liste_heuristiques_var, 'heuristique', *self.liste_heuristiques)
        self.heuristique_label = tk.Label(self.cadre_entree_uti, text="heuristique :")
        self.heuristique_label.grid(row=3, column=2)
        self.heuristique_menu.grid(row=3, column=3)

        self.afficher_check_var = tk.IntVar()
        self.afficher_check_button = tk.Checkbutton(self.cadre_entree_uti, text="Progression", variable=self.afficher_check_var, onvalue = 1, offvalue=0)
        self.afficher_check_button.grid(row=4, column=2)

        self.redimensionner_label = tk.Label(self.cadre_entree_uti, text="redimensionner :")
        self.redimensionner_entree = tk.Entry(self.cadre_entree_uti)
        self.redimensionner_label.grid(row=1, column=0)
        self.redimensionner_entree.grid(row=1, column=1)

        self.dimension_var = tk.StringVar()
        self.dimension_var.set("dimension :")
        self.dimension_label = tk.Label(self.cadre_entree_uti, textvariable=self.dimension_var)
        self.dimension_label.grid(row=2, column=0)

        self.bouton_maj = tk.Button(self.cadre_entree_uti, text="mettre à jour", command=self.afficher_image)
        self.bouton_maj.grid(row=2, column=1)

        self.chemin.grid(row=0, column=1)

        self.entree_x = tk.Entry(self.cadre_entree_uti)
        self.x_label = tk.Label(self.cadre_entree_uti, text="Point de départ :")
        self.x_label.grid(row=3, column=0)
        self.entree_y = tk.Entry(self.cadre_entree_uti)
        self.y_label = tk.Label(self.cadre_entree_uti, text="Point d'arrivée :")
        self.y_label.grid(row=4, column=0)

        self.entree_x.grid(row=3, column=1)
        self.entree_y.grid(row=4,column=1)
        self.bouton_coord.grid(row=5, column=0)

        self.etat_var = tk.StringVar()
        self.etat_var.set("repos")
        self.etat_label = tk.Label(self.cadre_entree_uti, textvariable=self.etat_var)
        self.etat_label.grid(row=5, column=1)

        self.racine.mainloop()

    def afficher_image(self, *args):
        """
        Méthode qui permet d'afficher l'image à l'écran, elle permet aussi de la mettre à jour, lorsque l'utilisateur le souhaite.
        :param args:
        """

        #Présence d'un try catch au cas où l'utilisateur ne sélectionne pas d'image et que cette méthode est appelée.
        try:
            print(self.liste_var.get())
            print(f"choix = {self.redimensionner_entree.get()}")

            #Si l'utilisateur n'a pas donné de coefficient pour redimensionner l'image, on le met à 1.
            if self.redimensionner_entree.get() == "":
                coef = 1
            else:
            #Sinon on en le cast en float, car la variable self.redimensionner_entree.get() est une chaine de caractères.
                coef = float(self.redimensionner_entree.get())

            #si l'utilisateur met à jour l'image, on efface tout ce qu'il y avait sur la canvas précédente, si elle existe.
            if self.canvas is not None:
                self.canvas.delete('all')
                self.sommets_var.set("sommets visités :")
                self.temps_var.set("temps :")

            #On va chercher l'image dans son répertoire.
            repertoire_courant = Path(__file__).parent
            self.chemin_image = repertoire_courant.parent/'res'/self.liste_var.get()
            self.image = Image.open(self.chemin_image)
            #On la redimensionne, la nouvelle_taille ne change pas si le coef est égal à 1.
            nouvelle_taille = (math.floor(self.image.width/coef), math.floor(self.image.height/coef))
            self.image = self.image.resize(size= nouvelle_taille)
            self.photo = ImageTk.PhotoImage(self.image)
            #On prépare la canvas pour afficher l'image dessus.
            self.canvas = tk.Canvas(self.cadre_image, width=self.image.width, height=self.image.height, borderwidth=0,highlightthickness=0, bg="#fe8e36")
            self.canvas.place(relx=0.5, rely=0.5, anchor="center")
            #On affiche l'image sur la canvas.
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            #On affiche les dimensions de l'image à l'écran, afin d'aider l'utilisateur à choisir des points.
            self.dimension_var.set(f"dimensions : {self.image.width},{self.image.height}")
        #Si on n'a pas trouvé l'image, on affiche un message à l'écran.
        except ValueError:
            self.etat_var.set("Veuillez entrer une valeur correcte.")
        except IsADirectoryError:
            self.etat_var.set("Veuillez entrer un chemin valide.")

    def afficher_chemin(self):
        """
        Méthode permettant d'afficher le chemin sur l'image, on utilise A étoile ici, il y a la possibilité de passer par Dijkstra mais
        pour des raisons de performances il est préférable de garder A étoile.
        La méthode prend le chemin retourné par A étoile et affiche chacun des points de ce chemin sur la canvas.
        """

        #Présence d'un try except au cas où l'utilisateur a mal donné les points ou n'a pas donné d'image correcte.
        try:
            print(self.entree_x.get(), self.entree_y.get())

            self.etat_var.set("Veuillez patienter.") #ne fonctionne pas, à changer.

            #Tout d'abord on récupère les deux points grâces aux entrées utilisateurs, puis on les linéarise.
            x_coord = (int(self.entree_x.get().split(',')[0]), int(self.entree_x.get().split(',')[1]))
            y_coord = (int(self.entree_y.get().split(',')[0]), int(self.entree_y.get().split(',')[1]))

            #Linéarisation des points.
            x = x_coord[1] * self.image.width + x_coord[0]
            y = y_coord[1] * self.image.width + y_coord[0]

            print(x,y)

            #Création d'un graphe à partir de l'image.
            graphe1 = image_vers_graphe.image(self.image)
            #Création du chemin avec a_étoile.
            chemin, sommets = graphe1.a_etoile(x,y, self.liste_heuristiques_var.get(), self.canvas, self.afficher_check_var.get())
            self.sommets_var.set(f"sommets visités : {sommets}")
            #chemin = graphe1.a_etoile_basique(x,y)


            self.temps_var.set(f"temps : {graphe1.graphe.liste_sommet[y].temps_depuis_source}")
            print(f"temps = {graphe1.graphe.liste_sommet[y].temps_depuis_source}")
            #chemin = graphe.dijkstra(x,y)

            self.etat_var.set("Terminé.")

            couleurs  = ['red', 'blue', 'green', 'yellow']
            match self.liste_heuristiques_var.get():
                case 'manhattan':
                    couleur = 'orange'
                case 'euclide':
                    couleur = 'yellow'
                case 'chebyshev':
                    couleur = 'red'
                case _:
                    couleur = 'green'

            #Affichage du chemin sur la canvas, boucle basique qui place un point rouge sur chaque pixel du chemin.
            for pixel in chemin:
                center_x = pixel % self.image.width
                center_y = pixel // self.image.width
                # Dessiner un petit point rouge

                #Code pour afficher de plus gros points, pas très beau.
                """
                self.canvas.create_oval(
                    center_x - 1,
                    center_y - 1,
                    center_x + 1,
                    center_y + 1,
                    fill="red",
                    outline="red"
                )
                """
                self.canvas.create_oval(
                    center_x,
                    center_y,
                    center_x,
                    center_y,
                    fill=couleur,
                    outline=couleur
                )

        except ValueError:
            self.etat_var.set("Veuillez entrer un point correct.")
        except IndexError:
            self.etat_var.set("Veuillez entrer un point correct.")