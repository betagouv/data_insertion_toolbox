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


# Valeurs :
# "01" : Ressources trop élévées
# "02" : Moins 25 ans sans enft/autre person. à charge
# "03" : Activité non conforme
# "04" : Titre de séjour non valide
# "05" : RSA inférieur au seuil
# "06" : Déclaration Trimestrielle Ressources non fournie
# "09" : Résidence non conforme
# "19" : Pas d'isolement
# "31" : Prestation exclue affil partielle
# "34" : Régime non conforme
# "35" : Demande avantage vielliesse absent ou tardif
# "36" : Titre de séjour absent
# "44" : Hospitalisation
# "70" : Action non engagée
# "78" : Surface pondérée > plafond ou inconnue
# "84" : Droit éteint
# "85" : Pas d'allocataire
# "97" : Bénéficiaire AAH réduite
# "AB" : Allocataire absent du foyer
# "CV"  : Attente décision PCG (le droit reste théorique jusqu'au retour)
# "CG" : Application Sanction -> integré dans les ETATDOSRSA=2
# "CZ" : Activité antérieure insuffisante
# "DA" : Activité antérieure absente
# "DB" : Etudiant rémunération insuff.
# "DC" : Activité antérieure non conforme
REAL_ELIGIBLE_SUSPENSION_MOTIVES = ["05", "44", "70"]
THEORICAL_ELIGIBLE_SUSPENSION_MOTIVES = ["01", "06", "35", "36"]
ELIGIBLE_SUSPENSION_MOTIVES = REAL_ELIGIBLE_SUSPENSION_MOTIVES + THEORICAL_ELIGIBLE_SUSPENSION_MOTIVES

ERROR_VALUE = "ERROR"
NOT_APPLICABLE_VALUE = "-1"

def get(node, attribute, default_value=ERROR_VALUE):
  try:
    return next(node.iter(attribute)).text
  except Exception as e:
    return default_value


class Application(object):
  def __init__(self, node):
    super(Application, self).__init__()
    self.rsaApplicationNumber = get(node,"NUMDEMRSA")
    self.matricule = get(node, "MATRICULE")
    self.statusCode = get(node,"ETATDOSRSA")
    self.suspensionMotive = get(node,"MOTISUSVERSRSA", NOT_APPLICABLE_VALUE)

  def withDroitsOuvertsEtVersables(self):
    return self.statusCode == "2"

  def withRights(self):
    return self.withDroitsOuvertsEtVersables() or self.statusCode == "3" or (
      self.statusCode == "4" and self.suspensionMotive in ELIGIBLE_SUSPENSION_MOTIVES)


class Applicant(object):
  def __init__(self, node, application):
    super(Applicant, self).__init__()
    self.application = application
    self.role = get(node,'ROLEPERS')
    self.topDroitsEtDevoirs = get(node,'TOPPERSDRODEVORSA', NOT_APPLICABLE_VALUE)
    self.topEntrant = get(node,'TOPPERSENTDRODEVORSA', NOT_APPLICABLE_VALUE) == "1"
    self.aid = '{}-{}'.format(self.application.rsaApplicationNumber, self.role)

  def withDroitsEtDevoirs(self):
    return self.topDroitsEtDevoirs == "1"

  def withRights(self):
    return self.withDroitsEtDevoirs() and self.application.withRights()
