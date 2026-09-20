# -*- coding: utf-8 -*-
"""Build the Medical Hypotheses manuscript.

Every number is read from escalation_results.json, and every reference from the
Crossref verification pass, so neither can drift from its source.

Three things the source draft asserted that the literature does not support have
been reworked rather than repeated:

  * N400 semantic responses have NOT been recorded in actively dying patients.
    Tone-based auditory ERPs have (Blundon 2020); N400 has been recorded in
    disorders of consciousness (Steppacher 2013). The semantic claim in dying
    patients is this paper's primary testable prediction, not its premise.
  * M3G neurotoxicity is contested, and the refutation comes from the same group
    that proposed it.
  * Music therapy and hypnotherapy at the end of life already exist and have
    been reviewed; the novelty claim has to be narrower than the draft's.

Added because the subject demands it: an explicit harm section and an ethical
statement. The draft had neither, in a paper about reducing opioid dose in
dying patients.

    python build_manuscript.py
"""
import io
import json
import os

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = r"C:\Users\Leon\Downloads\Medical Hypotheses"
R = json.load(io.open(os.path.join(HERE, "escalation_results.json"), encoding="utf-8"))
REFS = json.load(io.open(os.path.join(HERE, "_refs_final.json"), encoding="utf-8"))

BASE = R["baseline"]
INT = R["intervention"]
P = R["parameters"]

doc = Document()
st = doc.styles["Normal"]
st.font.name = "Times New Roman"
st.font.size = Pt(11)
st.paragraph_format.space_after = Pt(6)
st.paragraph_format.line_spacing = 2.0

for s in doc.sections:
    s.left_margin = s.right_margin = Inches(1.0)
    s.top_margin = s.bottom_margin = Inches(1.0)
    sectPr = s._sectPr
    ln = OxmlElement("w:lnNumType")
    ln.set(qn("w:countBy"), "1")
    ln.set(qn("w:start"), "1")
    ln.set(qn("w:restart"), "continuous")
    ln.set(qn("w:distance"), "360")
    anchor = sectPr.find(qn("w:pgMar"))
    if anchor is None:
        anchor = sectPr.find(qn("w:pgSz"))
    if anchor is None:
        sectPr.insert(0, ln)
    else:
        anchor.addnext(ln)

# citation numbering, by order of first appearance
ORDER = []


def C(*tags):
    nums = []
    for t in tags:
        if t not in ORDER:
            ORDER.append(t)
        nums.append(ORDER.index(t) + 1)
    nums.sort()
    return "[%s]" % ",".join(str(n) for n in nums)


def H(text, size=12, before=14):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.5
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(size)
    return p


def Pp(text, indent=False, size=11, spacing=2.0, italic=False):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = spacing
    if indent:
        p.paragraph_format.first_line_indent = Inches(0.3)
    r = p.add_run(text)
    r.italic = italic
    r.font.size = Pt(size)
    return p


def BULLET(text, bold_lead=None):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.line_spacing = 1.5
    if bold_lead:
        r = p.add_run(bold_lead)
        r.bold = True
        r.font.size = Pt(11)
    r = p.add_run(text)
    r.font.size = Pt(11)
    return p


def CAP(text):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.space_after = Pt(12)
    r = p.add_run(text)
    r.font.size = Pt(9.5)
    return p


def FIG(name, width=6.2):
    path = os.path.join(HERE, name)
    if os.path.exists(path):
        doc.add_picture(path, width=Inches(width))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER


def TBL(headers, rows, fs=9):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    for i, h in enumerate(headers):
        c = t.rows[0].cells[i]
        c.text = ""
        c.paragraphs[0].paragraph_format.line_spacing = 1.0
        r = c.paragraphs[0].add_run(h)
        r.bold = True
        r.font.size = Pt(fs)
    for row in rows:
        cells = t.add_row().cells
        for i, v in enumerate(row):
            cells[i].text = ""
            pp = cells[i].paragraphs[0]
            pp.paragraph_format.line_spacing = 1.0
            pp.paragraph_format.space_after = Pt(1)
            pp.add_run(str(v)).font.size = Pt(fs)
    return t


# ==================================================================== FRONT
p = doc.add_paragraph()
p.paragraph_format.line_spacing = 1.5
r = p.add_run("The auditory\u2013cardiac channel in the last days of life: a "
              "neurovisceral hypothesis for limiting opioid escalation")
r.bold = True
r.font.size = Pt(14)

Pp("Leon Sandler", spacing=1.5)
Pp("Independent Researcher, Northbrook, Illinois, United States", spacing=1.5, size=10.5)
Pp("ORCID: 0009-0007-4584-808X \u00b7 Correspondence: sandler.leon@gmail.com",
   spacing=1.5, size=10.5)

H("Abstract")
ABSTRACT = (
    "In the last days of life, continuous opioid infusion is titrated against "
    "observed distress. Because renal and hepatic clearance fall as death "
    "approaches, escalation and accumulation interact: metabolite accumulation "
    "can produce agitation, agitation is read as pain, and pain prompts further "
    "escalation. The endpoint is often a depth of sedation that ends "
    "communication between the patient and those present, days before death. We "
    "propose that part of this escalation is driven not by nociception but by a "
    "self-reinforcing loop between autonomic arousal and perceived pain, and "
    "that the loop is accessible through a sensory channel that remains "
    "functional when others have failed. Auditory event-related potentials "
    "persist in actively dying patients, and the subcortical auditory pathway "
    "reaches the central autonomic network without requiring cortical "
    "participation. We set out the anatomy, state explicitly which links are "
    "demonstrated and which are assumed, and analyse a minimal model of the "
    "escalation loop. The model indicates that damping autonomic arousal "
    "postpones rather than prevents metabolite accumulation, with a bounded "
    "benefit. We give five falsifiable predictions, the conditions under which "
    "the proposal would cause harm, and the reasons a negative trial would be "
    "informative. No patient data were collected and nothing here is a "
    "treatment recommendation.")
Pp(ABSTRACT, spacing=1.5)

Pp("Keywords: palliative care; end-of-life care; opioid escalation; auditory "
   "event-related potentials; neurovisceral integration; heart rate "
   "variability; clinical hypnosis; terminal agitation",
   spacing=1.5, size=10.5)

# ================================================================= SECTION 1
H("1. The problem")
Pp("Care of the dying is, pharmacologically, a titration problem. Continuous "
   "subcutaneous or intravenous opioid is adjusted against observed signs of "
   "distress: grimacing, restlessness, tachypnoea, tachycardia. National "
   "guidance is explicit that dose should follow assessed need %s, and opioids "
   "are the best-evidenced treatment for refractory breathlessness at the end "
   "of life %s. None of this is in question here."
   % (C("nice2016"), C("barnes2016")))
Pp("The difficulty is that the signs being titrated against are not specific to "
   "nociception, and the patient can no longer disambiguate them. As organ "
   "function declines, opioid metabolites accumulate. Opioid-induced "
   "neurotoxicity \u2014 myoclonus, hyperalgesia, delirium, terminal agitation "
   "\u2014 is a recognised complication in palliative medicine %s, and its "
   "presentation overlaps almost completely with the presentation of "
   "under-treated pain. A clinician watching a restless, grimacing patient "
   "cannot tell from the bedside whether the dose is too low or too high, and "
   "the default, humane response is to increase it."
   % C("oin2026"), indent=True)
Pp("We note at once that the mechanism usually invoked for this neurotoxicity is "
   "contested. Morphine-3-glucuronide was proposed as the neuroexcitatory agent "
   "%s, but the same group subsequently reported that M3G is not neurotoxic to "
   "primary hippocampal or cerebellar granule neurones %s. The clinical "
   "syndrome is well described; its molecular basis is not settled, and we "
   "therefore treat metabolite accumulation as a phenomenological driver rather "
   "than asserting a specific mediator."
   % (C("smith2000"), C("m3g_refute")), indent=True)
Pp("The cost of the resulting escalation is not primarily physiological. It is "
   "that the patient becomes unreachable. Families describe losing the person "
   "some days before the death, and clinicians are left balancing comfort "
   "against presence with no instrument that measures the trade-off.", indent=True)

# ================================================================= SECTION 2
H("2. The hypothesis")
p = doc.add_paragraph()
p.paragraph_format.left_indent = Inches(0.4)
p.paragraph_format.right_indent = Inches(0.4)
p.paragraph_format.line_spacing = 1.5
r = p.add_run("A component of terminal opioid escalation is driven by a "
              "self-reinforcing loop between autonomic arousal and perceived "
              "pain, rather than by nociceptive input alone. Because the "
              "subcortical auditory pathway remains functional when other "
              "sensory channels have failed, structured auditory input can "
              "reach the central autonomic network directly and damp that "
              "loop, postponing the point at which accumulation forces a choice "
              "between comfort and consciousness.")
r.bold = True
r.font.size = Pt(11)
Pp("Two claims are separable here and should be judged separately. The first is "
   "that an arousal\u2013pain loop contributes materially to dose escalation in "
   "the last days. The second is that the auditory channel is a usable point of "
   "entry to it. The first could be true and the second false.", indent=True)

# ================================================================= SECTION 3
H("3. Why the auditory channel, and what has actually been shown")
Pp("Acoustic signals reach the brainstem through the cochlear nuclei, superior "
   "olivary complex and inferior colliculus before any thalamocortical routing "
   "%s. These are among the most metabolically economical and phylogenetically "
   "conserved structures in the central nervous system, and processing along "
   "this path does not require cortical participation." % C("kraus2010"))
Pp("The evidentiary position must be stated precisely, because the source "
   "literature is often summarised more strongly than it supports. Two distinct "
   "findings are relevant and they are not the same finding.", indent=True)
BULLET("Auditory event-related potentials to tone sequences persist in actively "
       "dying hospice patients, in some cases within hours of death, and "
       "resemble those of healthy controls %s. This establishes that the "
       "auditory system is still processing structured acoustic input at the end "
       "of life. It does not establish that words are being understood."
       % C("blundon2020"), bold_lead="Hearing persists. ")
BULLET("The N400, an index of semantic mismatch, has been recorded in patients "
       "with disorders of consciousness, where its presence predicts later "
       "recovery %s. This establishes that automatic semantic processing can "
       "survive profound unresponsiveness. It was not measured in dying "
       "patients, and its absence in many such patients is precisely what makes "
       "it prognostic." % C("steppacher2013"),
       bold_lead="Semantic processing can survive unresponsiveness. ")
Pp("No published study has demonstrated semantic processing in actively dying "
   "patients. The proposition that the dying brain decodes the meaning of what "
   "is said to it is therefore a hypothesis, not a premise, and we treat it as "
   "this paper's primary experimental prediction (Section 7). Framing it as "
   "established \u2014 as popular accounts of \u2018hearing is the last sense to "
   "go\u2019 routinely do \u2014 would put the weight of the argument on a "
   "claim the literature has not yet tested.", indent=True)

# ================================================================= SECTION 4
H("4. From acoustic input to autonomic state")
Pp("The route from processed sound to cardiac output runs through the central "
   "autonomic network. Under the neurovisceral integration account, prefrontal "
   "and limbic structures exert inhibitory control over sympathoexcitatory "
   "circuits, with vagally mediated heart rate variability as the accessible "
   "index of that control %s. Afferent traffic from baroreceptors returns "
   "through the nucleus tractus solitarius to the insular cortex, which "
   "supports interoceptive representation of bodily state %s. The loop is "
   "bidirectional: a steady cardiac rhythm is not merely an output of calm but "
   "an input to it." % (C("thayer2009"), C("critchley2004")))
Pp("Where this becomes relevant to analgesia is the separability of pain's "
   "sensory and affective dimensions. Hypnotic suggestion directed at "
   "unpleasantness rather than intensity alters activity in the anterior "
   "cingulate cortex without corresponding change in primary somatosensory "
   "cortex %s \u2014 the affective component can be moved while the sensory "
   "component is left intact. Meta-analysis supports a moderate to large "
   "analgesic effect of hypnotic procedures %s, and the clinical literature on "
   "hypnotic approaches to chronic pain is consistent with a mechanism acting "
   "on pain-related distress rather than on transduction %s."
   % (C("rainville1997"), C("montgomery2000"), C("jensen2014")), indent=True)
FIG("figure1_pathway.png")
CAP("Figure 1. The proposed auditory\u2013cardiac pathway. Grey boxes are "
    "established anatomy; green marks the two steps for which there is direct "
    "evidence in unresponsive or dying patients; blue marks the proposed points "
    "of intervention and measurement. The red limb closes the loop: the "
    "interoceptive reading of cardiac state feeds back into threat appraisal.")

# ================================================================= SECTION 5
H("5. A minimal model of the escalation loop")
Pp("To ask whether the proposed loop can produce the clinical pattern, and what "
   "damping it would be worth, we analyse a deliberately minimal system. "
   "Perceived pain P is nociceptive drive N amplified by autonomic arousal A "
   "with gain g; arousal is driven by perceived pain and damped by a term V "
   "standing for the intervention; dose follows perceived pain; metabolite M "
   "accumulates as clearance declines exponentially; and once M crosses a "
   "threshold an agitation term is added to N, which is what closes the loop.")
Pp("P = N(1 + gA);  dA/dt = (a\u2080 + k_P P \u2212 V \u2212 A)/\u03c4_A;  "
   "dM/dt = k_M D \u2212 CL(t)M;  CL(t) = CL\u2080 exp(\u2212t/\u03c4_CL)",
   italic=True, spacing=1.5)
Pp("Every parameter is illustrative. None is fitted to patient data, this is not "
   "a pharmacokinetic simulation of morphine, and no quantity below should be "
   "read as a predicted dose or survival time. The model is used only to ask "
   "what class of behaviour the loop can produce and what would have to be "
   "measured to refute it. Results are therefore reported as relative timings.",
   indent=True)
Pp("Three results follow. First, the loop is capable of producing the clinical "
   "pattern: with the assumed parameters the threshold is crossed on day "
   "%.2f, after which dose saturates. Second, damping arousal postpones that "
   "crossing \u2014 a modest damping term delays it by %.1f hours and lowers "
   "mean pre-threshold dose by %.0f%%. Third, and most importantly, damping "
   "never prevents the crossing at any strength. The delay saturates at a "
   "ceiling of %.1f hours, reached when arousal is fully suppressed; removing "
   "the affective loop altogether gives essentially the same answer (day %.2f). "
   "The benefit this hypothesis can claim is bounded, and the bound is hours to "
   "a little over a day."
   % (BASE["cross_day"], INT["delay_hours"], -100 * INT["mean_dose_change"],
      R["max_delay_hours"], R["no_affective_loop"]["cross_day"]), indent=True)
FIG("figure2_model.png")
CAP("Figure 2. Behaviour of the minimal loop model. (A) Accumulated metabolite "
    "against time for no intervention, modest damping and maximal damping; "
    "circles mark the threshold crossing. (B) Delay in reaching the threshold as "
    "a function of damping strength. The delay saturates at %.1f hours and no "
    "damping strength prevents the crossing. Parameters are illustrative "
    "throughout; the figure shows the shape of the result, not a prediction for "
    "any patient." % R["max_delay_hours"])
Pp("That the modelled benefit is bounded is not a weakness of the proposal but "
   "the most useful thing the model says. An intervention that postpones the "
   "neurotoxic threshold by hours is worth having if those hours are lucid and "
   "the patient's family is present. An intervention sold as a way to avoid "
   "opioid escalation would be both wrong and dangerous.", indent=True)

# ================================================================= SECTION 6
H("6. Evidence status of each link")
Pp("The argument above chains together claims of very different evidentiary "
   "standing. Table 1 assigns each a status rather than folding them into a "
   "single judgement about the hypothesis, so that a reader can locate the weak "
   "links directly.")
TBL(["Link", "Status", "Basis"],
    [["Subcortical auditory pathway reaches limbic and autonomic structures "
      "without cortical routing", "Demonstrated", "Established neuroanatomy " + C("kraus2010")],
     ["Auditory ERPs to structured sound persist in actively dying patients",
      "Demonstrated", "Direct measurement in hospice patients " + C("blundon2020")],
     ["Automatic semantic processing can survive profound unresponsiveness",
      "Demonstrated", "N400 in disorders of consciousness " + C("steppacher2013")],
     ["Semantic processing persists in actively dying patients",
      "Untested", "Not measured in this population; prediction P1"],
     ["Vagally mediated HRV indexes central autonomic control",
      "Demonstrated", "Neurovisceral integration " + C("thayer2009")],
     ["Hypnotic suggestion separates pain affect from pain sensation",
      "Demonstrated", "ACC dissociation in healthy volunteers " + C("rainville1997")],
     ["Hypnotic procedures reduce analgesic requirement",
      "Supported", "Randomised evidence in conscious sedation " + C("faymonville1997")
      + "; meta-analysis " + C("montgomery2000")],
     ["Arousal amplifies perceived pain via central sensitisation",
      "Supported", "Mechanistic review " + C("woolf2011")],
     ["An arousal-pain loop drives a material share of terminal escalation",
      "Proposed", "This paper; prediction P2"],
     ["Auditory input can damp that loop in dying patients",
      "Proposed", "This paper; prediction P3"],
     ["Damping postpones rather than prevents metabolite accumulation",
      "Model result", "Section 5; conditional on assumed parameters"],
     ["A specific metabolite mediates opioid-induced neurotoxicity",
      "Contested", "Proposed " + C("smith2000") + ", refuted by the same group "
      + C("m3g_refute")]])
CAP("Table 1. Status of each link in the chain. Rows 4, 9 and 10 are the load "
    "bearing untested claims and are the targets of the experimental programme "
    "in Section 7.")

# ================================================================= SECTION 7
H("7. Predictions and falsification")
Pp("The hypothesis is refuted by any of the following.")
for tag, body in [
 ("P1. Semantic processing in dying patients. ",
  "N400 responses to semantic mismatch, recorded in actively dying patients "
  "using the paradigm already validated in disorders of consciousness, should "
  "be present in a substantial minority. If they are absent in essentially all "
  "patients while tone-based responses persist, the verbal content of the "
  "intervention is irrelevant and only prosody and familiarity could matter."),
 ("P2. An arousal component to escalation. ",
  "Among patients matched for disease, site and nociceptive burden, those with "
  "lower vagally mediated heart rate variability should require larger opioid "
  "dose increments over the same interval. If dose trajectory is independent of "
  "autonomic state, the loop does not contribute materially and the proposal "
  "fails at its foundation."),
 ("P3. Auditory input moves autonomic state. ",
  "Structured verbal pacing delivered to unresponsive dying patients should "
  "produce a measurable increase in high-frequency heart rate variability "
  "relative to matched acoustic control, within minutes. This is the most "
  "directly testable prediction and requires no change to any treatment."),
 ("P4. Dose trajectory. ",
  "In a randomised comparison against an attention-matched control, the "
  "intervention arm should show a lower rate of dose escalation over 48 hours "
  "without any increase in observed distress scores. The model's bounded "
  "benefit means the expected effect is small; a trial powered for a large "
  "effect would fail for the wrong reason."),
 ("P5. Preserved responsiveness. ",
  "If the mechanism operates, the intervention arm should retain measurable "
  "responsiveness longer. This is the outcome that matters to families and the "
  "one the hypothesis exists to serve, and it should be reported whatever the "
  "dose result."),
]:
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_before = Pt(5)
    r = p.add_run(tag)
    r.bold = True
    r.font.size = Pt(11)
    r = p.add_run(body)
    r.font.size = Pt(11)
Pp("P3 is the decisive early test. It is non-invasive, requires no protocol "
   "deviation, and would be informative whichever way it resolved.", indent=True)

# ================================================================= SECTION 8
H("8. How this proposal could cause harm")
Pp("A hypothesis whose practical implication is a smaller opioid dose in dying "
   "patients carries a specific and serious risk, and enumerating it is part of "
   "the proposal rather than a caveat appended to it.")
for lead, body in [
 ("Under-treatment of pain. ",
  "The principal danger is that the framework is read as a reason to withhold "
  "or delay analgesia in a patient who cannot report pain. Nothing here "
  "supports that. The proposal is adjunctive: the opioid is titrated to comfort "
  "exactly as it would otherwise be, and any reduction in requirement is an "
  "observed outcome, never a target to be pursued."),
 ("Misattribution of distress. ",
  "If a patient appears calmer because arousal has been damped while "
  "nociception is unchanged, observed distress scores could fall without the "
  "underlying pain changing. This is the failure mode most likely to cause "
  "harm and is the reason P4 specifies distress scores as a safety endpoint "
  "rather than an efficacy one."),
 ("Burden on the dying and on families. ",
  "Continuous verbal intervention at the bedside is not neutral. It occupies "
  "the room, may displace silence that families need, and may be experienced "
  "as intrusive by patients who cannot decline it. Consent cannot be obtained "
  "from an unresponsive patient, and advance preference should govern."),
 ("False reassurance. ",
  "Presenting an unproven adjunct as a way to preserve lucidity risks families "
  "attributing an unavoidable decline to insufficient effort, or declining "
  "adequate analgesia in hope of more time. The bounded benefit in Section 5 "
  "should be communicated as a bound, not as an expectation."),
 ("Displacement of established care. ",
  "Music therapy at the end of life has been systematically reviewed, with "
  "evidence judged insufficient for confident conclusions %s. A new adjunct "
  "with weaker evidence should not compete for the same resources." % C("bradt2014")),
]:
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_before = Pt(5)
    r = p.add_run(lead)
    r.bold = True
    r.font.size = Pt(11)
    r = p.add_run(body)
    r.font.size = Pt(11)

# ================================================================= SECTION 9
H("9. Relation to existing practice")
Pp("Soothing speech, familiar voices and music are already part of good hospice "
   "practice, and hypnotherapy has been delivered to palliative patients for "
   "anxiety %s. The claim here is narrower than 'sound helps'. It is that a "
   "specific, measurable autonomic pathway mediates the effect; that the "
   "relevant outcome is the trajectory of opioid requirement rather than a "
   "comfort score; and that the mechanism predicts a bounded, quantifiable "
   "benefit which can be tested and found absent. Existing practice is "
   "compatible with the hypothesis but does not test it, because it has not "
   "been paired with autonomic measurement or dose trajectory as endpoints."
   % C("plaskota2012"))

H("10. Ethical statement")
Pp("This is a conceptual hypothesis paper. No patient was studied, no data were "
   "collected, and no intervention described here has been tested in any "
   "population. Nothing in it constitutes clinical advice or a treatment "
   "recommendation, and nothing in it should delay, reduce or substitute for "
   "established palliative care, including adequate analgesia. Decisions about "
   "opioid dosing in dying patients are clinical judgements made at the bedside "
   "by those responsible for the patient. Any prospective evaluation would "
   "require research ethics approval with particular attention to consent by "
   "proxy, to the right to decline, and to safety monitoring for under-treated "
   "pain.")

# ============================================================== DECLARATIONS
H("Declarations")
Pp("Funding. This work received no external funding.")
Pp("Competing interests. The author declares no competing interests.")
Pp("Data availability. The model implementation, parameter set and figure "
   "generators are openly available at %s and archived at https://doi.org/%s. "
   "Running escalation_model.py followed by make_figures.py reproduces every "
   "number and figure. This manuscript is deposited at "
   "https://doi.org/10.5281/zenodo.22860432. Both are concept DOIs and resolve "
   "to the current version. No patient data were generated or analysed."
   % ("https://github.com/sandlerleon/auditory-cardiac-model", "10.5281/zenodo.22860430"))
Pp("Use of generative artificial intelligence. During the preparation of this "
   "work the author used Claude (Anthropic) to assist with literature synthesis, "
   "model implementation and drafting. The author reviewed and edited all "
   "content, verified every cited reference against Crossref, and takes full "
   "responsibility for the publication. No generative AI tool is listed as an "
   "author and none was used to produce or alter data.")

# ================================================================ REFERENCES
H("References")
for i, tag in enumerate(ORDER, 1):
    v = REFS[tag]
    au = ", ".join(v["authors"][:6]) + (", et al." if len(v["authors"]) > 6 else "")
    vol = (" %s" % v["volume"]) if v.get("volume") else ""
    pg = (":%s" % v["page"]) if v.get("page") else ""
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.left_indent = Inches(0.35)
    p.paragraph_format.first_line_indent = Inches(-0.35)
    r = p.add_run("[%d] %s. %s. %s %d;%s%s. https://doi.org/%s"
                  % (i, au, v["title"], v["journal"], v["year"], vol.strip(), pg,
                     v["doi"]))
    r.font.size = Pt(9.5)

if not os.path.isdir(OUT):
    os.makedirs(OUT)
path = os.path.join(OUT, "Auditory_Cardiac_Channel_MedicalHypotheses.docx")
doc.save(path)

words = sum(len(p.text.split()) for p in doc.paragraphs)
print("abstract words : %d" % len(ABSTRACT.split()))
print("total words    : %d" % words)
print("references     : %d (cited, in order of appearance)" % len(ORDER))
print("unused refs    : %s" % (sorted(set(REFS) - set(ORDER)) or "none"))
print("saved          : %s" % path)
