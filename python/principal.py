
from lxml import etree
import folium 
import serial 
import time 
import tkinter as tk
from selenium import webdriver
import os
import sys
import threading
import datetime

#import fichier
#------------------------------------------------
from Replace0 import Renplacement 



#from TestIHM import InterfaceIHM
from UI import nom_Du_Fichier
from UI import listPorts
#error

#------------------------------------------------


#variable glob qui sert a faire la vérif dans le tring 
verif = [True]

def ReceptionsGPS():
    #variable de la gestions des erreur 
    global Error
    CurrentTime = ""

    ValeurPortCom =  listPorts()
    #print("la valeur du port com et :" , ValeurPortCom)
    
    #le a et la pour dire qu"on rajoute au fur et a mesure 
    try:
        with open("Body.txt" , "a") as Body:  
            with serial.Serial(ValeurPortCom , 9600,) as ser:
                line = ser.readline()
                line =str(line)
                
                

                  
                
                #division de la string
                LineSplitedGPS  = str(line).split(",")
                #récupération de la latitude

                if not LineSplitedGPS[0].startswith("b'+RCV=0"):
                    raise Exception("erreur de format ")


                lat = LineSplitedGPS[2] 
                if len(lat) < 7 :
                    lat = "0.0000000"
                    print("ici il y a un probléme")
                #recupération de le longitude
                long = LineSplitedGPS[3]
                if len(long) < 7 :
                    lat = "0.0000000"
                    print("ici il y a un probléme")
                print(lat)
                
            #creations de la ligne XML (ouverture de la balise)
            Ligne3 = "<wpt lat=\" " + lat + "\"" + " lon=\" " + long +"\">\n"            
            Ligne3 = Ligne3.replace(',', '')            
            CurrentTime = datetime.datetime.now()
            #ajout de la fontions date time de pyton
            Ligne4 = "<time>" + str(CurrentTime) + "</time>\n"
            #fermeture de la balise 
            Ligne5 = "</wpt>\n"
            StrLigne3 = str(Ligne3)
            #concatéations des ligne pour en avoir une viabl 
            BodyComplet = StrLigne3 + Ligne4 + Ligne5
            #print(BodyComplet)
            #ecriture des informations dans un fichiée
            Body.write(BodyComplet)
            
        return ''
    #si une erreur bloquant et detectée   
    except:
        with open("Body.txt" , "a") as Body:      
            lat = "  0.0000000"
            long = "  0.0000000"
            Ligne3 = "<wpt lat=\" " + lat + "\"" + " lon=\" " + long +"\">\n"            
            
            Ligne3 = Ligne3.replace(',', '')            
            CurrentTime = datetime.datetime.now()
            #ajout de la fontions date time de pyton 
            Ligne4 = "<time>" + str(CurrentTime) + "</time>\n"
            Ligne5 = "</wpt>\n"
            
            StrLigne3 = str(Ligne3)
            #concatéations des ligne pour en avoir une viabl 
            BodyComplet = StrLigne3 + Ligne4 + Ligne5
            
            Body.write(BodyComplet)
    
        #le module a pour le fichier Body veut dire 
        #ecriture avec ajout en fin de fichier 
    
        return ' '

def ListPoint(parsed_GPX):
    
    ns = "http://www.topografix.com/GPX/1/1"
    #-------------------------------------------------
    #set des list lat long et temp 
    #-------------------------------------------------
    #liste des latitude exprimée en degrées 
    latitude = []
    #liste des longitude exprimée en degré
    longitude = []
    #rec,fuperations du temps dansune list 
    Result = []
    
    temps = []
    #conteur lat v permetre de garder les positions lat stockée 
    #celas va servir a la gesions des erreur 
    try:
        #ceci et dans la fontions ListPoint
        #on parcour le fichier GPX parser 
        for point in parsed_GPX :
            #on récupére les point en lat et en long 
            latitude = float(point.get("lat"))
            longitude = float(point.get("lon"))
            #concaténations des donnée dans un tableaux
            Result.append([latitude , longitude])            
        return Result   
    except:
        i = 2
        for point in parsed_GPX :
             
            latitude = "   0.0000000"
            longitude = "   0.0000000"
            
            Result.append([latitude , longitude])
            
                
            for enfant in point.getchildren():
                if enfant.tag == "{" + ns + "}time":
                    temps.append((str(enfant.text)))
        
        i += 1 
        return Result 
    
def RemiseAZeroBody():
    open("Body.txt","w").close()

def ConcatenationsDeFichier():
    
    #créations d'un fichier cataliseur de Head Body et Feet
    #with open("C:/Users/USER\Documents\info\Memoire\Part2\GPS_part\Code_Pyhton_Creations_Carte\mind.gpx" , "w") as Mind:
    
    #os.chdir(nom_Du_Fichier)
    #ouverture / remplacement du fichier GPX
    with open("{}.gpx".format(nom_Du_Fichier) , "w") as Mind:
        #pour line qui parcour le conteue du human 
        for line in Human :
            #on copie le contenue de Human
            with open(str(line)) as infile:  
                #on colle le contenue dans le GPX
                Mind.write(infile.read())
                
#tkinter qui va permettre de terminée le traceur 
#partie bouton ON OFF retou
def RadBut():
    #permet de partager la variable verif avec le tread 
    global verif
    app = tk.Tk() 
    app.geometry("200x200")
    def Stop():
        #insert sert a remplacer le contenue d'une liste 
        verif.insert(0,False)
        driver.quit()
        app.destroy()
    def Start():
        verif.insert(1,True)

     
    #definitions dans tkinter du typer de la variable (ici un int)
    #il sert de refre
    
    radioValue = tk.IntVar() 
    #set de la valeur de base de radioValue
    radioValue.set("1")
    rdioOne = tk.Radiobutton(app, text='ON',
                                 variable=radioValue, command=Start
                                 , value=1) 
    rdioTwo = tk.Radiobutton(app, text='OFF',
                                 variable=radioValue,command=Stop,
                                 value=0) 
    
    #sert a récuperer le contenue de la variable radioValue
        
    rdioOne.pack()
    rdioTwo.pack()
    app.mainloop()

def CreationsHTML():  
    """
    Color_Error = "blue"

    
    print("ets de l'erreur :", Error )
    if  Error == False:
        Color_Error = 'green'
    if Error == True:
        Color_Error = 'red'
    """
    #parsing du fichier GPX 
    root = etree.parse("{}.gpx".format(nom_Du_Fichier))
    #format normalisée des fichiez gpx 
    ns = "http://www.topografix.com/GPX/1/1"
    #definitions de la hiérarchie des balise du fichier via xpath 
    parsedGPX = root.xpath("/ns:gpx/ns:wpt", namespaces={"ns": ns})
    #appelle de la fontions ListPoint() qui va parcourir le fichier 
    ListeP = ListPoint(parsedGPX)
   

    point = ListeP[-1]

    #paramétre du type de carte + le zoom de debart
    fmap = folium.Map(location=point, tiles="Stamen Toner",
                      zoom_start=20)
    folium.TileLayer('OpenStreetMap').add_to(fmap) 
    folium.TileLayer('Stamen Watercolor').add_to(fmap)
    #patramétre de la pin d'informations 
    
    folium.LayerControl().add_to(fmap)
    folium.Marker(point, popup= point, icon=folium.Icon(color= 'green')).add_to(fmap)
    #paramétre de la connexions entre les point 
    
    folium.PolyLine(ListeP, color="blue" , weight=3, opacity=1).add_to(fmap)
    
    #sauvegarde du fichiée 
    fmap.save(nom_Du_Fichier + ".html")
    

###################################################### 
#apele des fontions 
#le fihier classe a la prioritée sur les autre 
#les fichier vont donc se faite
with open("Head.txt" , "w") as Head:
    #créations du head
    ContenueHead = "<gpx xmlns=\"http://www.topografix.com/GPX/1/1\" version=\"1.1\">\n"
    Head.write(ContenueHead)
    TotalHead = Head.readlines

with open("Feet.txt", "w") as Feet:
    #creations du feet
    ContenueFeet = "</gpx>"
    Feet.write(ContenueFeet)
    TotalFeet = Feet.readlines

######################################################   
#créations de human qui va comportée les 3 fichier composant le GPX 
Human = ['Head.txt' , 'Body.txt', 'Feet.txt']

#os.remove("C:/Users/USER/Documents/info/Memoire/Part2/GPS_part/CarteWeb/carte7.html")

#on ecrit dans body la valeur du gps 
ReceptionsGPS()
time.sleep(1)
#on assemble les fichiez 
ConcatenationsDeFichier()
time.sleep(1)
CreationsHTML()
os.remove("Body.txt")
#firefox et définie comme navigateur utilisée pour ouvrir l'html
driver = webdriver.Firefox()
#chemin vers l'html 
patWay = "file:///C:/Users/USER/Documents/info/Memoire/Part2/GPS_part/V1.1/" +  nom_Du_Fichier + "/" + nom_Du_Fichier + ".html"
#affichage de l'html dans firefox
driver.get(patWay)
#set des  
TotalDePositions = 0
#apelle de la fontions via un thread 
j = threading.Thread(target=RadBut)
#lancmeent de la fontions 
j.start()

while(verif[0]):
    #on ecrit dans body la valeur du gps 
    ReceptionsGPS()
    time.sleep(1)
    #on assemble les fichiez 
    ConcatenationsDeFichier()
    
    Renplacement()
    
    #on récupére le fichies précédamant crée 
    CreationsHTML()
    driver.refresh()
    TotalDePositions = TotalDePositions + 1
    #print(TotalDePositions)
    if(verif == False):
        break
        sys.exit()