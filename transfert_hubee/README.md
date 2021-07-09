Ce dossier contient des scripts pour faciliter les échanges de données via HubEE. Ce sont des expérimentations à partir desquelles nous pouvons automatiser les transferts.


# Préparations

## Dépendances

Il faut installer les dépendances à partir de la commande suivante :

```bash
pip install -r requirements.txt`
```

## Configuration

Un fichier `.env` doit être créé dans ce dossier avec un contenu similaire au fichier `exemple.env`. Le contenu de ce fichier devrait vous être communiqué par l'équipe data.insertion.


# Envoi

```bash
python envoi.py -- xxx yyy [nom du fichier]
```

où (xxx, yyy) représente (company_register, branch_code) du destinataire du fichier.
En cas d'absence de fichier, un fichier texte avec l'heure de création du fichier est envoyé.


# Réception

```bash
python reception.py -- xxx
```

où xxx représente company_register de l'émetteur du fichier.

À la réception, l'archive est décompressée, son contenu déchiffré puis mis à disposition dans un sous-dossier.
