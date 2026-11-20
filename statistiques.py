"""
Classe Statistiques avec fonction pour :
    1- calculer l'E-value d'un score : E = K * m * n * exp(-lambda * S)
"""

import math


class Statistiques:

    def __init__(self, lambda_=0.3176, K=0.134):
        self.lambda_ = lambda_   # valeur tabulée NCBI pour BLOSUM62 sans gap
        self.K = K               # valeur tabulée NCBI pour BLOSUM62 sans gap

    def evalue(self, score, m, n):
        return self.K * m * n * math.exp(-self.lambda_ * score)
