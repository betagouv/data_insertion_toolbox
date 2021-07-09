from cryptography.fernet import Fernet
from datetime import datetime
from dotenv import load_dotenv
import sys
import zipfile

from hubee import get_token, send
from transfert import get_encryption_tool


def generate_default_file():
  from tempfile import NamedTemporaryFile
  timestamp = datetime.now()
  filename = "content.txt"
  with NamedTemporaryFile('w') as f:
    f.write('Fichier généré à {}'.format(timestamp.isoformat()))
    f.flush()

    return generate_archive_file(f.name)


def generate_archive_file(filename):
  from tempfile import NamedTemporaryFile

  encryption_tool = get_encryption_tool()

  timestamp = datetime.now()

  with open(filename, 'rb') as in_file:
    with open(filename + '.enc', 'wb') as out_file:
      out_file.write(encryption_tool.encrypt(in_file.read()))

  archive_name = 'archive_{}.zip'.format(timestamp.strftime("%Y%m%d_%H%M%S"))
  with zipfile.ZipFile(archive_name, 'w') as a:
    a.write(filename + '.enc')
  return archive_name


def main():
  load_dotenv()
  hubee_token = get_token("OSL")

  if '--' not in sys.argv:
    print('La commande doit être appelée avec -- xxx yyy [nom du fichier] où (xxx, yyy) représente (company_register, branch_code)')
    return

  argv = sys.argv[sys.argv.index('--')+1:]
  if len(argv) < 2 or len(argv) > 3:
    print('La commande doit être appelée avec -- xxx yyy [nom du fichier] où (xxx, yyy) représente (company_register, branch_code)')
    return

  company_register = argv[0]
  branch_code = argv[1]
  if len(argv) == 2:
    filename = generate_default_file()
  else:
    filename = generate_archive_file(argv[2])
  result = send(company_register, branch_code, filename, hubee_token)
  print(result)


if __name__ == '__main__':
  main()
