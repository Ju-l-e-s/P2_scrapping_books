# Books Online - Système de surveillance des prix

## Description

Ce projet est un **scraper** qui permet de surveiller les prix des livres d'occasion sur le site [_Books to Scrape_](http://books.toscrape.com/). Le script extrait des informations sur les livres, telles que le titre, le prix, la disponibilité, la description, et télécharge également les images associées. Les données sont sauvegardées dans des fichiers CSV et les images sont stockées localement.

Le projet est divisé en plusieurs phases :

1. Extraction des informations d'un livre spécifique.
2. Extraction des informations pour tous les livres d'une catégorie.
3. Extraction des informations pour tous les livres de toutes les catégories.
4. Téléchargement des images de chaque livre.

## Fonctionnalités

- Récupération des données suivantes pour chaque livre :
  - URL de la page produit
  - Code produit universel (UPC)
  - Titre
  - Prix TTC et HT
  - Quantité disponible
  - Description du produit
  - Catégorie
  - Note de l'évaluation
  - URL de l'image
- Export des données dans des fichiers CSV.
- Téléchargement des images des livres.

## Prérequis

Assurez-vous d'avoir Python 3 installé sur votre machine. Vous pouvez télécharger Python [ici](https://www.python.org/downloads/).

## Installation

### 1. Cloner le repository

Clonez le repository GitHub sur votre machine locale :

```bash
git clone https://github.com/Ju-l-e-s/P2_scrapping_books.git
cd P2_scrapping_books
```

## Utilisation

### Extraire les données

```bash
python script.py
```

## Structure du projet

```
├── categories/             # Dossier principal contenant toutes les catégories
│   ├── Catégorie1/         # Dossier de la première catégorie
│   │   ├── data.csv        # Données des livres de la catégorie au format CSV
│   │   └── photos/         # Dossier contenant les images des livres
│   │       ├── livre1.jpg
│   │       ├── livre2.jpg
│   │       └── ...
│   ├── Catégorie2/
│   │   ├── data.csv
│   │   └── photos/
│   │       ├── livre1.jpg
│   │       ├── livre2.jpg
│   │       └── ...
│   └── ...                 # Autres catégories
├── main.py                 # Script Python principal
├── categories.py           # Module pour gérer les catégories
├── book_details.py         # Module pour extraire les détails des livres
├── data_saving.py          # Module pour sauvegarder les données
├── image_downloader.py     # Module pour télécharger les images
├── utils.py                # Fonctions utilitaires
├── requirements.txt        # Liste des dépendances du projet
└── README.md               # Fichier README avec les informations du projet
```

## Notes

- **Organisation des données** : Les données et les images sont structurées par catégorie pour faciliter la navigation et l’analyse.
- **Connexion Internet** : Assurez-vous d’avoir une connexion Internet stable lors de l’exécution du script, car il effectue de nombreuses requêtes réseau.
- **Site cible** : [_Books to Scrape_](http://books.toscrape.com/) est un site de démonstration conçu spécifiquement pour le web scraping.
