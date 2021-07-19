import datetime
import glob
import gzip
import pandas as pd
import os
import sys
from tqdm import tqdm
import xml.etree.ElementTree as ET


def ilen(iterable):
    return sum(1 for _ in iterable)


def get_meta(meta, item):
  try:
    return list(meta.iter(item))[0].text
  except IndexError:
    return 'Error'


def main():
  root_path = sys.argv[len(sys.argv)-1]
  matches = glob.glob("{}{}**{}*.xml*".format(root_path, os.sep, os.sep), recursive=True)
  ts = datetime.datetime.now()

  data = {
    "path": [],
    "size": [],
    "analysis": [],
    "date": [],
    "nature": [],
    "frequence": [],
    "dossier": [],
    "personne": [],
  }
  for m in tqdm(matches):
    start = datetime.datetime.now()
    data['path'].append(os.path.relpath(m, root_path))
    data['size'].append(os.path.getsize(m))
    if m.endswith('gz'):
      gz_input = gzip.open(m, 'r')
      tree = ET.parse(gz_input)
    else:
      tree = ET.parse(m)
    dom = tree.getroot()

    mmeta = list(dom.iter('IdentificationFlux'))
    fdate, fnature, ffrequence = ("#NA", "#NA", "#NA")
    if len(mmeta):
      meta = mmeta[0]
      fdate = get_meta(meta, 'DTREF')
      fnature = get_meta(meta, 'NATFLUX')
      ffrequence = get_meta(meta, 'TYPEFLUX')

    data['date'].append(fdate)
    data['nature'].append(fnature)
    data['frequence'].append(ffrequence)

    data['dossier'].append(ilen(dom.iter('InfosFoyerRSA')))
    data['personne'].append(ilen(dom.iter('Personne')))

    end = datetime.datetime.now()
    data['analysis'].append((end - start).total_seconds())

  df = pd.DataFrame.from_dict(data)
  output_path = os.path.join(root_path, 'files_summary_{}.xlsx'.format(ts.strftime("%Y-%m-%d_%H-%M-%S")))
  df.to_excel(output_path, index=False)
  print(output_path)
  print(df)


if __name__ == '__main__':
  main()
