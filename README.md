# Books Online - Système de surveillance des prix

## Description

Ce projet est un **scraper** qui permet de surveiller les prix des livres d'occasion sur le site _Books to Scrape_. Le script extrait des informations sur les livres, telles que le titre, le prix, la disponibilité, la description, et télécharge également les images associées. Les données sont sauvegardées dans des fichiers CSV et les images sont stockées localement.

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
git clone https://github.com/votre_nom_utilisateur/nom_du_projet.git
cd nom_du_projet
```

## Utilisation

### Extraire les données

```bash
python script.py
```

## Structure du projet

├── env/ # Environnement virtuel (exclu du repository)
├── images/ # Dossier où les images sont téléchargées
├── csv_files/ # Dossier où les csv sont enregistrés
├── requirements.txt # Liste des dépendances du projet
├── script.py # Script Python principal
├── README.md # Ce fichier
└── .gitignore # Fichier pour exclure certains fichiers du contrôle de version
