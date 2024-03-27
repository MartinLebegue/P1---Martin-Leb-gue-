
import requests 
from bs4 import BeautifulSoup 

#url = "https://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html"

#response = requests.get(url)

#if response.ok: 
    #soup = BeautifulSoup(response.text)
    #title = soup.find("title")
    #print(title.text)

url = "https://books.toscrape.com/catalogue/soumission_998/index.html"

fichier_text = r"C:\Users\33695\Desktop\Code\P1\infos_produits.txt"
fichier_text = 'infos_produits.txt'



def scrap_infos(url):
    response = requests.get(url)
    if response.status_code == 200:
        print("Réponse HTTP réussie.")
    else:
        print(f"Erreur HTTP : {response.status_code}")
        return {}
   
    soup = BeautifulSoup(response.content, "html.parser")

    titre = soup.find("h1").text
    print("Titre:", titre)

    div_description = soup.find("div", id="product_description")
    if div_description:
        # Trouver le paragraphe suivant le titre de la description
        p_description = div_description.find_next("p")
        if p_description:
            print("Description:", p_description.text)


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














