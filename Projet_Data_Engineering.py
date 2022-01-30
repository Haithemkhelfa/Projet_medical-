import pandas as pd
import numpy as np 
import json 
from json import JSONEncoder
import re

###Path ####
pubmed = "pubmed.csv"

drugs = "drugs.csv"

clinical_trials= "clinical_trials.csv"

pubmed_json = "pubmed.json"

############ Cleaning data_clinical_trials ##########################

#### lire le fichier  clinical_trials format .csv "

df_clinical_trials= pd.read_csv(clinical_trials)
print(df_clinical_trials)

#########
missing_text = df_clinical_trials.isnull()

print(missing_text)

#Faire fusioner les deux lignes suivantes  

print(df_clinical_trials.loc[[5, 6],:])

print(df_clinical_trials.dtypes)

# groupby combination and aggregate lines 
df_clinical_trials = df_clinical_trials.groupby(['scientific_title','date']).agg(lambda x: x.dropna(axis=0)).reset_index().set_index('id')
print(df_clinical_trials)

# Changer data types : la colonne "date"  >> datetime

df_clinical_trials = df_clinical_trials.astype({
    'scientific_title': 'str',
    'date' : 'datetime64',
    'journal' : 'str'
})

print(df_clinical_trials.dtypes)

# data_ drug : Les noms de drugs (des médicaments) avec un id (atccode) et un nom (drug)
##### lire le fichier drugs format .csv
df_drugs= pd.read_csv(drugs, sep=",",  encoding="utf-8")
print(df_drugs)

#############Cleaning data_pubmed json & csv ###########################

# lecture pubmed .csv
df_pubmed_csv= pd.read_csv(pubmed, sep=",",  encoding="utf-8")
print(df_pubmed_csv)

# Changer data types : la colonne "date"  >> datetime

df_pubmed_csv = df_pubmed_csv.astype({'title': 'str','date' : 'datetime64', 'journal' : 'str'})

print(df_pubmed_csv.dtypes)

# lecture pubmed .json la suite de fichier pubmed .json

df_pubmed_json = pd.read_json(pubmed_json)
print(df_pubmed_json)

# Changer data types : la colonne "date" >> datetime

df_pubmed_json = df_pubmed_json.astype({'title': 'str', 'date' : 'datetime64','journal' : 'str'}) 

print(df_pubmed_json.dtypes)

# concatenation 2 dataframes 
df_pubmed = pd.concat([df_pubmed_csv, df_pubmed_json], axis=0, ignore_index=True)
print(df_pubmed)
 
########################## Création des class ##########################

class DrugEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
    
class Drug():
    def __init__(self, atccode, drug):
        self.atccode = atccode
        self.drug = drug
        self.pubmed = []
        self.clinical_trials=[]

        
        #############################
    def add_pubmed(self,x):
        self.pubmed.append(x)
        
        ############################
        
        #############################
    def add_clinical_trials(self,x):
        self.clinical_trials.append(x)
        
        ############################
        
 #############################################################################       
class ClinicalTrial():
    def __init__(self,NTC_id, scientific_title, date, journal):
        self.id = NTC_id
        self.scientific_title = scientific_title
        self.date_mention = date
        self.journal = journal
 #############################################################################       
class Pubmed():
    def __init__(self, pmd_id, title, date, journal):
        self.id = pmd_id
        self.title = title
        self.date_mention = date
        self.journal = journal
##############################################################################
        

# Créer des objets Drug => Appeler les classes Drug        
list_drugs = []
for indx in df_drugs.index:
    dr= Drug(str(df_drugs['atccode'][indx]), str(df_drugs['drug'][indx]))
    list_drugs.append(dr)
    
    
################################################################################
# créer autres objets nécessaires pour la update des objects Drug: ClinicalTrial

###############################################################################

for drug in list_drugs:
    
    #copier le dataframe df_clinical_trials
    
    df_ct = df_clinical_trials.reset_index()
    
    #"w+" : lecture et écriture, avec suppression du contenu au préalable
    #Donc cette re.subdéclaration signifie "s'il y a un ou plusieurs caractères non alphanumériques 
    #avec un caractère alphanumérique avant et après, remplacez le(s) caractère(s) non alphanumérique(s) 
    #par un espace".
    
    
    list_title =  df_ct['scientific_title'].map(lambda x: re.sub(r"\W+", " ", x).upper().split())
    
    drug_names_list =[]
    
    for s_title in list_title:
        drug_names_list.append(str(drug.drug) in s_title)
    
        
    # Ajouter une colonne "presence_Drug" indiquant s'il contient le drug  True or False   
    df_ct['presence_Drug'] =  drug_names_list


    
    ########## filter #########
    
    df_ct = df_ct[df_ct['presence_Drug']]
    
    print(df_ct)
    
    #-------------------------------------------------------------#
    
    # créer des objets clinical_trials à partir de dataframe df_ct
    
    for indx in df_ct.index:
        
        ct = ClinicalTrial(str(df_ct['id'][indx]), str(df_ct['scientific_title'][indx]),str(df_ct['date'][indx]),str(df_ct['journal'][indx]))
        drug.add_clinical_trials(ct)
        
        
      ###############################################################################
    
    #df_pmd, créer autres objets nécessaires pour la update des objects Drug: pubmed
    
         ###############################################################################  
    
    #copier le dataframe df_clinical_trials
    
    df_pmd = df_pubmed.reset_index()
    
    
    list_title =  df_pmd['title'].map(lambda x: re.sub(r"\W+", " ", x).upper().split())
    
    drug_names_list =[]
    
    for s_title in list_title:
        drug_names_list.append(str(drug.drug) in s_title)
    
        
    # Ajouter une colonne "presence_Drug" indiquant s'il contient le drug  True or False   
    df_pmd['presence_Drug'] =  drug_names_list


    
    ########## filter #########
    
    df_pmd = df_pmd[df_pmd['presence_Drug']]
    
    print(df_pmd)
    
    #-------------------------------------------------------------#
    
    # créer des objets clinical_trials à partir de dataframe df_ct
    
    for indx in df_pmd.index:
        
        p = Pubmed(str(df_pmd['id'][indx]), str(df_pmd['title'][indx]),str(df_pmd['date'][indx]),str(df_pmd['journal'][indx]))
        drug.add_pubmed(p)  
        
############################## Affichier le fichier data avant le save dans un fichier.json #########################
    
data = json.dumps(list_drugs,indent=4, cls=DrugEncoder)

print(data)

with open('data.json', 'w') as my_file:
    json.dump(list_drugs, my_file,indent=4, cls=DrugEncoder)





