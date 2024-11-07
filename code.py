from tkinter import *
from tkinter.messagebox import *
from tkinter.ttk import Style
import json
from datetime import datetime, timedelta
from tkinter import simpledialog
import re
import math

# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Participant:
    def __init__(self, nom, prenom, entree, plat, dessert, boisson):
        self.nom = nom
        self.prenom = prenom
        self.entree = entree
        self.plat = plat
        self.dessert = dessert
        self.boisson = boisson
    
    def get_entree(self):
        return self.entree
    
    def get_plat(self):
        return self.plat
    
    def get_dessert(self):
        return self.dessert
    
    def get_boisson(self):
        return self.boisson
    
    def get_nom(self):
        return self.nom
    
    def get_prenom(self):
        return self.prenom
    
    def objet_class_to_object_json(self):
        return { "nom"     : self.nom,
                
                 "prenom"  : self.prenom,
                 
                 "entree"  : self.entree,
                 
                 "plat"    : self.plat,
                 
                 "dessert" : self.dessert,
                 
                 "boisson" : self.boisson
        }
    
    
    def objet_object_json_to_class(self, json_participant):
        return Participant(
            json_participant["nom"],
            
            json_participant["prenom"],
            
            json_participant["entree"],
            
            json_participant["plat"],
            
            json_participant["dessert"],
            
            json_participant["boisson"]
        )
    def afficher(self):
        res= "Le participant " + self.prenom + " " + self.nom + " a amené "
        if self.entree > 0:
            res += str(self.entree) +" entrée"
            if self.entree > 1 :
                res += "s"
            res += ", "
        if self.plat > 0:
            res += str(self.plat) + " plat"
            if self.plat > 1:
                res += "s"
            res += ", "
        if self.dessert > 0:
            res += str(self.dessert) + " dessert"
            if self.dessert > 1:
                res += "s"
                res += ", "
        if self.boisson > 0 :
            res += str(self.boisson) + " boisson"
            if self.boisson > 1:
                res += "s"
            res += "."
            
        return res        
            
        
class Repas(Participant):
    def __init__(self, bar, bar_var,jours_restant, nb_participants_var, canvas, origin_x, origin_y, radius):
        self.dessert = 0
        self.entree = 0
        self.plat = 0
        self.boisson = 0
        self.nbAssette = 30
        self.date_evenement = ""

        self.liste_des_participants_str = []
        self.liste_des_participants_object = []
        self.charger_historique(bar, bar_var, jours_restant)
        nb_participants_var.set(len(self.liste_des_participants_object))
        self.creer_graphique(canvas, origin_x, origin_y, radius)
        
    #Avoir le nombre de desserts enrégistrés    
    def get_dessert(self):
        return self.dessert
    
    #Pour avoir le nombre de plats enrégistrés
    def get_plat(self):
        return self.plat
    
    #Pour avoir le nombre d'entrées enrégistrées
    def get_entree(self):
        return self.entree
    
    
    #Pour avoir le nombre de boissons enrégistrées
    def get_boisson(self):
        return self.boisson
    
    
    
    #Pour avoir le nombre de places réserves
    def get_nbAssette(self):
        return self.nbAssette
        
    #Pour avoir la liste des participants    
    
        
    def get_next_color(self,i):
        """
        Retourne la prochaine couleur dans une séquence prédéfinie.

        Returns:
            str: Nom de la couleur.
        """
        
        colors = ['#317AC1', '#FF9CB6', '#CA7C5C', '#A4BD01']
        color = colors[i % len(colors)]
        return color
    
    def calculer_pourcentages(self):
        # Calculer le total de toutes les parties
        total = self.entree + self.plat + self.dessert + self.boisson

        # Calculer les pourcentages pour chaque catégorie
        pourcentage_entree = (self.entree / total) * 100
        pourcentage_plat = (self.plat / total) * 100
        pourcentage_dessert = (self.dessert / total) * 100
        pourcentage_boisson = (self.boisson / total) * 100

        return {
            "entree": pourcentage_entree,
            "plat": pourcentage_plat,
            "dessert": pourcentage_dessert,
            "boisson": pourcentage_boisson
        }
    #la fonction qui crée le graphe
    def creer_graphique(self, canvas, origin_x, origin_y, radius):
        data = [self.entree, self.plat, self.dessert, self.boisson]
        categories = ["Entrée", "Plat", "Dessert", "Boisson"]
        total = sum(data)
        start_angle = 0

        for i, value in enumerate(data):
            angle = 360 * (value / total)
            end_angle = start_angle + angle
            self.dessiner_tranche_de_graphe(canvas, origin_x, origin_y, radius, start_angle, end_angle, categories[i],i, value, total)
            start_angle = end_angle
            
    def dessiner_tranche_de_graphe(self, canvas, origin_x, origin_y, radius, start_angle, end_angle, categorie,i, value, total):
        
        start_angle_rad = math.radians(start_angle)
        end_angle_rad = math.radians(end_angle)

        # Calcul des coordonnées du point de départ et du point d'arrivée de l'arc
        x_start = origin_x + radius * math.cos(start_angle_rad)
        y_start = origin_y - radius * math.sin(start_angle_rad)
        x_end = origin_x + radius * math.cos(end_angle_rad)
        y_end = origin_y - radius * math.sin(end_angle_rad)

        # Dessiner l'arc sur le canvas
        canvas.create_arc(
            origin_x - radius, origin_y - radius, 
            origin_x + radius, origin_y + radius, 
            start=start_angle, extent=(end_angle - start_angle), 
            fill=self.get_next_color(i)
        )

        # Calculer le point milieu de l'arc pour placer le label
        mid_angle = (start_angle + end_angle) / 2
        mid_angle_rad = math.radians(mid_angle)
        label_radius = radius * 0.8  # distance du label du centre

        # Coordonnées du point du label
        label_x = origin_x + label_radius * math.cos(mid_angle_rad)
        label_y = origin_y - label_radius * math.sin(mid_angle_rad)

        # Afficher le label        
        percentage = (value / total) * 100
        canvas.create_text(label_x, label_y, text=f"{categorie}\n{percentage:.1f}%", font=("Arial", 10))
        
        
    #La fonction vérifie  s'il ya a pas un granf écart entre les différentes catégories pour eviter les grands écarts entre les catégories     
    def check_gap(self, max, participant):
        mes = ""
        liste_categogries = [("entree",self.entree + participant.get_entree()), ("plat",self.plat + participant.get_plat()), ("dessert",self.dessert + participant.get_dessert()), ("boisson", self.boisson + participant.get_boisson())]
        for i in range(len(liste_categogries)):
            for j in range(i+1, len(liste_categogries)):
                if abs(liste_categogries[i][1] - liste_categogries[j][1]) > max :
                    mes += f"l'écart entre {liste_categogries[i][0]}(={liste_categogries[i][1]}) et {liste_categogries[j][0]}(={liste_categogries[j][1]}) > {max}\n"
        return mes[:-1]
    #Une fonction intermédiare qui permet de vo=ider u champs
    def vider_champ(self, frame):
        for wdget in frame.winfo_children():
            if wdget.winfo_class() == "Entry":
                wdget.delete(0, END)
            if wdget.winfo_class() == "Spinbox":
                wdget.delete(0, END)
                wdget.insert(0, 0)
    #lA fonction participer enregistre les données d'un participant avoir verifier si les données sont correctement choisies
    def participer(self, participant, participation_frame, bar, bar_var, nb_participants_var, canvas, origin_x, origin_y, radius):
        #verifier le nom et le prenom:
        if participant.get_nom() == "" or participant.get_prenom() == "":
            showwarning("", "Remplir les champs nom et prénom pour pouvoir vous enrégistrer \n    Merci")
            return
        
        
        #Pour eviter l'ajout de categorie avec une quantite vide(ce qui n'a pas trop de chance)
        if participant.get_entree() == 0 and participant.get_plat() == 0 and participant.get_dessert() == 0 and  participant.get_boisson() == 0:
            showwarning("","La quantité de votre participation\n ne doit pas etre nulle.\n\nVeiller choisir une quantité non nulle pour au moins une catégorie pour pouvoir vous enrégistrer\n\nMerci")
            return
        mes =  self.check_gap(5, participant)
        
        #Mais aussi eviter l'ajout d'une quantité d'entrées superieur au nombre d'assiettes (pour visualiser des données rationnelles)
        if participant.get_entree() > self.get_nbAssette():
            showwarning("","La quantité de votre participation\n est supérieure au nombre de places reservées.\n\nPenser à augmenter le nombre de places \npuis recommencer.\n\nMerci")
            return
        if participant.get_entree() + self.entree > self.get_nbAssette():
            showwarning("","La quantité de votre participation plus(+)\nla quantité existante est supérieure au\n nombre de places reservées.\n\nPenser à augmenter le nombre de places \npuis recommencer.\n\nMerci")
            return
        
        #Mais aussi eviter l'ajout d'une quantité de plats superieur au nombre d'assiettes (pour visualiser des données rationnelles)
        if participant.get_plat() > self.get_nbAssette():
            showwarning("","La quantité de votre participation\n est supérieure au nombre de places reservées.\n\nPenser à augmenter le nombre de places \npuis recommencer.\n\nMerci")
            return
        if participant.get_plat() + self.plat > self.get_nbAssette():
            showwarning("","La quantité de votre participation plus(+)\nla quantité existante est supérieure au\n nombre de places reservées.\n\nPenser à augmenter le nombre de places \npuis recommencer.\n\nMerci")
            return
        
        
        #Mais aussi eviter l'ajout d'une quantité de desserts superieur au nombre d'assiettes (pour visualiser des données rationnelles)
        if participant.get_dessert() > self.get_nbAssette():
            showwarning("","La quantité de votre participation\n est supérieure au nombre de places reservées.\n\nPenser à augmenter le nombre de places \npuis recommencer.\n\nMerci")
            return
        if participant.get_dessert() + self.dessert > self.get_nbAssette():
            showwarning("","La quantité de votre participation plus(+)\nla quantité existante est supérieure au\n nombre de places reservées.\n\nPenser à augmenter le nombre de places \npuis recommencer.\n\nMerci")
            return
        
        #Mais aussi eviter l'ajout d'une quantité de boissons superieur au nombre d'assiettes (pour visualiser des données rationnelles)
        if participant.get_boisson() > self.get_nbAssette():
            showwarning("","La quantité de votre participation\n est supérieure au nombre de places reservées.\n\nPenser à augmenter le nombre de places \npuis recommencer.\n\nMerci")
            return
        if participant.get_boisson() + self.boisson > self.get_nbAssette():
            showwarning("","La quantité de votre participation plus(+)\nla quantité existante est supérieure au\n nombre de places reservées.\n\nPenser à augmenter le nombre de places \npuis recommencer.\n\nMerci")
            return
        
        if mes != "":
            showwarning("", f"Aprés enrégistrement de vos données\n {mes}\nPour une bonne organisation l'écart entre les catégories ne doit pas dépasser 5\nMerci de réessayer avec d'autres valeurs")
            self.vider_champ(participation_frame)
            print(participation_frame.winfo_children)
            return
        #Si tous les controle reussissent alors on enréistre les valeurs renseignées
        self.entree = self.entree + participant.get_entree()
        self.plat = self.plat + participant.get_plat()
        self.dessert = self.dessert + participant.get_dessert()
        self.boisson = self.boisson + participant.get_boisson()
        
        self.liste_des_participants_str.append(participant.afficher())
        self.liste_des_participants_object.append(participant)
        
        #en fin remplir nos progessbar
        bar_var[0].set(self.entree)
        bar_var[1].set(self.plat)
        bar_var[2].set(self.dessert)
        bar_var[3].set(self.boisson)
        self.change_color(bar[0], bar[1], bar[2], bar[3])
        nb_participants_var.set(len(self.liste_des_participants_object))
        self.sauvegarder_historique()
        self.creer_graphique(canvas, origin_x, origin_y, radius)
        participation_frame.destroy()
        
        
    #UNE FONCTION QUI PERMET DE RECUPERER LES INFORMATIONS D'UN PARTICIPANT EN OUVRANT UN FRAME
    def participerBis(self, root, bar, bar_var, nb_participants_var, canvas, origin_x, origin_y, radius):
        participation_frame = Frame(root)
        participation_frame.grid(row=1, column=2, columnspan=2, rowspan=6)
        
        nom = StringVar()
        prenom = StringVar()
        entree = IntVar()
        plat = IntVar()
        dessert = IntVar()
        boisson = IntVar()
        
        titre_label = Label(participation_frame, text="Veiller remplir le formulaire suivant pour participer:", font=("Helvetica", 15))
        titre_label.grid(row=0, column=0, columnspan=2)
        nom_label = Label(participation_frame, text="Nom: ", font=("Times", 20), bg="#29abe2", fg="white", width=10)
        nom_label.grid(row=1, column=0,  padx=5, pady=1, sticky=E)
        nom_champ = Entry(participation_frame, width=20 , textvariable=nom)
        nom_champ.grid(row=1, column=1, sticky=W)

        prenom_label = Label(participation_frame, text="Prenom: ", font=("Times", 20), bg="#29abe2", fg="white", width=10)
        prenom_label.grid(row=2, column=0, padx=5, pady=1, sticky=E)
        prenom_champ = Entry(participation_frame, width=20 , textvariable=prenom)
        prenom_champ.grid(row=2, column=1, sticky=W)


       

        entree_label = Label(participation_frame, text="Entrée", font=("Times", 20), bg="#29abe2", fg="white", width=10)
        entree_label.grid(row=3, column=0, padx=5, pady=1, sticky=E)
        
        entree_spinbox = Spinbox(participation_frame, textvariable=entree, width=18, from_= 0, to=100, wrap="False")
        entree_spinbox.grid(row=3, column=1, sticky=W)
        
        
        
        plat_label = Label(participation_frame, text="Plat", font=("Times", 20), bg="#29abe2", fg="white", width=10)
        plat_label.grid(row=4, column=0, padx=5, pady=1, sticky=E)
        
        plat_spinbox = Spinbox(participation_frame, textvariable=plat, width=18, from_= 0, to=100, wrap="False")
        plat_spinbox.grid(row=4, column=1, sticky=W)
        
        
        
        dessert_label = Label(participation_frame, text="Dessert", font=("Times", 20), bg="#29abe2", fg="white", width=10)
        dessert_label.grid(row=5, column=0, padx=5, pady=1, sticky=E)
        
        dessert_spinbox = Spinbox(participation_frame, textvariable=dessert, width=18, from_= 0, to=100, wrap="False")
        dessert_spinbox.grid(row=5, column=1, sticky=W)
        
        
        
        
        boisson_label = Label(participation_frame, text="Boisson", font=("Times", 20), bg="#29abe2", fg="white", width=10)
        boisson_label.grid(row=6, column=0, padx=5, pady=1, sticky=E)
        
        boisson_spinbox = Spinbox(participation_frame, textvariable=boisson, width=18, from_= 0, to=100, wrap="False")
        boisson_spinbox.grid(row=6, column=1, sticky=W)
        
        
        


        button_participer = Button(participation_frame,cursor="hand2", text="Enrégistrer", font=("italic", 14), bg="green4", fg="white", command=lambda:self.participer(Participant(nom.get(), prenom.get(), entree.get(), plat.get(), dessert.get(), boisson.get()), participation_frame, bar, bar_var, nb_participants_var, canvas, origin_x, origin_y, radius))
        button_participer.grid(row=7, column=0, padx=50, pady=30, sticky=W)


        button_annuler = Button(participation_frame,cursor="hand2", text="Annuler", font=("italic", 14), bg="red4", fg="white", command=lambda:participation_frame.destroy())
        button_annuler.grid(row=7, column=1, padx=50, pady=30, sticky=W)
    
    
    def is_survoler(self, event, buton_supprimer_participant, var):
        buton_supprimer_participant.config(bg="red")
        var.set("Veillez selectionner dans la \nliste ci_desssus pour supprimer")
    
    def is_not_survoler(self, event, buton_supprimer_participant, var):
        buton_supprimer_participant.config(bg="#FFFFFF")
        var.set("")
    #la fonction qui permet de supprimer un ou plusieurs participants.
    def supprimer_participants(self,listebox_des_participants_var, listebox_des_participants, bar, bar_var, nb_participants_var, canvas, origin_x, origin_y, radius):
        #Verifier si au moins un participant est selectionné
        if not listebox_des_participants.curselection():
            showinfo("","aucun participant n'est sélectionne !")
        #si un seul est selectionné
        if len(listebox_des_participants.curselection()) == 1:
            question = askokcancel("", "Voulez-vous vrément supprimer ce participant ?")
            if question == YES:
                pass
            else :
                showinfo("", "La suppression est annulé !")
                return
        if len(listebox_des_participants.curselection()) > 1:
            question = askokcancel("", "Voulez-vous vrément supprimer ces participants ?")
            if question == YES:
                pass
            else :
                showinfo("", "La suppression est annulé !")
                return        
        for index_part in reversed(listebox_des_participants.curselection()):
            self.entree -= self.liste_des_participants_object[index_part].get_entree()
            self.plat -= self.liste_des_participants_object[index_part].get_plat()
            self.dessert -= self.liste_des_participants_object[index_part].get_dessert()
            self.boisson -= self.liste_des_participants_object[index_part].get_boisson()
            
            del self.liste_des_participants_str[index_part]
            del self.liste_des_participants_object[index_part]
        #aprés avoir supprimer, on met à jour les couleurs des bars
        self.change_color(bar[0], bar[1], bar[2], bar[3])
        bar_var[0].set(self.entree)
        bar_var[1].set(self.plat)
        bar_var[2].set(self.dessert)
        bar_var[3].set(self.boisson)
        #on met à jour les liste des participants
        listebox_des_participants_var.set(self.liste_des_participants_str)
        nb_participants_var.set(len(self.liste_des_participants_object))
        #on suvegarde de nouveau
        self.sauvegarder_historique() 
        #on refait notre graphe aussi
        self.creer_graphique(canvas, origin_x, origin_y, radius)   
    #Cette focntion sauvegarde les donner dans le ficheir json a chaque fois qu'elle est appelée(participatio ou suppression)
    def sauvegarder_historique(self):
        
        liste_des_participants_json = [part.objet_class_to_object_json() for part in self.liste_des_participants_object]
        historique = {
            "les_participants_object" : liste_des_participants_json,
            
            "les_participants_str"    : self.liste_des_participants_str,
            
            "les_entrees"             : self.entree,
            
            "les_plats"               : self.plat,
            
            "les_desserts"            : self.dessert,
            
            "les_boissons"            : self.boisson,
            
            "date_evenement"           :self.date_evenement
        }
        
        mon_fichier = "sauvegarde.json"
        with open(mon_fichier, "w") as f :
            json.dump(historique, f, indent=5)
    
    #Cette fonction permet de charger les données sauvegardées précédamment  quand l'appliquation est ouverte        
    def charger_historique(self, bar, bar_var,jours_restant):
        #overture dsu fichier et récupération des données 
        with open("sauvegarde.json", "r") as f :
            historique = json.load(f)

        self.liste_des_participants_object = [self.objet_object_json_to_class(part) for part in historique["les_participants_object"]]
        self.liste_des_participants_str = historique["les_participants_str"]
        self.entree = historique["les_entrees"]
        self.plat = historique["les_plats"]
        self.dessert = historique["les_desserts"]
        self.boisson = historique["les_boissons"]

        bar_var[0].set(self.entree)
        bar_var[1].set(self.plat)
        bar_var[2].set(self.dessert)
        bar_var[3].set(self.boisson)
        self.change_color(bar[0], bar[1], bar[2], bar[3])
        
        
        # Récupérer la date de l'événement depuis l'historique
        date_evenement_str = historique["date_evenement"]

        # Convertir la date de l'événement en objet datetime
        date_evenement = datetime.strptime(date_evenement_str, "%d/%m/%Y")

        # Calculer le nombre de jours restants jusqu'à la date de l'événement
        current_date = datetime.now()
        jours_restants = (date_evenement - current_date).days

        # Stocker le nombre de jours restants dans la variable jours_restant
        jours_restant.set(jours_restants)

        # Enregistrer la date de l'événement dans l'attribut de l'instance
        self.date_evenement = date_evenement_str
        
    #cette fonction permet de voir la liste des participants dans une fenetre toplevel avec deux boutons: l'un pour supprimer un ou plusieurs participants et un autre pour fermer la fenetre          
    def voir_les_participants(self, root, bar, bar_var, nb_participants_var, canvas, origin_x, origin_y, radius):
        toplevel_liste_des_participants = Toplevel(root)
        listebox_des_participants_var = StringVar()
        #on charge la liste des participants(n chaine de caractere) de l'objet repas initié dans la variable listevar du widget lisbox.
        listebox_des_participants_var.set(self.liste_des_participants_str)
        listebox_des_participants = Listbox(toplevel_liste_des_participants, listvariable= listebox_des_participants_var, width=70, height=15, selectmode=MULTIPLE)
        listebox_des_participants.grid(row=0, column=0, columnspan=4,rowspan=3, padx=50, pady=50)
        #Le bouton qui détruit le toplevel.
        button_fermer = Button(toplevel_liste_des_participants,cursor="hand2", text="X", bg='red', fg='white', font=("Times", 20), command=lambda:toplevel_liste_des_participants.destroy())
        button_fermer.grid(row=4, column=3)
        var = StringVar()
        bul_label = Label(toplevel_liste_des_participants, textvariable=var, font=('Times', 15))
        bul_label.grid(row=3, column=0)
        buton_supprimer_participant = Button(toplevel_liste_des_participants,cursor="hand2", text='Supprimer des participants', bg='#FFFFFF', fg='black', font=("Times", 20), command=lambda:self.supprimer_participants(listebox_des_participants_var, listebox_des_participants, bar, bar_var, nb_participants_var, canvas, origin_x, origin_y, radius))
        #La définition d'un évènement: quand on on survole le bouton supprimer, s'afficxhe l'expliquation de la manière de supprimer.
        buton_supprimer_participant.bind("<Enter>", lambda event: self.is_survoler(event, buton_supprimer_participant, var))
        buton_supprimer_participant.bind("<Leave>", lambda event: self.is_not_survoler(event, buton_supprimer_participant, var))
        buton_supprimer_participant.grid(row=4, column=0)
    #Une fonction qui change la couleur (rouge bleu vert) pour chaque pourcentage de la bar de visualisation()
    
    #La fonction qui permet changer la couleur des progressbar, en fonction du pourcentage de remplissage des bars
    def change_color(self, entree_bar, plat_bar, dessert_bar, boisson_bar):
        #C'est la définitio de 4 styles de couleurs correspondant 4 poucentages(entre 0 et 25,entre 25 et 50,entre 50 et 75, entre 75 et 100 ) 
        red = Style()
        red.theme_use('alt')
        red.configure("red.Vertical.TProgressbar", background = 'red')
        
        pink = Style()
        pink.theme_use('alt')
        pink.configure("pink.Vertical.TProgressbar", background = 'pink')
        
        blue = Style()
        blue.theme_use('alt')
        blue.configure("blue.Vertical.TProgressbar", background = 'blue')
        
        green = Style()
        green.theme_use('alt')
        green.configure("green.Vertical.TProgressbar", background = 'green')
        barres = [entree_bar, plat_bar, dessert_bar, boisson_bar]
        
        #A chaque opération de participation ou de suppression, on parcourt les progressbars et on redefinit les couleurs en fonction des pourcentages
        for bar in barres :
            val = bar.cget("value")
            if val / self.nbAssette*100 <= 25:
                bar.config(style="red.Vertical.TProgressbar")
            elif 25 < val / self.nbAssette*100 <= 50:
                bar.config(style="pink.Vertical.TProgressbar")
            elif 50 < val / self.nbAssette*100 <= 75:
                bar.config(style="blue.Vertical.TProgressbar")
            else :
                bar.config(style="green.Vertical.TProgressbar")
    #la fonction qui permet de demander la date de l'evenement et d'afficher le nombre de jours qui reste avant la fete        
    def definir_date_evenement(self,nbjour_restant) :
        date_saisie = simpledialog.askstring("", "Saisir la date de l'evenement sous\nle format le format jj/mm/aaaa.")
        if not re.match(r'^\d{2}/\d{2}/\d{4}$', str(date_saisie)):
            showerror("Erreur", "Format de date incorrect.\nUtilisez le format jj/mm/aaaa.")
            return
        date_evenement = datetime.strptime(str(date_saisie), "%d/%m/%Y")
        current_date = datetime.now()
        if (date_evenement - current_date).days <0 :
            showerror("", "la date entré doit etre égale ou \npostérieure à la date d'aujourd'hui")
        nbjour_restant.set((date_evenement - current_date).days)
        self.date_evenement = date_saisie
        #on sauvegarde la date dans notre fichier json.
        self.sauvegarder_historique()

