### Objectif : représenter une séquence via une classe et lire un fichier FASTA

class Sequence :

    def __init__(self, nom, residus) :
        self.nom = nom
        self.residus = residus

    def __len__(self):
        return len(self.residus)

    def mots(self, w):
        # nombre de mots = len(self) - w + 1, on veut dans liste la position (début de la fenêtre flissante) et les résidus de cette fenêtre
        liste = []
        for position in range(len(self) - w + 1):
            liste.append((position, self.residus[position:position + w]))
        return liste



def lire_fasta(chemin):
    with open(chemin) as fichier:
        lignes = fichier.read().splitlines()

    sequences = []
    for ligne in lignes:
        if ligne.startswith(">"):
            nom = ligne[1:].strip()
            nouvelle = Sequence(nom, "")
            sequences.append(nouvelle)

        else:
            sequences[-1].residus += ligne

    return sequences
