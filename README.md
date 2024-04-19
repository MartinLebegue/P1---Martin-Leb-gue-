# Books to Scrap - Beta Scraper 

Ce script en version bêta est un système de surveillance des prix limité à un seul revendeur. Ce script permet d'extraire l'ensemble du site [Books To Scrap ](https://books.toscrape.com/) et de trier les données ainsi que les images. Il permet de ce fait, une surveillance complète sur commande. 

## Fonctionnalités
Extraction rapide et efficace des données.
Sauvegarde organisée des données et des images par catégorie.
Facilité d'extension pour inclure d'autres sources ou revendeurs.

## Prérequis
Assurez-vous d'avoir installé Python sur votre système. Ce projet a été testé avec Python 3.11.0, mais devrait être compatible avec d'autres versions de Python 3.

###  Configuration et Création de l'Environnement Virtuel
Pour exécuter ce projet, il est recommandé d'utiliser un environnement virtuel. Cela permet de gérer séparément les dépendances du projet et d'éviter tout conflit avec d'autres projets.
Ouvrez un terminal ou une invite de commande et naviguez jusqu'au répertoire de votre projet. Exécutez ensuite la commande suivante pour créer un environnement virtuel :

`python -m venv env`

env est le nom de l'environnement virtuel, mais vous pouvez le nommer comme vous le souhaitez.

### Activation de l'Environnement Virtuel
Pour activer l'environnement virtuel, utilisez l'une des commandes suivantes, en fonction de votre système d'exploitation.

Sur Windows :

`env\Scripts\activate`

Sur macOS et Linux :

`source env/bin/activate`

Vous saurez que l'environnement virtuel est activé car son nom apparaîtra entre parenthèses au début de la ligne dans votre terminal.

### Installation des Dépendances
Avec l'environnement virtuel activé, installez les dépendances requises en exécutant :

`pip install -r /path/to/requirements.txt`

Assurez-vous que le fichier requirements.txt est présent dans le répertoire de votre projet et liste toutes les bibliothèques nécessaires.

### Exécution de l'Application
Pour exécuter l'application, utilisez la commande suivante dans le terminal avec l'environnement virtuel activé :

`python nom_du_script.py`

Remplacez nom_du_script.py par le nom réel de votre script Python.

###  Ce que Fait l'Application
Lorsque vous exécutez l'application, elle effectue les opérations suivantes :

***Création de Fichiers CSV :*** Pour chaque catégorie de livre traitée, l'application crée un fichier "Données" dans lequel il inscrit les fichiers CSV divisés selon les catégories du site. Ces fichiers contiennent des informations sur les livres de la catégorie respective, telles que le titre, le prix, etc.

***Organisation des Images :*** L'application télécharge également les images des couvertures des livres. Ces images sont sauvegardées dans un dossier nommé images, situé dans le dossier du code. À l'intérieur du dossier images, des sous-dossiers sont créés pour chaque catégorie de livre, permettant une organisation claire des images par catégorie.

## Structure des Fichiers
Vous devez impérativement changer le chemin d'accès du fichier_text comme ceci : 

`fichier_text = r"C:\Users\...\"`


Après l'exécution de l'application, vous trouverez une structure de fichiers et de dossiers semblable à celle-ci dans votre répertoire de projet :

```
├── env/                        # Dossier pour l'environnement virtuel
├── images/                     # Dossier contenant toutes les images téléchargées
│   ├── categorie_1/            # Sous-dossier pour les images de la catégorie 1
│   ├── categorie_2/            # Sous-dossier pour les images de la catégorie 2
│   └── ...                     # Autres sous-dossiers pour les images par catégorie
├── Données/                    # Dossier contenant tous les fichiers csv
│  ├──categorie_1.csv           # Fichier CSV pour la catégorie 1
│  ├──categorie_2.csv           # Fichier CSV pour la catégorie 2
│  └── ...                      # Autres fichiers CSV pour les autres catégories
```

Assurez-vous que le dossier de votre projet a suffisamment d'espace disponible pour stocker les images et les fichiers CSV générés.

## Erreurs Potentielles et Leur Résolution
Lors de la configuration et de l'exécution de l'application, vous pourriez rencontrer certaines erreurs. Voici une liste des erreurs courantes et des suggestions pour les résoudre :

### Dépendances Manquantes
***Erreur: pip install -r requirements.txt*** échoue ou des erreurs se produisent lors de l'installation des dépendances.

***Solution:*** essayer d'installer les dépendances une par une. 

`pip install requests`

`pip install Bs4`

### Erreurs de Connexion Lors du Téléchargement des Images
***Erreur:*** Des erreurs de type ***ConnectTimeoutError*** se produisent lors de l'essai de télécharger les images.

***Solution:*** Vérifiez votre connexion Internet. Si le problème persiste, augmentez le délai d'attente dans le script (par exemple, requests.get(url, timeout=20))

### Permissions 
***Erreur:*** Le script ne peut pas créer de fichiers ou de dossiers, générant des erreurs de type ***PermissionError***.

***Solution:*** Assurez-vous que vous avez les droits nécessaires pour écrire dans le dossier où vous exécutez le script




