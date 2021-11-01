#test de créations d'une ihm
#les proéocupations principales sont 
#un nomage des fichier 
#oectif 1 crée un fichier a partir d"un nom 
#donnée dans un champ tkinter 
#faire a tenions a bien gérer les mainloop 

import tkinter as tk
import os 
import subprocess
import serial.tools.list_ports
nom_Du_Fichier = ""

class InterfaceIHM:
###############################################################
    def __init__(self):
        #intance de la fenétre principales 
        self.IHM = tk.Tk()
        #définir la taille de la fenêtre
        self.IHM.geometry("400x300")
############################################################### 
       
#fontions de fin de loop 
###############################################################    
    def Terminate(self):
        #apelle du main loop pour finir la boucle tkinter 
        self.IHM.mainloop() 
        
#menu reoulant du choix du port COM 
###############################################################
    def MenuDéroulantPortCom(self):
        #set de la variable port qui va lister tout les port com actif 
        
        #tentative de lister les port dans un teblaux 
        self.listPort = listPorts()
        #créations de la liste 
        self.list = [self.listPort]
        #dire que la variable varible aura a mémorisée une chaine de caractére 
        self.variable = tk.StringVar(self.IHM)
        #la varible va affichée le contenue de la positions 0 de la liste 
        self.variable.set(self.list[0])
        #set du menu déroulant 
        self.opt = tk.OptionMenu(self.IHM, self.variable , self.list)
        self.opt.pack()


#menu déroulat du chois de a couleur de la carte 
###############################################################
#pour rapelle il y a Mapbox , Stamen Terrain , Stamen Toner , OpenStreetMap , cartodbpositron

###############################################################

#fontions de la 1étre zone de saisie 
###############################################################        
    def ZoneDeText(self):
        #créations de la variable qui va contenir les info
        self.saisir=tk.StringVar()
        #set du text en null 
        self.saisir.set("")
        #placement dans lespace de la zone 
        self.saisir=tk.Entry(textvariable=self.saisir, width=7)
        self.saisir.pack()
        
        
###############################################################

    def Register(self):
        global Test 
        global nom_Du_Fichier
        self.contenue = self.saisir.get()
        os.mkdir(self.contenue)
        Test = False 
        nom_Du_Fichier = self.contenue
        self.IHM.destroy()
###############################################################
    def Quit(self):
        self.IHM.destroy()
        
###############################################################
    
    def BouttonQuit(self,  Text):
            self.text1 = Text 
            #intance du BouttonRegister 
            self.widget = tk.Button(None)
            #definitions de son text et de son utilitée 
            self.widget.config(text=self.text1, command=self.Quit) 
            #affichage du BouttonRegister (expand oui ou non  , remplisage )
            self.widget.pack(expand=tk.NO, fill=tk.Y)



#fontions du boutton quitter 
############################################################### 
    def BouttonRegister(self,  Text):
        self.text1 = Text 
        #intance du BouttonRegister 
        self.widget = tk.Button(None)
        #definitions de son text et de son utilitée 
        self.widget.config(text=self.text1, command=self.Register) 
        #affichage du BouttonRegister (expand oui ou non  , remplisage )
        self.widget.pack(expand=tk.NO, fill=tk.Y)
        
############################################################### 

#def du label (réutilisable)
###############################################################      
    def Label(self , Text):
        self.text = Text
        #zone_texte = tkinter.Label (text = "zone de texte")
        self.label1 = tk.Label (text=self.text)
        self.label1.pack()
###############################################################



def listPorts():
    #1er test avec le try except et sa a l'air pas mal 
    try:
        #liste des port COM (nom , numéro, systéme atachée au port)
        ports = list( serial.tools.list_ports.comports())
        for port in ports:           
            #va permetre de lister les numéro des port COM up
            #print(port)
            print(port.device)
            
        return port.device
    
    #gestions de l'erreur de l'absence de port com 
    except:
        #ouai l'anglais c'est stylée 
        IHM.Label("no COM port detected Please reload")
        IHM.BouttonQuit("Quitter")
        IHM.Terminate()
        print("erreur no port Com detected")

#l'ordre et important il ne faut pas oubliée 
#apele des fontions 
label1 = "Interface de test "
IHM = InterfaceIHM()
IHM.MenuDéroulantPortCom()
IHM.Label("choisir le port COM")
IHM.Label("Nom du dossier")
IHM.ZoneDeText()
#IHM.BouttonTest("crrée le dossiée")
IHM.BouttonRegister("lancer le traceur")
IHM.Terminate()

#test de créations de document dans le dissée fraichement crée 
print(nom_Du_Fichier)
Fichier = nom_Du_Fichier+".txt"
os.chdir(nom_Du_Fichier)
with open( Fichier , "w") as d :
    d.write("hello")

#retour en ariée pour pouvoir gérer les sous dossiée 
subprocess.call('cd ..', shell=True)
