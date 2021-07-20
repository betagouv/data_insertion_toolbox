import xml.etree.ElementTree as ET
from pprint import pprint

def main():
  file_path = "/home/thomas/Documents/Beta.gouv.fr/data.insertion/Fichers d'exemple/CG005.RSABEM.anonyme.xml"
  tree = ET.parse(file_path)
  root = tree.getroot()
  print(root)

if __name__ == '__main__':
  main()


def process(root):
  applications = []
  applicants = []
  for applicationNode in root.iter('InfosFoyerRSA'):
    application = Application(applicationNode)
    applications.append(application)

    for applicantNode in applicationNode.iter('Personne'):
      applicants.append(Applicant(applicantNode, application))

  return (applications, applicants)


ELIGIBLE_SUSPENSION_MOTIVES = ["01", "05", "06", "35", "36"]


ERROR_VALUE = "ERROR"

def get(node, attribute):
  try:
    return next(node.iter(attribute)).text
  except Exception as e:
    return ERROR_VALUE


class Application(object):
  def __init__(self, node):
    super(Application, self).__init__()
    self.rsaApplicationNumber = get(node,"NUMDEMRSA")
    self.statusCode = get(node,"ETATDOSRSA")
    self.suspensionMotive = get(node,"MOTISUSVERSRSA")

  def withDroitsOuvertsEtVersables(self):
    return self.statusCode == "2"

  def withDroitsOuvertsSuspendu(self):
    return self.statusCode == "4"

  def withRights(self):
    return self.withDroitsOuvertsEtVersables() or (
      self.withDroitsOuvertsSuspendu() and self.suspensionMotive in ELIGIBLE_SUSPENSION_MOTIVES)


class Applicant(object):
  def __init__(self, node, application):
    super(Applicant, self).__init__()
    self.application = application
    self.role = get(node,'ROLEPERS')
    self.topDroitsEtDevoirs = get(node,'TOPPERSDRODEVORSA')
    self.aid = '{}-{}'.format(self.application.rsaApplicationNumber, self.role)

  def withDroitsEtDevoirs(self):
    return self.topDroitsEtDevoirs == "1"

  def withRights(self):
    return self.withDroitsEtDevoirs() and self.application.withRights()
