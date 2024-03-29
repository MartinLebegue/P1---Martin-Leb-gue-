
import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin
#url = "https://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html"

#response = requests.get(url)

#if response.ok:
    #soup = BeautifulSoup(response.text)
    #title = soup.find("title")
    #print(title.text)


fichier_text = r"C:\Users\33695\Desktop\Code\P1\infos_produits.txt"
fichier_text = 'infos_produits.txt'

def scrap_infos(book_url):

    infos_produit = {}

    response = requests.get(book_url)
    if response.status_code == 200:
        print("Réponse HTTP réussie.")
    else:
        print(f"Erreur HTTP : {response.status_code}")
        return {}

    infos_produit["Porduct Page URL"] = book_url

    soup = BeautifulSoup(response.content, "html.parser")

    # Trouver la balise <ul> avec la classe 'breadcrumb'
    breadcrumb = soup.find('ul', class_='breadcrumb')
    # Trouver toutes les balises <a> dans le breadcrumb
    links = breadcrumb.find_all('a')
    if links:
        category_link = links[-1]  # Avant-dernier lien
        category_name = category_link.text.strip()
    infos_produit["Catégorie"] = category_name

    #Trouver le titre via le selecteur h1 et l'ajouter au dictionnaire
    titre = soup.find("h1").text
    print("Titre ajouté au fichier texte.")
    infos_produit["Title"] = titre #Ajout au dictionnaire

    #Trouver la description via l'id "product_description" et en déduire le "p" et l'écrire dans le dic
    div_description = soup.find("div", id="product_description")
    if div_description:
        # Trouver le paragraphe suivant le titre de la description
        p_description = div_description.find_next("p")
        if p_description:
            print("Description ajoutée au fichier texte.")
            infos_produit["Product Description"] = p_description.text

    # Trouver la balise <p> qui contient la classe 'star-rating'
    star_rating_element = soup.find("p", class_="star-rating")

    # Extraire le niveau de la note à partir de la classe
    if star_rating_element:

        # Les classes seront quelque chose comme 'star-rating Three'
        star_rating_classes = star_rating_element.get('class')  # ['star-rating', 'Three']

        # La classe de notation (par exemple, 'Three') est le deuxième élément de la liste
        star_rating = star_rating_classes[1] if len(star_rating_classes) > 1 else None

        # Convertir le texte de la note en nombre (par exemple 'Three' devient 3)
        ratings = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
        star_rating_number = ratings.get(star_rating, 0)
        print(f"Review out of 5 : {star_rating_number}")

        #Inscrire la review dans le fichier texte
        infos_produit["Review out of 5"] = star_rating_number

    #Trouver les valeurs dans le tableau descriptif

    tableau_produit = soup.find("table", class_="table table-striped")

    for row in tableau_produit.find_all("tr"):
        header = row.find("th").text
        value = row.find("td").text
        infos_produit[header] = value

    print("Informations extraites avec succès.")

    return infos_produit

def scrape_category_page(category_url):
    response = requests.get(category_url)
    soup = BeautifulSoup(response.content, "html.parser")
    books_info = []

    # Supposons que chaque livre soit dans un élément <article class="product_pod">.
    # Modifier le sélecteur si nécessaire.
    books = soup.find_all('article', class_='product_pod')
    for book in books:
        # Supposons que le lien du livre soit dans un élément <h3> à l'intérieur de <article>.
        # Modifier le sélecteur si nécessaire.
        book_link = book.find('h3').find('a')['href']
        full_book_link = urljoin(category_url, book_link)
        book_info = scrap_infos(full_book_link)
        books_info.append(book_info)

    return books_info

# URL de la première page de la catégorie 'Fiction'
category_url = 'https://books.toscrape.com/catalogue/category/books/fiction_10/index.html'

# Scraping de la première page de la catégorie
books_info = scrape_category_page(category_url)


fichier_csv = "infos_produit.csv"


# Écriture dans un fichier CSV
fichier_csv = "infos_produits.csv"
with open(fichier_csv, mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=books_info[0].keys())
    writer.writeheader()
    for book_info in books_info:
        writer.writerow(book_info)

print(f"Les informations du produit ont été écrites dans {fichier_csv}")














