# -*- coding:utf-8 -*-

########################################
## Abdoulaye KATCHALA MELE            ##
## PROG2 - 2022 - Université d'Artois ##
## Projet Tetris                      ##
########################################

#############################
## importation des modules ##
#############################
from random import randint

#############################
## procédures et fonctions ##
#############################

# Les 7 types de formes
LES_FORMES = [[(-1,1),(-1,0),(0,0),(1,0)],[(-1,0),(0,0),(0,1),(1,1)],[(-1,1),(0,1),(0,0),(1,0)],[(-1,0),(0,0),(1,0),(1,1)],[(-1,1),(0,1),(0,0),(1,1)],[(0,0),(1,0),(1,1),(0,1)],[(0,0),(0,1),(0,2),(0,3)],[(-1,1),(-1,0),(0,0),(1,0),(1,1)]]

class ModeleTetris :
    '''Classe qui permet de modeliser le modele du jeu Tetris'''
    def __init__(self,nb_lig=24,nb_col=14) :
        '''ModeleTetris,int,int -> ModeleTetris
        Permet de creer une instance du modele du jeu caracterisé par tous ses composants
        '''
        # Attribut nombre de ligne (incluant la parie grise)
        self.__haut = nb_lig
        # Attribut nombre de colonne
        self.__larg = nb_col
        # Attribut base 
        self.__base = 4
        # Attribut score
        self.__score = 0
        # Attribut forme suivante
        self.__suivante = Forme(self)
        # Attribut coef
        self.__coef = 1
        # Attribut delai
        self.__delai = 320

        # Attribut Terrain qui est une matrice
        self.__terrain = list()
        for i in range(self.__haut) :
            self.__terrain.append(list())
            for j in range(self.__larg) :
                if i < 4 :
                    self.__terrain[i].append(-2)
                else :
                    self.__terrain[i].append(-1)
        # Attribut Forme
        self.__forme = Forme(self)
    
    def get_largeur(self) :
        '''ModeleTetris -> int
        Retourne le nombre de colonne du terrain du jeu
        '''
        return self.__larg
    
    def get_hauteur(self) :
        '''ModeleTetris -> int
        Retourne le nombre de ligne du terrain du jeu
        '''
        return self.__haut
    
    def get_valeur(self,lig,col) :
        '''ModeleTetris,int,int -> int
        Retourne la valeur de la case de coordonnées lig col dans le terrain du jeu
        '''
        return self.__terrain[lig][col]
    
    def est_occupe(self,lig,col) :
        '''ModeleTetris,int,int -> bool
        Retourne Vrai si la case est occupé c'est à dire que la valeur contenu dans la case est 
        negative et Faux si non
        '''
        return self.__terrain[lig][col] >= 0
    
    def fini(self) :
        '''ModeleTetris -> bool
        Retourne Vrai si au moins une case de la ligne noire la plus haute est occupée
        '''
        # Parcours la ligne noire la plus haute pour voir si il y'a une case qui est occupé
        for i in range(self.__larg) :
            if self.est_occupe(self.__base,i) :
                return True
        # Si il n'y a aucune case elle retourne Faux
        return False

    def ajoute_forme(self) :
        '''ModeleTetris(inout) -> rien
        Parcours les coordonnées absolues de la forme affecte la valeur de la couleur de
        la forme aux case du terrain
        '''
        # Parcours les coordonnées absolues de la forme
        for i in self.__forme.get_coords() :
            # Affecte la valeur de la couleur de la forme à la case de ces coordonées
            self.__terrain[i[1]][i[0]] = self.__forme.get_couleur()
        return
    
    def forme_tombe(self) :
        '''ModeleTetris(inout) -> bool
        Fait tomber la forme en appellant la fonction tombe et retourne Faux.
        Si la forme n'est pas tombé elle ajoute la forme sur le terrain, supprime les lignes completes,
        affecte la forme suivante à self.__forme et prend une nouvelle forme à self.__suivante puis retourne Vrai
        '''
        # On conserve le boolean issu de la collision ou non de la forme
        ya_collision = self.__forme.tombe()

        # Si il ya eu collision
        if ya_collision :
            # Elle ajoute la forme au terrain
            self.ajoute_forme()
            # Supprime les lignes completes
            self.supprime_lignes_completes()
            # Affecte la forme suivante à self.__forme et retourne Vrai
            self.__forme = self.__suivante
            # Nouvelle valeur à self.__suivante
            self.__suivante = Forme(self)
            return True

        # Si il n'y a pas eu collision il retourne Faux
        return False
    
    def get_couleur_forme(self) :
        '''ModeleTetris -> int
        Retourne la couleur de la forme actuelle (pas la suivante)
        '''
        return self.__forme.get_couleur()
    
    def get_coords_forme(self) :
        '''ModeleTetris -> list(tuple(int))
        Retourne les coordonnées absolues de self.__forme
        '''
        return self.__forme.get_coords()

    def forme_a_gauche(self) :
        '''ModeleTetris(inout) -> rien
        deplace la forme actuelle (pas la suivante) vers la gauche par sa methode a_gauche
        '''
        # Appelle la methode a_gauche pour deplacer la forme vers la gauche
        self.__forme.a_gauche()
    
    def forme_a_droite(self) :
        '''ModeleTetris(inout) -> rien
        deplace la forme actuelle (pas la suivante) vers la droite par sa methode a_droite
        '''
        # Appelle la methode a_droite pour deplacer la forme vers la droite
        self.__forme.a_droite()

    def forme_tourne(self) :
        '''ModeleTetris(inout) -> rien
        Demande à la forme actuelle (pas la suivante) de se tourner en appellant sa methode tourne
        '''
        # Demande à la forme de se tourner par sa methode tourner
        self.__forme.tourne()
    
    def est_ligne_complete(self,lig) :
        '''ModeleTeTris,int -> bool
        Parcours le terrain à la ligne d'indice lig et retourne Faux dès qu'elle tombe sur une case non occupée.
        Si elle trouve que des cases occupée, elle retourne Vrai
        '''
        # Il faudrait que lig soit valide
        assert self.__base <= lig < self.__haut
        
        # Parcours self.__terrain à l'indice lig
        for i in range(self.__larg) :
            # Dès qu'elle trouve une case non occupée elle retourne False
            if not self.est_occupe(lig,i) :
                return False
        # À l'inverse elle retourne True
        return True
    
    def supprime_ligne(self,lig) :
        '''ModeleTetris(inout),int -> rien
        Parcours le terrain en remontant en haut à partir de la ligne à l'indice lig et parcours la ligne aussi afin de affecter aux valeurs des cases de cette ligne
        les valeurs des cases de la ligne au dessus d'elle et à la première ligne une nouvelle ligne des valeurs de case non occupée
        '''
        # Parcours self.__terrain à partir de la ligne lig en remontant en haut
        for i in range(lig,self.__base-1,-1) :
            # Parcours la ligne aussi
            for j in range(self.__larg) :
                # Si elle a atteint la première ligne
                if i == self.__base :
                    # Elle affecte aux cases la valeur -1
                    self.__terrain[i][j] = -1
                # Si non elle affecte aux cases la valeur des cases au dessus
                else :
                    self.__terrain[i][j] = self.__terrain[i-1][j] 
    
    def supprime_lignes_completes(self) :
        '''ModeleTetris(inout) -> rien
        Parcours le terrain et teste si une ligne est complete; si c'est le cas il supprime la ligne et continue de parcourir le terrain
        Ensuite il rend le jeu plus rapide en fonction du score du joueur
        '''
        # Parcours le terrain
        for lig in range(self.__base,self.__haut) :
            # Si la ligne est complete
            if self.est_ligne_complete(lig) :
                # Elle supprime la ligne
                self.supprime_ligne(lig)
                self.__score += self.__coef
        # Rend le jeu plus rapide en fonction du score (Plus le score augmente plus le jeu est rapide)
        for i in range(5) :
            if 8*i <= self.__score <= 8*(i+1) :
                self.__delai = 320 - i*70
                self.__coef = i+1
        
    def get_score(self) :
        '''ModeleTetris -> int
        Retourne le score du joueur
        '''
        return self.__score
    
    def get_coords_suivante(self) :
        '''ModeleTetris -> int
        Retourne les coordonnées relatives de la forme suivante
        '''
        return self.__suivante.get_coords_relatives()
    
    def get_couleur_suivante(self) :
        '''ModeleTetris -> int
        Retourne la couleur de la forme suivante
        '''
        return self.__suivante.get_couleur()
    
    def ctrl_recommencer(self) :
        '''ModeleTetris(inout) -> rien
        Parcours le terrain pour rendre toutes les cases inouccupées c'est à dire
        leur valeur devient -1
        '''
        # Parcours le terrain
        for i in range(self.__haut) :
            for j in range(self.__larg) :
                # Affecte -2 aux cases appartenant aux lignes inferieurs à la base
                if i < self.__base :
                    self.__terrain[i][j] = -2
                # Affecte -1 aux restes des cases
                else :
                    self.__terrain[i][j] = -1
    
    def get_delai(self) :
        '''ModeleTetris(inout) -> rien
        Retourne le delai d'appel par défaut de joue
        '''
        return self.__delai
    

    # Fin de la classe ModeleTetris


class Forme :
    '''Classe permettant de modeliser une forme du jeu'''
    def __init__(self,mod) :
        '''Forme,ModeleTetris -> Forme
        Permet de creer une instance de la classe Forme caracterisé par le modele, sa couleur 
        les coordonnées de sa case pivot et sa forme
        '''
        # Attribut couleur
        self.__couleur = randint(0,7)
        # Attribut modele
        self.__modele = mod
        # Attribut Forme qui est la forme à l'indice self.__couleur de LES_FORMES
        self.__forme = LES_FORMES[self.__couleur][:]
        # Les Coordonnées de la case qui servira de pivot sur le terrain
        # Si la forme est le baton
        if self.__couleur == 6 :
            # Le x0 n'a plus de restrictions
            self.__x0 = randint(0,self.__modele.get_largeur()-1)
        else :
            # Si non il est restreint entre 1 et l'avant derbière colonne
            self.__x0 = randint(1,self.__modele.get_largeur()-2)
        # Le y0 reste 0 car la case d'origine relative est toujours celle qui est la plus haute
        self.__y0 = 0
    
    def get_couleur(self) :
        '''Forme -> int
        Retourne la couleur de la forme
        '''
        return self.__couleur
    
    def get_coords(self) :
        '''Forme -> list(tuple(int))
        Ajoute les coordonnées de la case pivot aux autres coordonnées dans self.__forme et
        retourne les coordonnées absolues de la forme sur le terrain
        '''
        # On crée une liste vide pour eviter de changer self.__forme
        coords = list()
        # Parcours self.__forme pour leur ajouter les coordonnées de la case pivot
        for i in self.__forme :
            coords.append((i[0]+self.__x0,i[1]+self.__y0))
        
        # Les retournes
        return coords
    
    def collision(self) :
        '''Forme -> bool
        Parcours les coordonnées de la forme dans le terrain et retourne Vrai si une des coordonnées 
        se trouve au dessus d'une case occupé ou à la ligne basse ou Faux si elle ne doit pas se poser
        '''
        # Parcours les coordonnées de la forme dans le terrain pour voir si la forme doit s'arrêter
        for i in self.get_coords() :
            # Si la case a atteint la plus basse ligne ou que la case en dessous est occupé il retourne Vrai 
            if i[1] == self.__modele.get_hauteur()-1 or self.__modele.est_occupe(i[1]+1,i[0]) :
                return True
        
        # Faux si la forme ne doit pas s'arrêter
        return False
    
    def tombe(self) :
        '''Forme(inout) -> bool
        Incrémente la valeur de l'attribut self.__y0 si il n'y a pas collision et 
        retourne Vrai si il ne l'a pas incrémenté
        '''
        # Si il y a eu collision il retourne Vrai
        if self.collision() :
            return True
        
        # Si non il incrémente et retourne Faux
        self.__y0 += 1
        return False

    def position_valide(self) :
        '''Forme -> bool
        Parcours les coordonnées absolues de la forme et teste si chaque coordonnée n'est
        pas occupée sur le terrain
        '''
        # Parcours les coordonnées absolues de la forme
        for coord in self.get_coords() :
            # dès qu'elle trouve une coordonnée occupée, elle retourne Faux
            if not(0 <= coord[0] < self.__modele.get_largeur() and 0 <= coord[1] < self.__modele.get_hauteur()) or self.__modele.est_occupe(coord[1],coord[0]) :
                return False
        # Si non elle retourne Vrai
        return True
    
    def a_gauche(self) :
        '''Forme(inout) -> rien
        déplace la forme d'une colonne vers la gauche c'est à dire desincremente la valeur de self.__x0
        et teste si la nouvelle position est valide; si non elle incremente sa valeur pour l'initialiser
        '''
        # Deplace la forme vers la gauche 
        self.__x0 -= 1
        
        # Si sa position est n'est pas valide elle incremente self.__x0 pour l'initialiser
        if not self.position_valide() :
            self.__x0 += 1
    
    def a_droite(self) :
        '''Forme(inout) -> rien
        déplace la forme d'une colonne vers la droite c'est à dire incremente la valeur de self.__x0
        et teste si la nouvelle position est valide; si non elle desincremente sa valeur pour l'initialiser
        '''
        # Deplace la forme vers la droite 
        self.__x0 += 1
        
        # Si sa position est n'est pas valide elle desincremente self.__x0 pour l'initialiser
        if not self.position_valide() :
            self.__x0 -= 1

    def tourne(self) :
        '''Forme(inout) -> rien
        Memorise les coordonnées de self.__forme dans une variable et remplace ces coordonnées par leurs images
        par la rotation de 90° et teste si sa position est valide, si non la forme reprend sa valeur memorisée
        '''
        # Memorise sa valeur dans forme_prec
        forme_prec = self.__forme.copy()

        # Parcours self.__forme
        for i in range(len(self.__forme)) :
            # Remplace les coordonnées par leur rotation
            self.__forme[i] = (-forme_prec[i][1],forme_prec[i][0])
        # Si la position n'est pas valide elle le remet à sa valeur initiale
        if not self.position_valide() :
            self.__forme = forme_prec
    
    def get_coords_relatives(self) :
        '''Forme -> list(tuple(int))
        Ajoute les coordonnées de la case pivot aux autres coordonnées dans self.__forme et
        retourne les coordonnées absolues de la forme sur le terrain
        '''
        return self.__forme.copy()

    # Fin de la classe Forme