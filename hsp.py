"""
Classe HSP (High-scoring Segment Pair) et affiche l'alignement blast
"""


class HSP:

    def __init__(self, requete, sujet, debut_requete, debut_sujet, longueur, score):
        self.requete = requete
        self.sujet = sujet
        self.debut_requete = debut_requete
        self.debut_sujet = debut_sujet
        self.longueur = longueur
        self.score = score
        self.evalue = None

    def segment_requete(self):
        return self.requete.residus[self.debut_requete:self.debut_requete + self.longueur]

    def segment_sujet(self):
        return self.sujet.residus[self.debut_sujet:self.debut_sujet + self.longueur]

    def identites(self):
        total = 0
        for a, b in zip(self.segment_requete(), self.segment_sujet()):
            if a == b:
                total += 1
        return total

    def afficher(self):
        print(">" + self.sujet.nom)
        print(f"  Score = {self.score}, E-value = {self.evalue:.2g}")
        print(f"  Identités = {self.identites()}/{self.longueur}")
        print(f"  Query  {self.debut_requete + 1}  {self.segment_requete()}")
        print(f"  Sbjct  {self.debut_sujet + 1}  {self.segment_sujet()}")
        print()
