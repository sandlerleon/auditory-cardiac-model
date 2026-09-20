# The auditory–cardiac channel in the last days of life

Leon Sandler, Independent Researcher — sandler.leon@gmail.com
ORCID [0009-0007-4584-808X](https://orcid.org/0009-0007-4584-808X)

Model and manuscript for *"The auditory–cardiac channel in the last days of life:
a neurovisceral hypothesis for limiting opioid escalation,"* submitted to
**Medical Hypotheses**.

> **This is a hypothesis paper.** No patient was studied and no data were
> collected. Nothing here is clinical advice, and nothing here should delay,
> reduce or substitute for established palliative care including adequate
> analgesia. The proposal is adjunctive; any reduction in opioid requirement is
> an outcome to be observed, never a target to pursue.

## The problem

In the last days of life, opioid infusion is titrated against observed distress.
But the signs being titrated against — restlessness, grimacing, tachycardia —
are also the signs of opioid-induced neurotoxicity as metabolites accumulate in
a patient whose clearance is failing. The bedside cannot distinguish too little
drug from too much, and the humane default is to give more. The cost is that
patients become unreachable days before they die.

## The hypothesis

Part of that escalation is driven by a self-reinforcing loop between autonomic
arousal and perceived pain rather than by nociception alone — and the loop is
reachable through the subcortical auditory pathway, which stays functional when
other sensory channels have failed.

## The model

```
P = N(1 + gA)                          perceived pain
dA/dt = (a₀ + k_P·P − V − A)/τ_A       autonomic arousal, damped by V
dM/dt = k_M·D − CL(t)·M                metabolite accumulation
CL(t) = CL₀·exp(−t/τ_CL)               clearance falls as death approaches
```

Once `M` crosses a threshold an agitation term is added to `N`, which closes the
loop. **Every parameter is illustrative.** This is not a pharmacokinetic
simulation of morphine and no output is a predicted dose or survival time.

## What the model says

| | result |
|---|---|
| Threshold crossed, no intervention | day 1.04 |
| Modest damping | day 1.30 — **+6.2 hours**, mean pre-threshold dose −11% |
| Maximal damping | **ceiling +34.8 hours** |
| Prevention at any damping strength | **none** |

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

The audit re-checks five headline numbers, verifies every reference is cited and
every citation listed, and scans for language that would overclaim — text
suggesting the intervention replaces opioid, eliminates the need for it, or
prevents the neurotoxic threshold.

All 17 references were verified against Crossref.

## Citation

Concept DOIs, which always resolve to the latest version:

- Code and model: [10.5281/zenodo.22860430](https://doi.org/10.5281/zenodo.22860430)
- Manuscript: [10.5281/zenodo.22860432](https://doi.org/10.5281/zenodo.22860432)

## License

Code MIT (`LICENSE`); manuscript text and figures CC BY 4.0.
