"""Figure de synthese NACA 0012 : ecart relatif CFD / reference TMR (SST) pour Cl et Cd.

Reference = milieu de la plage des codes (CFL3D, FUN3D, NTS) ; la bande grisee est
l'etalement de ces codes. CFD = maillage fin, R = 400 c. Les barres d'erreur de Cd sont
le GCI du maillage fin ; les losanges creux sont les valeurs extrapolees (Richardson)."""
from pathlib import Path
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent

cl = {  # alpha: (cfd, extrapole, ref_min, ref_max)
    10: (1.080367, 1.0855, 1.0765, 1.0840),
    15: (1.487542, 1.5105, 1.5068, 1.5110),
}
cd = {  # alpha: (cfd, extrapole, ref_min, ref_max, GCI %)
    0: (0.0078090, None, 0.00808, 0.00809, None),
    10: (0.0129412, 0.012566, 0.01236, 0.01253, 3.6),
    15: (0.0246294, 0.023045, 0.02187, 0.02275, 8.0),
}

def pct(v, lo, hi):
    mid = 0.5 * (lo + hi)
    return 100 * (v / mid - 1)

fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))

# --- Cl ---
a_ax = ax[0]
for a, (v, e, lo, hi) in cl.items():
    mid = 0.5 * (lo + hi)
    a_ax.fill_between([a - 0.8, a + 0.8], 100 * (lo / mid - 1),
                      100 * (hi / mid - 1), color="0.8",
                      label="TMR reference spread" if a == 10 else None)
    a_ax.plot(a, pct(v, lo, hi), "o", color="C0", label="CFD, fine mesh" if a == 10 else None)
    a_ax.plot(a, pct(e, lo, hi), "D", mfc="none", color="C3",
              label="Richardson-extrapolated" if a == 10 else None)
a_ax.axhline(0, color="k", lw=0.6)
a_ax.set_title("Cl", fontsize=10)

# --- Cd ---
b_ax = ax[1]
for a, (v, e, lo, hi, g) in cd.items():
    mid = 0.5 * (lo + hi)
    b_ax.fill_between([a - 0.8, a + 0.8], 100 * (lo / mid - 1), 100 * (hi / mid - 1), color="0.8")
    err = pct(v, lo, hi)
    yerr = (v * g / 100) / mid * 100 if g else 0
    b_ax.errorbar(a, err, yerr=yerr, fmt="o", color="C0", capsize=4,
                  label="CFD, fine mesh \u00b1 mesh uncertainty (GCI)" if a == 10 else None)
    if g:
        b_ax.annotate(f"GCI \u00b1{g:.1f} %", (a, err + yerr), textcoords="offset points",
                      xytext=(8, -2), fontsize=8, color="C0")
    if e:
        b_ax.plot(a, pct(e, lo, hi), "D", mfc="none", color="C3")
b_ax.axhline(0, color="k", lw=0.6)
b_ax.plot([], [], "D", mfc="none", color="C3", label="Richardson-extrapolated")
b_ax.fill_between([], [], [], color="0.8", label="TMR reference spread")
b_ax.legend(fontsize=8, loc="upper left")
b_ax.set_title("Cd", fontsize=10)

for a_ax_ in ax:
    a_ax_.set_xlabel("\u03b1 (deg)")
    a_ax_.set_ylabel("Deviation from reference mid-range (%)")
    a_ax_.set_xticks([0, 10, 15])
    a_ax_.set_xlim(-1.5, 16.5)
    a_ax_.grid(alpha=0.3)
ax[0].legend(fontsize=8, loc="lower left")
fig.suptitle("NACA 0012, M = 0.15, Re = 6\u00d710\u2076, k-\u03c9 SST (Star-CCM+, R = 400 c) vs TMR SST reference",
             fontsize=10)
fig.tight_layout()
out = ROOT / "figures" / "naca0012_validation_summary.png"
fig.savefig(out, dpi=200)
print("Figure :", out)
