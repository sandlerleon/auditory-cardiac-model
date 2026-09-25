# The auditory–cardiac channel in the last days of life

Leon Sandler, Independent Researcher — sandler.leon@gmail.com
ORCID [0009-0007-4584-808X](https://orcid.org/0009-0007-4584-808X)

Model and manuscript for *"The auditory–cardiac channel in the last days of life:
a neurovisceral hypothesis for modulating opioid escalation,"* submitted to
**Medical Hypotheses**.

> **This is a hypothesis paper.** No patient was studied and no data were
> collected. Nothing here is clinical advice, and nothing here should delay,
> reduce or substitute for established palliative care including adequate
> analgesia. The proposal is adjunctive; any reduction in opioid requirement is
> an outcome to be observed, never a target to pursue.

## The problem

In the last days of life, opioid infusion is commonly titrated against
observed signs of distress, but those signs may reflect nociception, autonomic
arousal, delirium or opioid-related neurotoxicity. Where clearance of active
metabolites declines, bedside signs alone may not distinguish too little drug
from too much, and a common, humane response is to give more.

## The hypothesis

Part of that escalation is driven by a self-reinforcing loop between autonomic
arousal and perceived distress rather than by nociception alone — and the loop
may be reachable through hearing, since auditory processing appears to persist
when other channels have failed. Anatomical connection is not evidence of a
therapeutic effect: whether auditory input changes autonomic state in dying
patients, and whether that changes opioid requirement, are both untested.

## The model

```
P = N(1 + gA),  N = N₀ + k_agit·H(M − M*)   perceived pain; agitation after M* is crossed
dA/dt = (a₀ + k_P·P − V − A)/τ_A, A ≥ 0      autonomic arousal, damped by V
dD/dt = (min(P, D_max) − D)/τ_D              dose titrated toward perceived pain
dM/dt = k_M·D − CL(t)·M                      metabolite accumulation
CL(t) = CL₀·exp(−t/τ_CL)                     declining clearance
```

Initial conditions A(0) = a₀, D(0) = 0, M(0) = 0; forward Euler, dt = 0.002 day,
10 days. `M*` is an **illustrative model threshold**, not a neurotoxic
concentration. The manuscript's Table 1 lists every parameter value and unit. **Every parameter is illustrative.** This is not a pharmacokinetic
simulation of morphine and no output is a predicted dose or survival time.

## What the model says

| | result |
|---|---|
| Threshold crossed, no intervention | day 1.04 |
| Modest damping | day 1.30 — **+6.2 hours**, mean pre-threshold dose −11% |
| Maximal damping | **ceiling +34.8 hours** |
| Prevention at any damping strength | **none** |
| Sensitivity (each of 11 parameters ×0.75 / ×1.25) | delay 3.5–10.7 h, ceiling 21.0–50.7 h, prevention in no run |

The benefit is bounded and the bound is hours to a little over a day. That is
the most useful thing the model says: an intervention that buys lucid hours is
worth having; one sold as a way to avoid opioid escalation would be wrong and
dangerous.

## What is known versus proposed

The paper assigns every link an explicit status. Two are worth flagging here
because they are routinely conflated in popular accounts:

- **Auditory responses persist in dying patients** — demonstrated, with
  tone-based ERPs recorded in hospice patients within hours of death.
- **Semantic processing survives unresponsiveness** — demonstrated, but in
  disorders of consciousness, not in dying patients.
- **Semantic processing persists in actively dying patients** — **untested.**
  No published study has shown this. It is the paper's primary prediction, not
  its premise.

The molecular basis of opioid-induced neurotoxicity is also contested: M3G was
proposed as the neuroexcitatory agent and then reported non-neurotoxic by the
same group.

## Contents

```
code/
  escalation_model.py    the loop model and its sweeps -> escalation_results.json
  make_figures.py        both figures
  build_manuscript.py    manuscript, every number read from the JSON
  build_cover_letter.py  cover letter
  audit_manuscript.py    numeric, reference and safety-language checks
  harvest_refs.py        Crossref verification of every reference
  add_refs_v2.py         revision-2 reference additions, each checked against Crossref
figures/                 two figures, 300 dpi
manuscript/              manuscript and cover letter
```

## Reproducing

```bash
pip install -r requirements.txt
python code/escalation_model.py   # model -> escalation_results.json
python code/make_figures.py       # both figures
python code/build_manuscript.py   # manuscript
python code/audit_manuscript.py   # checks the document against the model
```

The audit re-checks the headline and sensitivity numbers, verifies every reference is cited and
every citation listed, and scans for language that would overclaim — text
suggesting the intervention replaces opioid, eliminates the need for it, or
prevents the neurotoxic threshold.

All 21 references were verified against their sources (20 against Crossref; the
NICE NG31 guideline has no DOI and is cited by its URL).

## Citation

Concept DOIs, which always resolve to the latest version:

- Code and model: [10.5281/zenodo.22860430](https://doi.org/10.5281/zenodo.22860430)
- Manuscript: [10.5281/zenodo.22860432](https://doi.org/10.5281/zenodo.22860432)

## License

Code MIT (`LICENSE`); manuscript text and figures CC BY 4.0.
