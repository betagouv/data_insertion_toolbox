import datetime
import glob
import gzip
import pandas as pd
import os
import sys
from tqdm import tqdm
import xml.etree.ElementTree as ET

from cnaf_files import process, ERROR_VALUE, NOT_APPLICABLE_VALUE


def ilen(iterable):
    return sum(1 for _ in iterable)


def get_meta(meta, item):
  try:
    return list(meta.iter(item))[0].text
  except IndexError:
    return 'Error'


def main():
  root_path = sys.argv[len(sys.argv)-1]
  matches_base = glob.glob("{}{}**{}*.xml".format(root_path, os.sep, os.sep), recursive=True)
  matches_gz = glob.glob("{}{}**{}*.xml.gz".format(root_path, os.sep, os.sep), recursive=True)
  matches = matches_base + matches_gz
  ts = datetime.datetime.now()

  data = {
    "path": [],
    "size": [],
    "analysis": [],
    "date": [],
    "nature": [],
    "frequence": [],
    "dossier": [],
    "dossier_soumis_DD": [],
    "dossier_erreur": [],
    "personne": [],
    "personne_soumise_DD": [],
    "personne_entrante": [],
    "personne_entrante_erreur": [],
    "personne_sans_TOPPERSDRODEVORSA": [],
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

    (applications, applicants) = process(dom)

    data['dossier'].append(len(applications))
    data['personne'].append(len(applicants))

    data['dossier_soumis_DD'].append(len([a for a in applications if a.withRights()]))
    data['personne_soumise_DD'].append(len([a for a in applicants if a.withRights()]))

    data['personne_entrante'].append(len([a for a in applicants if a.topEntrant]))
    data['personne_entrante_erreur'].append(len([a for a in applicants if a.topEntrant and not a.withRights()]))

    data['dossier_erreur'].append(len([a for a in applications if a.statusCode == ERROR_VALUE]))
    data['personne_sans_TOPPERSDRODEVORSA'].append(len([a for a in applicants if a.topDroitsEtDevoirs == NOT_APPLICABLE_VALUE]))

    end = datetime.datetime.now()
    data['analysis'].append((end - start).total_seconds())

    if True:
      data_path = '{}_applicant_extract_{}.csv'.format(m, ts.strftime("%Y-%m-%d_%H-%M-%S"))
      applicant_data = {
        'NUMDEMRSA': [],
        'MATRICULE': [],
        'id': [],
        'ROLEPERS': [],
        'TOPPERSDRODEVORSA': [],
        'TOPPERSENTDRODEVORSA': [],
        'ETATDOSRSA': [],
        'MOTISUSVERSRSA': [],
        'applicationWithRights': [],
        'withRights': [],
        }
      for a in applicants:
        applicant_data['NUMDEMRSA'].append(a.application.rsaApplicationNumber)
        applicant_data['MATRICULE'].append(a.application.matricule)
        applicant_data['id'].append(a.aid)
        applicant_data['ROLEPERS'].append(a.role)
        applicant_data['TOPPERSDRODEVORSA'].append(a.topDroitsEtDevoirs)
        applicant_data['TOPPERSENTDRODEVORSA'].append(a.topEntrant)
        applicant_data['ETATDOSRSA'].append(a.application.statusCode)
        applicant_data['MOTISUSVERSRSA'].append(a.application.suspensionMotive)
        applicant_data['applicationWithRights'].append(a.application.withRights())
        applicant_data['withRights'].append(a.withRights())
      applicant_df = pd.DataFrame.from_dict(applicant_data)
      applicant_df.to_csv(data_path, index=False)

  df = pd.DataFrame.from_dict(data)
  output_path = os.path.join(root_path, 'files_summary_{}.xlsx'.format(ts.strftime("%Y-%m-%d_%H-%M-%S")))
  df.to_excel(output_path, index=False)
  print(output_path)
  print(df)


if __name__ == '__main__':
  main()
