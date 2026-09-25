# -*- coding: utf-8 -*-
"""A minimal model of the terminal opioid escalation loop, and what an
affective-gain reduction would do to it.

The clinical problem is a feedback: distress raises perceived pain, perceived
pain prompts dose escalation, escalation in a patient whose clearance is falling
accumulates metabolite, and metabolite accumulation produces agitation that is
read as pain and prompts further escalation.

    perceived pain      P = N * (1 + g*A)
    autonomic arousal   dA/dt = (a0 + kP*P - kV*V - A) / tau_A
    dose               dD/dt = (D_target(P) - D) / tau_D
    metabolite          dM/dt = kM*D - CL(t)*M
    clearance           CL(t) = CL0 * exp(-t/tau_CL)

N is nociceptive drive, g the affective gain, V a vagally mediated damping term
standing for the auditory intervention, and M the accumulating active metabolite.
Neurotoxicity is modelled as M crossing a threshold M*, above which an agitation
term is added to N -- which is what closes the loop.

EVERY parameter here is illustrative. None is fitted to patient data, and the
model is not a pharmacokinetic simulation of morphine. Its purpose is to show
what kind of behaviour the proposed loop can produce and what would have to be
measured to refute it. Results are reported as relative changes, never as
predicted doses or survival times.

    python escalation_model.py
"""
import json

import numpy as np

SEED = 20260920

# ---- illustrative parameters, all ASSUMED (see the manuscript's status table)
P0 = dict(
    N0=1.0,        # baseline nociceptive drive, arbitrary units
    g=0.80,        # affective gain: how much arousal amplifies perceived pain
    a0=0.30,       # baseline arousal
    kP=0.55,       # how strongly perceived pain drives arousal
    tau_A=0.25,    # arousal time constant, days
    tau_D=0.15,    # dose-adjustment time constant, days
    kM=1.0,        # metabolite formation per unit dose
    CL0=1.6,       # initial metabolite clearance, per day
    tau_CL=3.0,    # clearance decay time constant, days
    Mstar=1.0,     # neurotoxicity threshold, normalised
    kAgit=0.9,     # agitation added to nociceptive drive once M > Mstar
    Dmax=6.0,      # ceiling on dose, arbitrary units
)
T_END, DT = 10.0, 0.002


def run(V=0.0, p=None, t_end=T_END, dt=DT):
    """Integrate the loop. V is the vagal damping supplied by the intervention."""
    p = dict(P0, **(p or {}))
    n = int(t_end / dt)
    t = np.linspace(0, t_end, n)
    A = np.empty(n); D = np.empty(n); M = np.empty(n); P = np.empty(n)
    A[0], D[0], M[0] = p["a0"], 0.0, 0.0
    CL = p["CL0"] * np.exp(-t / p["tau_CL"])
    crossed = None
    for i in range(n - 1):
        agit = p["kAgit"] if M[i] > p["Mstar"] else 0.0
        N = p["N0"] + agit
        P[i] = N * (1.0 + p["g"] * A[i])
        # clinicians titrate toward perceived pain
        D_target = min(P[i], p["Dmax"])
        A[i + 1] = A[i] + dt * ((p["a0"] + p["kP"] * P[i] - V - A[i]) / p["tau_A"])
        A[i + 1] = max(A[i + 1], 0.0)
        D[i + 1] = D[i] + dt * ((D_target - D[i]) / p["tau_D"])
        M[i + 1] = M[i] + dt * (p["kM"] * D[i] - CL[i] * M[i])
        if crossed is None and M[i + 1] > p["Mstar"]:
            crossed = float(t[i + 1])
    P[-1] = (p["N0"] + (p["kAgit"] if M[-1] > p["Mstar"] else 0.0)) * (1 + p["g"] * A[-1])
    # dose saturates at Dmax once the loop runs away, so cumulative dose over the
    # whole record is uninformative. What matters clinically is how long the
    # patient stays below the neurotoxic threshold, and the dose needed up to
    # that point.
    k = n - 1 if crossed is None else int(crossed / dt)
    return {"t": t, "A": A, "D": D, "M": M, "P": P, "cross": crossed,
            "auc_dose": float(np.trapezoid(D, t)),
            "dose_to_cross": float(np.trapezoid(D[:k + 1], t[:k + 1])),
            "mean_dose_pre": float(D[:k + 1].mean()),
            "peak_dose": float(D.max()),
            "saturated": bool(D.max() >= P0["Dmax"] - 1e-6)}


def main():
    res = {"seed": SEED, "parameters": P0, "t_end": T_END, "dt": DT}
    HRS = 24.0

    base = run(V=0.0)
    inter = run(V=0.35)
    res["baseline"] = {"cross_day": base["cross"],
                       "dose_to_cross": round(base["dose_to_cross"], 3),
                       "mean_dose_pre": round(base["mean_dose_pre"], 3)}
    res["intervention"] = {"V": 0.35, "cross_day": inter["cross"],
                           "dose_to_cross": round(inter["dose_to_cross"], 3),
                           "mean_dose_pre": round(inter["mean_dose_pre"], 3),
                           "delay_hours": round((inter["cross"] - base["cross"]) * HRS, 1),
                           "mean_dose_change": round(
                               inter["mean_dose_pre"] / base["mean_dose_pre"] - 1, 4)}
    print("baseline           : threshold at day %.2f, mean pre-threshold dose %.2f"
          % (base["cross"], base["mean_dose_pre"]))
    print("modest damping     : threshold at day %.2f (+%.1f h), mean dose %.2f (%+.0f%%)"
          % (inter["cross"], res["intervention"]["delay_hours"],
             inter["mean_dose_pre"], 100 * res["intervention"]["mean_dose_change"]))

    # ---- can damping prevent the crossing, or only postpone it?
    Vs = np.linspace(0.0, 3.0, 301)
    cross = []
    for V in Vs:
        r = run(V=float(V))
        cross.append(r["cross"] if r["cross"] else None)
    res["sweep"] = {"V": Vs.tolist(), "cross_day": cross}
    res["prevented_at_any_V"] = any(c is None for c in cross)
    finite = [c for c in cross if c is not None]
    res["max_cross_day"] = round(max(finite), 3)
    res["max_delay_hours"] = round((max(finite) - base["cross"]) * HRS, 1)
    print("\nprevention at any damping : %s"
          % ("yes" if res["prevented_at_any_V"] else "NO"))
    print("latest achievable crossing: day %.2f, a ceiling of +%.1f h"
          % (res["max_cross_day"], res["max_delay_hours"]))

    # ---- removing the affective loop entirely, as an upper bound
    no_loop = run(V=0.0, p={"g": 0.0})
    res["no_affective_loop"] = {"cross_day": round(no_loop["cross"], 3),
                                "mean_dose_pre": round(no_loop["mean_dose_pre"], 3)}
    print("affective loop removed    : threshold at day %.2f, mean dose %.2f"
          % (no_loop["cross"], no_loop["mean_dose_pre"]))

    # ---- does the direction hold across the assumed gain?
    res["gain_sweep"] = {}
    print("\n%-6s %12s %14s %12s" % ("g", "base (d)", "damped (d)", "delay (h)"))
    for g in (0.4, 0.6, 0.8, 1.0, 1.2):
        b = run(V=0.0, p={"g": g})
        iv = run(V=0.35, p={"g": g})
        d = round((iv["cross"] - b["cross"]) * HRS, 1)
        res["gain_sweep"]["%.1f" % g] = {
            "baseline_cross": round(b["cross"], 3),
            "intervention_cross": round(iv["cross"], 3), "delay_hours": d,
            "mean_dose_change": round(iv["mean_dose_pre"] / b["mean_dose_pre"] - 1, 4)}
        print("%-6.1f %12.2f %14.2f %12.1f" % (g, b["cross"], iv["cross"], d))
    res["delay_positive_for_all_gains"] = all(
        v["delay_hours"] > 0 for v in res["gain_sweep"].values())
    print("\ndelay positive across every assumed gain: %s"
          % res["delay_positive_for_all_gains"])

    # ---- one-at-a-time sensitivity: every parameter scaled by 0.75 and 1.25
    res["sensitivity"] = sensitivity()

    # ---- what a reader needs to reproduce the numbers
    res["reproduction"] = {
        "integration": "forward Euler, dt = %.3f day, t = 0 to %.0f days" % (DT, T_END),
        "initial_conditions": {"A": "a0", "D": 0.0, "M": 0.0},
        "threshold": "first time M exceeds Mstar; after that N = N0 + kAgit",
        "dose_rule": "dD/dt = (min(P, Dmax) - D)/tau_D",
        "modest_damping_V": 0.35, "maximal_damping_V_in_figure": 1.5,
        "sweep_V": [0.0, 3.0, 301]}

    json.dump(res, open("escalation_results.json", "w"), indent=1)
    print("\nwrote escalation_results.json")


SENS_PARAMS = ["g", "a0", "kP", "tau_A", "tau_D", "kM", "CL0", "tau_CL", "Mstar",
               "kAgit", "Dmax"]


def sensitivity(factors=(0.75, 1.25), V_mod=0.35, Vs=np.linspace(0.0, 3.0, 61)):
    """Scale each parameter in turn and re-derive the three reported quantities."""
    HRS = 24.0
    out = []
    print("\n%-7s %6s %10s %10s %10s %10s" % ("param", "x", "base (d)", "delay(h)",
                                             "ceiling(h)", "prevented"))
    for name in SENS_PARAMS:
        for f in factors:
            p = {name: P0[name] * f}
            b = run(V=0.0, p=p)
            if b["cross"] is None:
                row = {"param": name, "factor": f, "baseline_cross_day": None,
                       "delay_hours": None, "ceiling_hours": None, "prevented": True,
                       "note": "threshold not reached within %.0f days" % T_END}
            else:
                iv = run(V=V_mod, p=p)
                cs = [run(V=float(v), p=p)["cross"] for v in Vs]
                fin = [c for c in cs if c is not None]
                row = {"param": name, "factor": f,
                       "baseline_cross_day": round(b["cross"], 3),
                       "delay_hours": (round((iv["cross"] - b["cross"]) * HRS, 1)
                                       if iv["cross"] is not None else None),
                       "ceiling_hours": round((max(fin) - b["cross"]) * HRS, 1) if fin else None,
                       "prevented": any(c is None for c in cs)}
            out.append(row)
            print("%-7s %6.2f %10s %10s %10s %10s"
                  % (name, f, row["baseline_cross_day"], row["delay_hours"],
                     row["ceiling_hours"], row["prevented"]))
    return out


if __name__ == "__main__":
    main()
