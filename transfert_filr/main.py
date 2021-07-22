from dotenv import load_dotenv

import csv
import os
import pandas as pd
import requests
from pprint import pprint

load_dotenv()
FILR_HOST = os.getenv('FILR_HOST')
FILR_USERNAME = os.getenv('FILR_USERNAME')
FILR_PASSWORD = os.getenv('FILR_PASSWORD')

dossiers_cibles = {
    '06': 'alpes maritimes',
    '13': 'bouche du rhone',
    '22': 'cote darmor',
    '29': 'finistere',
    '35': 'ile et vialaine',
    '53': 'mayenne',
    '56': 'morbihan',
    '67': 'Alsace',
    '68': 'Alsace',
    '83': 'var'
}


def get_folder(folders, name, check=True):
    matches = [item for item in folders['items'] if item['title'] == name]

    if check:
        assert len(matches) == 1, name + " non trouve"
    return matches[0] if len(matches) else None


def main():
    print('Quel fichier doit etre decoupe ?')
    file = input('--> ').replace('"', "")
    print(file)

    print('Recuperation des dossiers.')
    folders = requests.get(FILR_HOST + '/rest/folders', auth=(FILR_USERNAME, FILR_PASSWORD)).json()
    for (code) in dossiers_cibles:
        folder = get_folder(folders, dossiers_cibles[code], check=False)
        if folder:
          pprint((code, folder['id']))
        else:
          pprint((code, folder))

    df = pd.read_csv(file, sep=";", dtype=str)
    name, _ = os.path.splitext(file)
    l = []
    for k, gr in df.groupby('departement'):
        print(k)
        filename = name + '_' + k + '_out.csv'
        l.append(filename)
        gr.to_csv(filename, index=False, quoting=csv.QUOTE_NONNUMERIC, sep=";")

        base_name = os.path.basename(filename)

        if k not in dossiers_cibles:
            print("Le departement {} n'a pas de dossier sur filr. Mise a dispo impossible.".format(k))
            continue

        dest_folder = get_folder(folders, dossiers_cibles[k], check=False)
        if not dest_folder:
            print("{} non trouve. Mise a dispo impossible".format(dossiers_cibles[k]))
            continue
        else:
            print('Dossier trouve, le fichier sera mis a dispo {}'.format(base_name))

        with open(filename, 'rb') as f:
            data = f.read()
            res = requests.post(FILR_HOST + '/rest/folders/' + str(dest_folder['id']) + '/library_files?file_name=' + base_name,
              data=data, headers={'Content-Type': 'application/octet-stream'}, auth=(FILR_USERNAME, FILR_PASSWORD)).json()
            pprint("OK")


if __name__ == '__main__':
    main()
