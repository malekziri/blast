"""
Classe Blast :
    1- trouver les hits à partir mots de la requête dans la banque
    2- étendre un hit d'un côté (X-drop)
    3- étendre un hit des deux côtés (HSP)
    4- étendre tous les hits
    5- calculer l'E-value de chaque HSP
    6- lancer la recherche
"""

from statistiques import Statistiques
from hsp import HSP


class Blast:

    def __init__(self, matrice, banque, T=13, X=16, evalue_max=10):
        self.matrice = matrice
        self.banque = banque
        self.w = banque.w
        self.T = T
        self.X = X
        self.evalue_max = evalue_max
        self.stats = Statistiques()

    def trouver_hits(self, requete):
        hits = []
        for pos_requete, mot in requete.mots(self.w):
            for voisin in self.matrice.mots_voisins(mot, self.T):
                for numero, pos_sujet in self.banque.occurrences(voisin):
                    hits.append((numero, pos_requete, pos_sujet))
        return hits

    def _etendre_un_cote(self, requete, sujet, i, j, pas):
        score, meilleur, lettres_gardees, lettres_lues = 0, 0, 0, 0
        while 0 <= i < len(requete) and 0 <= j < len(sujet):
            score += self.matrice.score(requete.residus[i], sujet.residus[j])
            lettres_lues += 1
            if score > meilleur:
                meilleur = score
                lettres_gardees = lettres_lues
            elif meilleur - score > self.X:
                break
            i += pas
            j += pas
        return meilleur, lettres_gardees

    def etendre(self, requete, sujet, pos_q, pos_s): #pos_q et pos_s position du hit dans requête et sujet (séquence dans banque)
        graine = self.matrice.score_mots(requete.residus[pos_q:pos_q + self.w],
                                         sujet.residus[pos_s:pos_s + self.w])
        gain_d, n_droite = self._etendre_un_cote(
            requete, sujet, pos_q + self.w, pos_s + self.w, +1)
        gain_g, n_gauche = self._etendre_un_cote(
            requete, sujet, pos_q - 1, pos_s - 1, -1)
        return HSP(requete, sujet,
                   debut_requete=pos_q - n_gauche,
                   debut_sujet=pos_s - n_gauche,
                   longueur=n_gauche + self.w + n_droite,
                   score=graine + gain_g + gain_d)

    def etendre_tous_les_hits(self, requete, hits):
        meilleurs = {}   #meilleur HSP trouvé sur cette diagonale
        for numero, pos_q, pos_s in hits:
            sujet = self.banque.sequences[numero]
            hsp = self.etendre(requete, sujet, pos_q, pos_s)
            diagonale = (numero, pos_s - pos_q)
            if diagonale not in meilleurs or hsp.score > meilleurs[diagonale].score:
                meilleurs[diagonale] = hsp
        return list(meilleurs.values())

    def calculer_evalues(self, requete, hsps):
        m, n = len(requete), self.banque.taille_totale()
        for hsp in hsps:
            hsp.evalue = self.stats.evalue(hsp.score, m, n)

    def rechercher(self, requete):
        hits = self.trouver_hits(requete)
        hsps = self.etendre_tous_les_hits(requete, hits)
        self.calculer_evalues(requete, hsps)
        significatifs = [h for h in hsps if h.evalue <= self.evalue_max]
        return sorted(significatifs, key=lambda h: h.evalue)
