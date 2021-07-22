Ce dossier contient un script pour faciliter le découpage de fichiers nationaux Pole emploi et la mise à disposition via Filr pour chaque département. C'est une expérimentatione pour automatiser les transferts.


# Instructions

Un fichier .env est nécessaire pour indiquer les informations de connexion à FILR. Un exemple est donné dans `.env.exemple`.


- Aller sur le portail partenaire
- Télécharger le fichier
- Renommer le fichier au format dates_PE_AAAMMJJ.csv avec AAAAMMJJ qui correspond au jour où le fichier a été mis à disposition
- Ouvrir un invité de commande en indiquant cmd dans le menu démarrer
- Aller dans le dossier contenant le script
- Lancer les commandes suivantes :
condabin\conda.bat activate base
python.exe process.py
- Après apparition de -->
- Glisser coller le nom du fichier à découper
- Faire entrée

Les fichiers par départements seront disponibles dans les dossiers dédiés.
