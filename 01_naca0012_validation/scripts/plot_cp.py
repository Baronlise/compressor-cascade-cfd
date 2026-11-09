"""Trace Cp(x/c) : CFD Star-CCM+ vs essais, avec RMSE.

Usage :
  python plot_cp.py Cp_15_degres.csv --alpha 15 --exp gregory_alpha15.csv -o cp_alpha15.png
  python plot_cp.py Cp_0_degres.csv  --alpha 0  --exp gregory_alpha0.csv  -o cp_alpha0.png --single

Fichier CFD : export CSV d'un XY Plot Star-CCM+ (x, Cp, et si possible y).
Fichier essais : colonnes  x, cp, surface   (surface = upper ou lower)
"""
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def load_cfd(path):
    df = pd.read_csv(path)
    df = df.apply(pd.to_numeric, errors="coerce").dropna(axis=1, how="all").dropna()
    a = df.to_numpy()
    n = a.shape[1]
    if n < 2:
        raise SystemExit(f"Il faut au moins 2 colonnes numeriques, trouve {n}.")
    x, cp = a[:, 0], a[:, 1]
    y = a[:, 3] if n >= 4 else (a[:, 2] if n == 3 else None)
    return x, cp, y


def split_surfaces(x, cp, y):
    """Retourne (x_up, cp_up, x_lo, cp_lo)."""
    if y is not None:
        up = y >= 0
    else:
        # sans y : on coupe au bord d'attaque (x minimal), la branche la plus
        # basse en Cp (depression) est l'extrados
        i = int(np.argmin(x))
        b1, b2 = slice(0, i + 1), slice(i, None)
        up_is_first = cp[b1].min() < cp[b2].min()
        up = np.zeros(len(x), bool)
        up[b1 if up_is_first else b2] = True
    xu, cu = x[up], cp[up]
    xl, cl = x[~up], cp[~up]
    ou, ol = np.argsort(xu), np.argsort(xl)
    return xu[ou], cu[ou], xl[ol], cl[ol]


def rmse(xc, cc, xe, ce):
    if len(xc) < 2 or len(xe) == 0:
        return np.nan
    m = (xe >= xc.min()) & (xe <= xc.max())
    if not m.any():
        return np.nan
    return float(np.sqrt(np.mean((np.interp(xe[m], xc, cc) - ce[m]) ** 2)))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("cfd")
    p.add_argument("--alpha", type=float, required=True)
    p.add_argument("--exp")
    p.add_argument("--single", action="store_true",
                   help="alpha=0 : les deux surfaces se superposent")
    p.add_argument("--cells", default="")
    p.add_argument("--xmin", type=float, default=0.02,
                   help="RMSE 'hors bord d'attaque' calculee pour x/c >= xmin")
    p.add_argument("-o", "--out", required=True)
    a = p.parse_args()

    x, cp, y = load_cfd(a.cfd)
    fig, ax = plt.subplots(figsize=(7, 5))

    if a.single:
        o = np.argsort(x)
        ax.plot(x[o], cp[o], "-", color="C0", label="CFD, k-ω SST")
        cfd = {"upper": (x[o], cp[o])}
    else:
        xu, cu, xl, cl = split_surfaces(x, cp, y)
        ax.plot(xu, cu, "-", color="C0", label="CFD suction side")
        ax.plot(xl, cl, "-", color="C1", label="CFD pressure side")
        cfd = {"upper": (xu, cu), "lower": (xl, cl)}

    txt = []
    if a.exp:
        e = pd.read_csv(a.exp)
        for s, mk, col in (("upper", "o", "C0"), ("lower", "s", "C1")):
            d = e[e["surface"].str.lower() == s]
            if len(d) == 0 or s not in cfd:
                continue
            ax.plot(d["x"], d["cp"], mk, mfc="none", color=col,
                    label="Experiment, suction side (Gregory & O'Reilly)")
            xe, ce = d["x"].to_numpy(), d["cp"].to_numpy()
            r_all = rmse(*cfd[s], xe, ce)
            k = xe >= a.xmin
            r_x = rmse(*cfd[s], xe[k], ce[k])
            txt.append(f"RMSE, all points (n={len(xe)}) = {r_all:.3f}")
            txt.append(f"RMSE, x/c ≥ {a.xmin:g} (n={int(k.sum())}) = {r_x:.3f}")

    ax.invert_yaxis()
    lo, hi = ax.get_ylim()   # axe inverse : lo > hi
    ticks = list(ax.get_yticks())
    if lo >= 1 and 1 not in ticks:
        ticks.append(1)
    ax.set_yticks(sorted(t for t in ticks if hi <= t <= lo or lo <= t <= hi))
    ax.set_ylim(lo, hi)
    ax.set_xlim(0, 1)
    ax.set_xlabel("x/c")
    ax.set_ylabel("Cp")
    ax.grid(alpha=0.3)
    ax.set_title(f"NACA 0012, α = {a.alpha:g}°, M = 0.15, Re = 6×10⁶, "
                 f"k-ω SST {a.cells}".strip(), fontsize=10)
    if txt:
        ax.text(0.98, 0.02, "\n".join(txt), transform=ax.transAxes,
                ha="right", va="bottom", fontsize=9,
                bbox=dict(fc="white", ec="0.7"))
    ax.legend(fontsize=8)
    fig.text(0.01, 0.005, "Experiment: Re = 2.88×10⁶, digitized data, suction side only", fontsize=7, color="0.4")
    fig.tight_layout()
    fig.savefig(a.out, dpi=200)
    print("Figure :", a.out, *txt)


if __name__ == "__main__":
    main()
