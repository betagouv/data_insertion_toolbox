
Ce dossier contient un script pour regrouper les fichiers du CD93 en fichier XML. Les dossiers de fichiers au format `MSABEM_M_dd.RCV` où `dd` correspond à `01`, `02`, `03`, etc. sont regroupés dans le fichier `MSABEM_M.xml`.

> Si le fichier `MSABEM_M.xml` existe déjà, un suffixe (de la forme `2021-08-04_10-38-34`) est ajouté au nom du fichier pour éviter de remplacer le ficheir existant.


## Lancement

```bash
python main.py [Chemin vers le dossier contenant les fichiers RCV à regrouper]
```
