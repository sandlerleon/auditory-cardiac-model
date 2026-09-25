# -*- coding: utf-8 -*-
"""Two figures: the proposed pathway, and what the loop model does.

Figure 1 replaces the ASCII schematic in the draft. Figure 2 is computed from
escalation_results.json.

    python make_figures.py
"""
import json

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

R = json.load(open("escalation_results.json"))
DPI = 300
plt.rcParams.update({"font.size": 8.5, "axes.labelsize": 9, "axes.titlesize": 9,
                     "legend.fontsize": 7.6, "xtick.labelsize": 8,
                     "ytick.labelsize": 8, "axes.linewidth": 0.8,
                     "font.family": "DejaVu Sans"})
BLUE, RED, GREEN, GREY = "#1b6ca8", "#c1553b", "#3f8f4a", "#8a8a8a"

# ============================================================ FIGURE 1
fig, ax = plt.subplots(figsize=(7.4, 7.0))
ax.set_xlim(0, 11.2); ax.set_ylim(-1.2, 12.4); ax.axis("off")

# Evidence coding (revised): green is reserved for the one step actually measured in
# dying patients (tone-evoked auditory ERPs). Links that are anatomy elsewhere but
# untested in this population are orange and dashed.
ORANGE = "#c98a1b"
BOXES = [
    ("Acoustic input\nstructured verbal pacing", 5.0, 11.6, BLUE, "in"),
    ("Cochlear nerve (CN VIII)", 5.0, 10.5, GREY, "path"),
    ("Brainstem auditory nuclei\ncochlear nucleus, superior olive,\ninferior colliculus",
     5.0, 9.2, GREY, "path"),
    ("Auditory cortex / temporal network\ntone-evoked ERPs measured in dying\n"
     "patients; semantic (N400) untested", 2.45, 7.45, GREEN, "branch"),
    ("Amygdala / limbic appraisal\nsubcortical route shown in animal\n"
     "studies; untested in dying patients", 7.55, 7.45, ORANGE, "branch"),
    ("Hypothalamus / central\nautonomic network", 5.0, 5.9, GREY, "path"),
    ("Vagus nerve (CN X)", 5.0, 4.8, GREY, "path"),
    ("Sinoatrial node\nreadout: high-frequency HRV", 5.0, 3.6, BLUE, "out"),
    ("Baroreceptor afferents\nvia nucleus tractus solitarius", 5.0, 2.3, GREY, "path"),
    ("Insular cortex\ninteroceptive state", 5.0, 1.0, GREY, "out"),
]
W = {"in": 3.5, "path": 3.6, "branch": 4.1, "out": 3.6}
H = {"in": 0.72, "path": 0.86, "branch": 0.72, "out": 0.72}
for text, x, y, col, kind in BOXES:
    w = W[kind]
    h = H[kind] if text.count("\n") < 2 else 1.05
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle="round,pad=0.06", linewidth=1.1,
                                linestyle="--" if col == ORANGE else "-",
                                edgecolor=col, facecolor=col + "18"))
    ax.text(x, y, text, ha="center", va="center", fontsize=7.2)


def arrow(x1, y1, x2, y2, col="#555555", style="-|>", rad=0.0, ls="-"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style,
                                 mutation_scale=11, lw=1.1, color=col, linestyle=ls,
                                 shrinkA=4.0, shrinkB=4.0, zorder=6,
                                 connectionstyle="arc3,rad=%.2f" % rad))


arrow(5.0, 11.24, 5.0, 10.93)
arrow(5.0, 10.07, 5.0, 9.73)
arrow(4.4, 8.67, 3.0, 8.02)
arrow(5.6, 8.67, 7.0, 8.02, col=ORANGE, ls="--")
arrow(3.0, 6.88, 4.5, 6.35, col=ORANGE, ls="--")
arrow(7.0, 6.88, 5.5, 6.35, col=ORANGE, ls="--")
arrow(5.0, 5.47, 5.0, 5.20)
arrow(5.0, 4.40, 5.0, 3.96)
arrow(5.0, 3.24, 5.0, 2.70)
arrow(5.0, 1.92, 5.0, 1.36)
# the proposed feedback limb that closes the loop
ax.add_patch(FancyArrowPatch((6.85, 1.0), (9.1, 6.88), arrowstyle="-|>",
                             mutation_scale=11, lw=1.1, color=RED, linestyle="--",
                             shrinkA=6, shrinkB=6, zorder=5,
                             connectionstyle="arc3,rad=-0.34"))
ax.text(10.75, 3.9, "proposed: interoceptive state feeds\nback into threat appraisal",
        fontsize=7.0, color=RED, ha="center", va="center", rotation=90)
ax.text(5.0, 12.2, "Proposed auditory–cardiac pathway", ha="center",
        fontsize=10.5, fontweight="bold")
ax.text(0.15, -0.75,
        "Grey: established anatomy. Green: measured in dying patients (tone-evoked auditory ERPs only).\n"
        "Orange, dashed: proposed links, untested in dying patients. Blue: proposed intervention and readout.\n"
        "Anatomical connection is not evidence of a therapeutic effect.",
        fontsize=6.8, color="#555555", ha="left")
fig.tight_layout()
fig.savefig("figure1_pathway.png", dpi=DPI, bbox_inches="tight")
plt.close(fig)
print("figure1_pathway.png")

# ============================================================ FIGURE 2
fig, ax = plt.subplots(1, 2, figsize=(9.6, 3.7))

# --- A: metabolite trajectories
import escalation_model as EM
base = EM.run(V=0.0)
damp = EM.run(V=0.35)
full = EM.run(V=1.5)
for r, col, lab, ls in [(base, RED, "no intervention", "-"),
                        (damp, BLUE, "modest damping", "-"),
                        (full, GREEN, "maximal damping", "--")]:
    ax[0].plot(r["t"], r["M"], color=col, lw=1.7, ls=ls, label=lab)
    if r["cross"]:
        ax[0].plot([r["cross"]], [EM.P0["Mstar"]], "o", ms=5, color=col,
                   markeredgecolor="white", markeredgewidth=0.7, zorder=6)
ax[0].axhline(EM.P0["Mstar"], color="#333333", lw=1.1, ls=":")
ax[0].text(0.12, EM.P0["Mstar"] + 0.05, "illustrative model threshold M*", fontsize=7.2,
           color="#333333")
ax[0].set_xlim(0, 4.0); ax[0].set_ylim(0, 2.4)
ax[0].set_xlabel("days from start of continuous infusion")
ax[0].set_ylabel("accumulated metabolite M (model units)")
ax[0].set_title("A   Damping postpones the threshold", loc="left", fontweight="bold")
ax[0].legend(frameon=False, loc="lower right")

# --- B: delay against damping, with the ceiling
V = np.array(R["sweep"]["V"])
cross = np.array([c if c is not None else np.nan for c in R["sweep"]["cross_day"]])
delay = (cross - R["baseline"]["cross_day"]) * 24.0
ax[1].plot(V, delay, color=BLUE, lw=1.9)
ax[1].axhline(R["max_delay_hours"], color=GREY, lw=1.1, ls="--")
ax[1].text(2.95, R["max_delay_hours"] + 1.0, "ceiling %.1f h" % R["max_delay_hours"],
           ha="right", fontsize=7.6, color="#444444")
ax[1].plot([0.35], [R["intervention"]["delay_hours"]], "o", ms=6, color=RED,
           markeredgecolor="white", markeredgewidth=0.7, zorder=6)
ax[1].annotate("modest damping\n+%.1f h" % R["intervention"]["delay_hours"],
               xy=(0.35, R["intervention"]["delay_hours"]), xytext=(0.62, 4.0),
               fontsize=7.4, color=RED,
               arrowprops=dict(arrowstyle="->", lw=0.9, color=RED))
ax[1].set_xlim(0, 3.0); ax[1].set_ylim(0, R["max_delay_hours"] * 1.22)
ax[1].set_xlabel("vagal damping supplied by the intervention (model units)")
ax[1].set_ylabel("delay in reaching the threshold (hours)")
ax[1].set_title("B   The delay is bounded", loc="left", fontweight="bold")
ax[1].text(0.06, R["max_delay_hours"] * 1.10,
           "no damping strength prevents the crossing", fontsize=7.4, color="#444444")

for a in ax:
    a.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig("figure2_model.png", dpi=DPI, bbox_inches="tight")
plt.close(fig)
print("figure2_model.png")
