"""
Programme principal
"""

from sequence import lire_fasta
from matrice import MatriceSubstitution
from banque import Banque
from blast import Blast

FICHIER_REQUETE = "data/P69905_Hbalpha_humaine.fasta"
FICHIER_BANQUE = "data/banque.fasta"
W = 3
T = 13
X = 16


def main():
    # 1. Lire les séquences
    requete = lire_fasta(FICHIER_REQUETE)[0]
    sequences = lire_fasta(FICHIER_BANQUE)

    # 2. Préparer les objets
    matrice = MatriceSubstitution()
    banque = Banque(sequences, W)
    blast = Blast(matrice, banque, T=T, X=X)

    # 3. Lancer BLAST
    resultats = blast.rechercher(requete)

    # 4. Afficher
    print(f"Requête : {requete.nom} ({len(requete)} aa)")
    print(f"Banque : {len(banque)} séquences, {banque.taille_totale()} aa")
    print(f"lambda = {blast.stats.lambda_:.4f}")
    print(f"{len(resultats)} HSP avec E-value <= {blast.evalue_max}")
    print()
    for hsp in resultats:
        hsp.afficher()


if __name__ == "__main__":
    main()
