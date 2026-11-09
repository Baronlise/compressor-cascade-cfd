"""GCI sur trois maillages (procedure de Celik et al. 2008 / Roache).

Usage : python gci.py        (modifie les valeurs en bas du fichier)
Raffinement : h = (1/N)^(1/2) en 2D, calcule a partir du nombre de cellules.
Ordre apparent p par iteration de point fixe, facteur de securite Fs = 1,25.
"""
import math


def gci(N, f, Fs=1.25):
    """N, f : [fin, moyen, grossier]. Retourne un dictionnaire de resultats."""
    h = [(1.0 / n) ** 0.5 for n in N]
    r21, r32 = h[1] / h[0], h[2] / h[1]
    e21, e32 = f[1] - f[0], f[2] - f[1]
    if e21 == 0 or e32 == 0 or e32 / e21 < 0:
        return {"erreur": "convergence non monotone : GCI non applicable"}
    s = 1.0
    p = 2.0
    for _ in range(200):
        q = math.log((r21 ** p - s) / (r32 ** p - s))
        p_new = abs(math.log(abs(e32 / e21)) + q) / math.log(r21)
        if abs(p_new - p) < 1e-10:
            break
        p = p_new
    f_ext = (r21 ** p * f[0] - f[1]) / (r21 ** p - 1)
    e_a = abs((f[0] - f[1]) / f[0])
    return {
        "r21": r21, "r32": r32, "p": p,
        "f_extrapolee": f_ext,
        "ecart_relatif_fin_moyen_%": 100 * e_a,
        "GCI_fin_%": 100 * Fs * e_a / (r21 ** p - 1),
    }


if __name__ == "__main__":
    # Etude de convergence en maillage, domaine de 400 c (moyennes sur 300 iterations).
    # Ordre dans chaque liste : fin, moyen, grossier.
    ETUDES = {
        "alpha = 10 deg": {
            "cellules": [332499, 194679, 112033],
            "Cd": [0.0129412, 0.0133583, 0.0142805],
            "Cd pression": [0.0071328, 0.0076051, 0.0086263],
            "Cd frottement": [0.0058086, 0.0057533, 0.0056540],
            "Cl": [1.080367, 1.076037, 1.073593],
        },
        "alpha = 15 deg": {
            "cellules": [369075, 216349, 121664],
            "Cd": [0.0246294, 0.0265271, 0.0311805],
            "Cd pression": [0.0196647, 0.0216807, 0.0266006],
            "Cd frottement": [0.0049645, 0.0048462, 0.0046056],
            "Cl": [1.487542, 1.464913, 1.415074],
        },
    }
    for titre, etude in ETUDES.items():
        print(f"\n{titre} (domaine 400 c)")
        print(f"{'grandeur':<15}{'ordre p':>9}{'valeur extrapolee':>20}{'GCI maillage fin':>19}")
        for nom, valeurs in etude.items():
            if nom == "cellules":
                continue
            r = gci(etude["cellules"], valeurs)
            if "erreur" in r:
                print(f"{nom:<15}  {r['erreur']}")
                continue
            print(f"{nom:<15}{r['p']:>9.2f}{r['f_extrapolee']:>20.6f}{r['GCI_fin_%']:>18.1f}%")
