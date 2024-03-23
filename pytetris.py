# -*- coding:utf-8 -*-

########################################
## Abdoulaye KATCHALA MELE            ##
## PROG2 - 2022 - Université d'Artois ##
## Projet Tetris                      ##
########################################

#############################
## importation des modules ##
#############################
from cgitb import text
import modele
import vue
import time

#############################
## procédures et fonctions ##
#############################

class Controleur :
    '''Classe permettant de modeliser le controleur du jeu Tetris'''
    def __init__(self,mod_tetris) :
        '''Controleur,ModeleTetris -> Controleur
        Permet de creer une instance de la classe controleur qui permettra de controler
        le modele et la vue
        '''
        # Attribut modele
        self.__modele = mod_tetris
        # Attribut vue
        self.__vue = vue.VueTetris(self.__modele)
        # Attribut fenetre
        self.__fen = self.__vue.fenetre()
        
        # Un Clique sur la flèche gauche deplace la forme vers la gauche
        self.__fen.bind("<Key-Left>",self.forme_a_gauche)
        # Un Clique sur la flèche droite deplace la forme vers la droite
        self.__fen.bind("<Key-Right>",self.forme_a_droite)
        # Un Clique sur la flèche bas deplace la forme plus rapidement vers le bas
        self.__fen.bind("<Key-Down>",self.forme_tombe)
        # Un Clique sur la flèche haut fait deplace la forme moins rapidement
        self.__fen.bind("<Key-Up>",self.forme_remonte)
        # Un Clique sur espace tourne la forme
        self.__fen.bind("<space>",self.forme_tourne)
        # Un Clique sur Entrée met le jeu en pause ou fait recommencer le jeu
        self.__fen.bind("<Return>",self.ctrl_pause_recom)

        # demande à la vue de dessiner la forme du modele et la forme suivante
        self.__vue.dessine_forme(self.__modele.get_coords_forme(),self.__modele.get_couleur_forme())
        self.__vue.dessine_forme_suivante(self.__modele.get_coords_suivante(),self.__modele.get_couleur_suivante())

        # Attribut delai
        self.__delai = self.__modele.get_delai()

        # Appel de la methode self.joue()
        self.joue()

        # Lancement de la boucle des evenements
        self.__fen.mainloop()
    
    def joue(self) :
        '''Controleur -> None
        boucle principale du jeu. Fait tomber une forme d’une ligne, réecrit le texte du bouton ctrl si le jeu est finie
        '''
        if not(self.__modele.fini() or self.__vue.pause()) :
            self.affichage()
        elif self.__modele.fini() :
            self.__vue.get_btn_ctrl().config(text="Recommencer")
        self.__fen.after(self.__delai,self.joue)
    
    def affichage(self) :
        '''Controleur(inout) -> None
        Elle fait tomber la forme d'une case (plus vite si on appuie sur la fleche bas), 
        puis demande à la vue de redessiner et la forme puis demande au modele le score pour le mettre à jour sur la vue
        Si il y'a collision elle remet le delai d'appel de joue à sa valeur en fonction du score et demande à la vue de dessiner la forme suivante en recuperant ses coordonnées et couleurs au près du modele 
        '''
        # Fait tomber la forme d'une case
        colli = self.__modele.forme_tombe()
        # Si il y'a collision
        if colli :
            # Elle remet self.__delai à sa valeur en fonction du score
            self.__delai = self.__modele.get_delai()
            # Elle demande à la vue de dessiner la forme suivante en recuperant sa couleur et ses coordonnées au près du modele
            self.__vue.dessine_forme_suivante(self.__modele.get_coords_suivante(),self.__modele.get_couleur_suivante())
        
        # La vue redessine son terrain
        self.__vue.dessine_terrain()
        # La vue redessine la forme
        self.__vue.dessine_forme(self.__modele.get_coords_forme(),self.__modele.get_couleur_forme())
        # Demande au modele le score
        val = self.__modele.get_score()
        # Met le score à jour
        self.__vue.met_a_jour_score(val)

    def forme_a_gauche(self,event) :
        '''Controleur(inout),event -> rien
        demande à self.__modele de se deplacer à gauche par sa methode forme_a_gauche
        '''
        # Appelle la methode forme_a_gauche de self.__modele pour le deplacer à gauche 
        self.__modele.forme_a_gauche()

    def forme_a_droite(self,event) :
        '''Controleur(inout),event -> rien
        demande à self.__modele de se deplacer à droite par sa methode forme_a_droite
        '''
        # Appelle la methode forme_a_droite de self.__modele pour le deplacer à droite 
        self.__modele.forme_a_droite()
    
    def forme_tombe(self,event) :
        '''Controleur(inout),event -> rien
        diminue la valeur de self.__delai pour faire tomber la forme plus rapidement
        '''
        # diminue self.__delai en lui soustrayant 90 si la difference est positif
        if self.__delai - 90 >= 0:
            self.__delai -= 90
    
    def forme_tourne(self,event) :
        '''Controleur(inout) -> rien
        Demande au modele de se tourner en appellant sa methode forme_tourne
        '''
        # Demande au modele de se tourner par sa methode forme_tourne
        self.__modele.forme_tourne()
    
    def forme_remonte(self,event) :
        '''Controleur(inout) -> rien
        augmente la valeur de self.__delai pour faire tomber la forme moins vite si elle est inferieur à 320
        '''
        # Augmente self.__delai en lui ajoutant 90 si l'addition est inférieur à 320
        if self.__delai + 90 <= self.__modele.get_delai():
            self.__delai += 90

    def ctrl_pause_recom(self,event) :
        '''Controleur,event -> rien
        Appelle la methode ctrl_pause_recom de la clase VueTetris
        '''
        self.__vue.ctrl_pause_recom()
    

    # Fin de la classe Controleur

###########################
###########################
### PROGRAMME PRINCIPAL ###
###########################
###########################

if __name__ == "__main__" :
    # création du modèle
    tetris = modele.ModeleTetris()
    
    # création du contrôleur. c’est lui qui créé la vue
    # et lance la boucle d’écoute des évts
    ctrl = Controleur(tetris)