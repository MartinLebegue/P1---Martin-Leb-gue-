
import requests 
from bs4 import BeautifulSoup 

#url = "https://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html"

#response = requests.get(url)

#if response.ok: 
    #soup = BeautifulSoup(response.text)
    #title = soup.find("title")
    #print(title.text)

url = "https://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html"

fichier_text = 'infos_produits.txt'

def scrap_infos(url):
    response = requests.get(url)
    if response.status_code == 200:
        print("Réponse HTTP réussie.")
    else:
        print(f"Erreur HTTP : {response.status_code}")
        return {}
   
    soup = BeautifulSoup(response.content, "html.parser")

    tableau_produit = soup.find("table", class_="table table-striped")
    infos_produit = {}

    for row in tableau_produit.find_all("tr"):
        header = row.find("th").text
        value = row.find("td").text
        infos_produit[header] = value

    print("Informations extraites avec succès.")
    return infos_produit

infos_produit = scrap_infos(url)

print("Début de l'écriture dans le fichier...")
with open(fichier_text, "w") as file:
    for header, value in infos_produit.items():
        file.write(f"{header}: {value}\n")
print("Fin de l'écriture dans le fichier.")














