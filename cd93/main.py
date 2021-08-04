import datetime
import glob
import os
import xml.etree.ElementTree as ET
import sys


def main():
  root_path = sys.argv[len(sys.argv)-1]
  split_file_paths = glob.glob("{}*.RCV".format(root_path))
  grouped_path = list(set([item[0:-7] for item in split_file_paths]))

  if len(grouped_path) == 0:
    print("Aucun fichier à traiter.")

  for prefix_path in grouped_path:
    print(prefix_path)
    sources = [i for i in split_file_paths if i.startswith(prefix_path)]

    base = None
    last = None
    for s in sources:
        tree = ET.parse(s)
        root = tree.getroot()
        if base is None:
            base = tree
            last = root[-1]
            root.remove(last)
        else:
            group_root = base.getroot()
            for i in root.iter('InfosFoyerRSA'):
                group_root.append(i)
    base.getroot().append(last)

    result_path = "{}.xml".format(prefix_path)
    if os.path.exists(result_path):
      ts = datetime.datetime.now()
      result_path = "{}_{}.xml".format(prefix_path, ts.strftime("%Y-%m-%d_%H-%M-%S"))

    with open(result_path, 'w') as f:
      base.write(f, encoding="unicode")


if __name__ == '__main__':
  main()
