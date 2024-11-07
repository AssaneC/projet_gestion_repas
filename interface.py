from tkinter import *
from tkinter.ttk import Progressbar, Style
import code
from tkinter import *

 
root = Tk()
root.title("Participation au repas de la promo")
root.config(bg="#efeded")
#les stringvars pour gerer le progressbars
entree_var = IntVar()

plat_var = IntVar()

dessert_var = IntVar()

boisson_var = IntVar()

nb_jours_avant_la_fete = Label(root,font=("italic", 15), text="  jj- avant la fete:                          ")
nb_jours_avant_la_fete.grid(row=0 , column=0, pady=10)

nb_jours_avant_la_fete_var = StringVar()

button_donner_date_evenement = Button(root, text="J-J", cursor="hand2" ,bg="#9AC8EB", command=lambda:repas1.definir_date_evenement(nb_jours_avant_la_fete_var))
button_donner_date_evenement.grid(row=0, column=2)

nombre_de_jours_avant_la_fete = Label(root,font=("italic", 15), textvariable=nb_jours_avant_la_fete_var, bg="#efeded")
nombre_de_jours_avant_la_fete.grid(row=0, column=1)


nb_participants_label = Label(root, font=("italic", 15), text="Nombre de personnes à la fête:")
nb_participants_label.grid(row=1, column=0)


nb_participants_var = IntVar()

nombre_de_personnes = Label(root, font=("italic", 15), textvariable=nb_participants_var, bg="#efeded")
nombre_de_personnes.grid(row=1, column=1)

frame_des_progressbar = Frame(root, bg="#efeded")
frame_des_progressbar.grid(row=3, column=0, columnspan=3, pady= 70)

entree_bar = Progressbar(frame_des_progressbar, orient="vertical", length=200, mode="determinate", variable=entree_var , maximum=30)
plat_bar = Progressbar(frame_des_progressbar, orient="vertical", length=200, mode="determinate", variable=plat_var , maximum=30)
dessert_bar = Progressbar(frame_des_progressbar, orient="vertical", length=200, mode="determinate", variable=dessert_var , maximum=30)
boisson_bar = Progressbar(frame_des_progressbar, orient="vertical", length=200, mode="determinate", variable=boisson_var, maximum=30)
bar = [entree_bar, plat_bar, dessert_bar, boisson_bar]
bar_var = [entree_var, plat_var, dessert_var, boisson_var]

frame_pie_chart = Frame(root, bg="#eeeeee")
frame_pie_chart.grid(row=3, column=3, columnspan=2, pady=20)



canvas_width = 300
canvas_height = 300
canvas = Canvas(frame_pie_chart, width=canvas_width, height=canvas_height, bg="white")
canvas.pack()

origin_x = canvas_width // 2
origin_y = canvas_height // 2
radius = min(canvas_width, canvas_height) // 3

repas1 = code.Repas(bar, bar_var, nb_jours_avant_la_fete_var, nb_participants_var, canvas, origin_x, origin_y, radius)


but_participer = Button(root, text="Nouveau participant   ", font=("italic", 14),cursor="hand2", bg="#29abe2", fg="white", command=lambda:repas1.participerBis(root, bar, bar_var, nb_participants_var, canvas, origin_x, origin_y, radius))
but_participer.grid(row=2, column=3, padx=50, pady=30, sticky=E)


entree_bar.grid(row=1, column=0)
label_nb_entree = Label(frame_des_progressbar,font=("italic", 14), textvariable=entree_var, bg="#efeded")
label_nb_entree.grid(row=0, column = 0)

plat_bar.grid(row=1, column=1)
label_nb_plat = Label(frame_des_progressbar,font=("italic", 14), textvariable=plat_var, bg="#efeded")
label_nb_plat.grid(row=0, column = 1)


dessert_bar.grid(row=1, column=2)
label_nb_dessert = Label(frame_des_progressbar,font=("italic", 14), textvariable=dessert_var, bg="#efeded")
label_nb_dessert.grid(row=0, column = 2)


boisson_bar.grid(row=1, column=3)
label_nb_boisson = Label(frame_des_progressbar,font=("italic", 14), textvariable=boisson_var, bg="#efeded")
label_nb_boisson.grid(row=0, column = 3)




entree_label = Label(frame_des_progressbar, text="entrée", width= 20,bg="#efeded")
entree_label.grid(row=2, column=0)

plat_label = Label(frame_des_progressbar, text="plat", width= 20,bg="#efeded")
plat_label.grid(row=2, column=1)

dessert_label = Label(frame_des_progressbar, text="dessert", width= 20,bg="#efeded")
dessert_label.grid(row=2, column=2)

boisson_label = Label(frame_des_progressbar, text="boisson", width= 20,bg="#efeded")
boisson_label.grid(row=2, column=3)

but_participant = Button(root, text="Liste des Participants",cursor="hand2", bg="#29abe2", font=("italic", 14), fg="white", command=lambda:repas1.voir_les_participants(root, bar, bar_var,nb_participants_var, canvas, origin_x, origin_y, radius))
but_participant.grid(row=1, column=3)






root.mainloop()

# //le nombre de personne a la fete
# //le maximum
# //la date