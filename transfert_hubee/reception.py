from cryptography.fernet import Fernet
import datetime
from dotenv import load_dotenv
import os
import sys
import zipfile
from tempfile import NamedTemporaryFile

from hubee import get_token, get_notifications, get_case, get_attachment, patch_case, delete_notification
from transfert import get_encryption_tool


def main():
  ts = datetime.datetime.now()
  load_dotenv()
  if '--' not in sys.argv:
    print('La commande doit être appelée avec -- xxx où xxx représente le company_register')
    return

  argv = sys.argv[sys.argv.index('--')+1:]
  if len(argv) != 1:
    print('La commande doit être appelée avec -- xxx où xxx représente le company_register')
    return

  company_source = argv[0]

  hubee_token = get_token("SI")
  encryption_tool = get_encryption_tool()

  notifications = get_notifications(hubee_token)
  interesting_notifications = [n for n in notifications if n['transmitter']['companyRegister'] == company_source ]

  if not len(interesting_notifications):
    print('Aucun fichier à traiter. Arrêt.')
    return

  notification = interesting_notifications[0]
  case_id = notification['caseId']
  case = get_case(case_id, hubee_token)

  output_dir = '{}_case_{}'.format(ts.strftime("%Y-%m-%-d_%H-%M-%S"), case_id)
  os.mkdir(output_dir)

  for attachment in case['attachments']:
    attachment_path = os.path.join(output_dir, attachment['fileName'])
    with open(attachment_path, 'wb') as f:
      attachment_data = get_attachment(case['id'], attachment['id'], hubee_token)
      f.write(attachment_data.content)

    with zipfile.ZipFile(attachment_path) as myzip:
      for file in myzip.infolist():
        if not file.filename.endswith('.enc'):
          continue

        myzip.extract(file.filename, output_dir)
        with open(os.path.join(output_dir, file.filename), 'rb') as in_file:
          clearfile_name = os.path.join(output_dir, file.filename[0:-len('.enc')])
          with open(clearfile_name, 'wb') as out_file:
            out_file.write(encryption_tool.decrypt(in_file.read()))

    patch_case(case_id, {"status": "DONE"}, hubee_token)
    delete_notification(notification['id'], hubee_token)


if __name__ == '__main__':
  main()
