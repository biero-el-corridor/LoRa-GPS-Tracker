from UI import nom_Du_Fichier

class Replace():
    #instantiations des constructeur
    def __init__(self,Num, zero_string , count, ligne ):
        self.Num = Num
        self.zero_string  = zero_string 
        self.count = count
        self.ligne = ligne
        
    def LLat(self, Llat):
        self.Llat = Llat
        #si la lat et égal a 0 
        if self.ligne[self.Num] == self.zero_string :
            #remplacement des 0 par l'encienne valeur 
            self.ligne[self.Num] = self.Llat[self.count - 1 ]            
        #retour de la valeur sous forme de string
        return str(self.ligne[self.Num])
    
    def LLong(self,Llong):
        self.Llong = Llong
        if self.ligne[self.Num] == self.zero_string :
            self.ligne[self.Num] = self.Llong[self.count - 1 ]
        return str(self.ligne[self.Num])
        return str(self.ligne[self.Num])



def Renplacement():
    
    with open("{}.gpx".format(nom_Du_Fichier), "r") as erreur:
        lignes  = erreur.readlines()
        count = 0 
        Llat = []
        Llong = []
    
        without_erro = ""
        #parcour du fichier 
        for ligne in lignes:
            #si la ligne commence par <wpt lat
            if ligne.startswith("<w"):    
                try: 
                    #divisions de la ligne en champ
                    ligne = ligne.split()   
                    #si le 2ée champ de la ligne contien des 0
                    #on le remplace par la derniére valeur viable 
                    replaceLat =  Replace(2,"0.0000000\"", count,  ligne)
                    replaceLong =  Replace(4,"0.0000000\">", count, ligne)                    
                    replaceLat = replaceLat.LLat(Llat)
                    replaceLong = replaceLong.LLong(Llong)
                    #creations de la nouvelle ligne 
                    noError = "<wpt lat=\"" + replaceLat + " lon=\"" + replaceLong + "\n" 
                    #la ligne corrigée 
                    without_erro += f"{noError}"
                    #
                    Llat.append(ligne[2])
                    Llong.append(ligne[4])  
                    count += 1
                except:
                    #transpositions de la tab en string
                    ligne = " ".join(ligne)  
                    
                    without_erro += f"{ligne}\n" 
            else:
                #si la phrase ne comence pas pas <wpt
                without_erro += f"{ligne}" 
                
    #ouverture du fichier GPX 
    with open("{}.gpx".format(nom_Du_Fichier), "w") as erreur:
        #Remplacement des encienne donnée par les nouvelle 
        erreur.write(without_erro)
             
