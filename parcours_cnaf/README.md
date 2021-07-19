Ce dossier contient des scripts pour faciliter l'analyse en masse des fichiers envoyés par la CNAF.

# Préparations

## Dépendances

Il faut installer les dépendances à partir de la commande suivante :

```bash
pip install -r requirements.txt`
```

## Lancement

```bash
python main.py [Chemin vers le dossier contenant les XML (gzip ou non)]
```

## Compréhension des performances

Pour nous aider à mieux comprendre les performances des scripts dans votre environnement, vous pouvez lancer une autre commande qui fait le même traitement mais qui, en plus, enregistre les performances du script :

```bash
python -m cProfile -o cnaf.prof main.py [Chemin vers le dossier contenant les XML (gzip ou non)]
```

`cnaf.prof` est le nom d'un fichier (que vous pouvez modifier) à nous envoyer pour nous permettre d'identifier ce qui est lent et ce qui rapide et réfléchir aux améliorations possibles.
