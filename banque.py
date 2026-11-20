"""
Classe Banque  :
    1- ranger les séquences en une banque
    2- découper chaque séquence en mots de w lettres et les ranger dans un dictionnaire : mot : [(numéro de séquence, position)]
    3- autres paramètres (occurence, taille de la banque, nombre de séquences)
"""

class Banque:

    def __init__(self, sequences, w):
        self.sequences = sequences
        self.w = w
        self.index = {}
        self._construire_index()

    def _construire_index(self):
        for numero, sequence in enumerate(self.sequences):
            for position, mot in sequence.mots(self.w):
                self.index.setdefault(mot, []).append((numero, position))

    def occurrences(self, mot):
        return self.index.get(mot, [])

    def taille_totale(self):
        return sum(len(sequence) for sequence in self.sequences)

    def __len__(self):
        return len(self.sequences)
