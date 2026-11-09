"""Regenere toutes les figures et les calculs de GCI du projet en une seule commande.

Depuis la racine du depot :
    python scripts/make_figures.py
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run(*args):
    subprocess.run([sys.executable, *map(str, args)], check=True, cwd=ROOT)


# (angle en degres, texte du nombre de cellules pour la legende)
CASES = [(15, "369k"), (10, "332k"), (0, "266k")]

for alpha, cells in CASES:
    cmd = [
        "scripts/plot_cp.py", f"data/Cp_{alpha}_degres_R400.csv",
        "--alpha", alpha, "--exp", f"data/gregory_alpha{alpha}.csv",
        "-o", f"figures/cp_alpha{alpha}_R400.png",
        "--cells", f"({cells} cells, R = 400 c)",
    ]
    if alpha == 0:
        cmd.append("--single")   # a 0 deg, extrados et intrados se superposent
    run(*cmd)

run("scripts/gci.py")           # affiche l'etude de convergence en maillage (10 deg)
run("scripts/plot_summary.py")  # figure de synthese Cl / Cd
print("Termine : les figures sont dans le dossier figures/")
