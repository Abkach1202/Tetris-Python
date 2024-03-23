# -*- coding:utf-8 -*-

########################################
## Abdoulaye KATCHALA MELE            ##
## PROG2 - 2022 - Université d'Artois ##
## Projet Tetris                      ##
########################################

#############################
## importation des modules ##
#############################
import modele
import tkinter

#############################
## procédures et fonctions ##
#############################

# Taille d'une case de tetris
DIM = 30
# Couleurs utilisées dans le jeu
COULEURS = ["red","blue","green","yellow","orange","purple","pink","cyan","dark grey","black"]
# Constante SUIVANT
SUIVANT = 6

class VueTetris :
    '''Classe qui permet de modeliser la vue du jeu Tetris'''
    def __init__(self,mod) :
        '''VueTetris,ModeleTetris -> VueTetris
        Permet de créer une instance de la classe VueTetris c'est à dire créer la fenêtre et
        lui ajouter ses composants
        '''
        # Sauvegarde le modele
        self.__modele = mod
        # Attribut Pause
        self.__pause = True

        # Création de la fenêtre et lui donne un titre
        self.__fen = tkinter.Tk()
        self.__fen.title("Tetris")

         # Création la frame du bouton Quitter le place
        fr_quit = tkinter.Frame(self.__fen)
        fr_quit.pack(side="right")

         # Creation et placement du label Forme_suivante
        forme_suiv = tkinter.Label(fr_quit,text="Forme suivante")
        forme_suiv.pack()
        
        # Création le canvas du terrain dnas la fenêtre et le canvas de la forme suivante dans la frame puis les places
        self.__can_terrain = tkinter.Canvas(self.__fen,width=mod.get_largeur()*DIM,height=mod.get_hauteur()*DIM)
        self.__can_fsuivante = tkinter.Canvas(fr_quit,width=DIM*SUIVANT,height=DIM*SUIVANT)
        self.__can_terrain.pack(side="left")
        self.__can_fsuivante.pack()

        # Création et placement des bouton et du label score
        btn_quit = tkinter.Button(fr_quit,text="Au revoir",command=self.__fen.destroy)
        self.__btn_ctrl = tkinter.Button(fr_quit,text="Commencer",command=self.ctrl_pause_recom)
        self.__lbl_score = tkinter.Label(fr_quit,text="Score : 0")
        self.__lbl_score.pack()
        self.__btn_ctrl.pack(side="bottom")
        btn_quit.pack(side="bottom")
        

        # Elle Crée les rectangles du terrain et les sauvegarde dans une Matrice
        self.__les_cases = list()
        for i in range(mod.get_hauteur()) :
            self.__les_cases.append(list())
            for j in range(mod.get_largeur()) :
                rect = self.__can_terrain.create_rectangle(j*DIM,i*DIM,(j+1)*DIM,(i+1)*DIM,outline="grey",fill=COULEURS[mod.get_valeur(i,j)])
                self.__les_cases[i].append(rect)
        
        # Elle Crée les rectangles de la forme suivante et les sauvegarde dans une Matrice
        self.__les_suivants = list()
        for i in range(SUIVANT) :
            self.__les_suivants.append(list())
            for j in range(SUIVANT) :
                suiv = self.__can_fsuivante.create_rectangle(j*DIM,i*DIM,(j+1)*DIM,(i+1)*DIM,outline="grey",fill=COULEURS[-1])
                self.__les_suivants[i].append(suiv)
        
    def fenetre(self) :
        '''VueTetris -> Tk
        Retourne la fenetre de l'application
        '''
        return self.__fen
    
    def dessine_case(self,i,j,coul) :
        '''VueTetris(inout),int,int,int -> rien
        Change la couleur de la case du terrain à la ligne i et colonne j à la couleur de l'indice coul
        '''
        # Change la couleur avec itemconfigure
        self.__can_terrain.itemconfigure(self.__les_cases[i][j],fill=COULEURS[coul])
    
    def dessine_terrain(self) :
        '''VueTetris(inout) -> rien
        Parcours les rectangles du canvas pour mettre à jour leurs couleurs et ainsi mettre 
        à jour le terrain
        '''
        # Parcours les cases du terrain 
        for i in range(self.__modele.get_hauteur()) :
            for j in range(self.__modele.get_largeur()) :
                # Met à jour la couleur de chaque case
                self.dessine_case(i,j,self.__modele.get_valeur(i,j))
        
    def dessine_forme(self,coords,couleur) :
        '''VueTetris(inout),list(tuple(int)),int -> rien
        Parcours coords pour changer la couleur de la case (le terrain) de coordonnées se trouvant dans coords à la couleur d'indice couleur
        '''
        # Parcours coords
        for i in coords :
            # Change la couleur de chaque case se trouvant dans coords en couleur
            self.dessine_case(i[1],i[0],couleur)
    
    def met_a_jour_score(self,val) :
        '''VueTetris(inout),int -> rien
        Configure le label score pour lui mettre val à la place de 0
        '''
        self.__lbl_score.config(text=f"Score : {val}")
    
    def dessine_case_suivante(self,x,y,coul):
        '''VueTetris(inout),int,int,int -> rien
        Change la couleur de la case de fsuivante à la ligne i et colonne j à la couleur de l'indice coul
        '''
        # Change la couleur avec itemconfigure
        self.__can_fsuivante.itemconfigure(self.__les_suivants[x][y],fill=COULEURS[coul])
    
    def nettoie_forme_suivante(self) :
        '''VueTetris(inout) -> rien
        Parcours self.__les_suivants pour rendre leurs couleurs noires
        '''
        # Parcours les suivants pour leurs mettre la couleur noire
        for i in range(SUIVANT) :
            for j in range(SUIVANT) :
                self.dessine_case_suivante(i,j,-1)
    
    def dessine_forme_suivante(self,coords,coul) :
        '''VueTetris(inout),list(tuple(int)),int -> rien
        Nettoie le canvas les_suivant et parcours coords pour changer la couleur de la case (les_suivants) de coordonnées se trouvant dans coords à la couleur d'indice couleur
        '''
        # Nettoie le canvas
        self.nettoie_forme_suivante()
        # Parcours coords
        for i in coords :
            # Change la couleur de chaque case se trouvant dans coords en couleur
            self.dessine_case_suivante(i[1]+2,i[0]+2,coul)
    
    def pause(self) :
        '''ModeleTetris -> bool
        Montre si le jeu est en pause ou pas
        '''
        return self.__pause

    def get_btn_ctrl(self) :
        '''VueTetris -> Button
        Retourne le bouton qui controle la pause et la reprise
        '''
        return self.__btn_ctrl
    
    def ctrl_pause_recom(self) :
        '''VueTetris -> rien
        Elle met leu jeu en marche et transforme le texte du bouton controle en Pause
        si la partie est en pause, si la parie est fini elle recommence le jeu;
        Si non elle met la partie en pause et transforme le texte en reprendre
        '''
        # Si la partie est en pause ou que la partie est finie
        if self.__pause or self.__modele.fini() :
            # Il remet le jeu en marche
            self.__pause = False
            # Réecrit le texte du bouton
            self.__btn_ctrl.config(text="Pause")
            # Si la partie est finie
            if self.__modele.fini() :
                # Il fait recommencer le jeu
                self.__modele.ctrl_recommencer()
        # Si non il met le jeu en pause et réecrit le texte du bouton
        else :
            self.__pause = True
            self.__btn_ctrl.config(text="Reprendre")
            
    
    # Fin de la classe VueTetris