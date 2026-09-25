# -*- coding: utf-8 -*-
"""Revision 2 reference changes, each verified against Crossref at run time.

  * adds LeDoux 2000, Koelsch 2014 and Benarroch 1993 for the auditory-to-autonomic
    anatomy (replacing Kraus 2010, which is about music training and too indirect);
  * adds the ESC/NASPE Task Force 1996 and Laborde 2017 for HRV measurement limits;
  * adds the NICE NG31 guideline itself (no DOI), so 'national guidance' cites the
    guideline and not only the Clinical Medicine summary of it;
  * gives the two Cochrane reviews proper year/issue/article-number metadata instead
    of Crossref's '2019' volume artefact.

    python add_refs_v2.py
"""
import io
import json
import os

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, "_refs_final.json")
REFS = json.load(io.open(PATH, encoding="utf-8"))

NEW = {
    "ledoux2000": "10.1146/annurev.neuro.23.1.155",
    "koelsch2014": "10.1038/nrn3666",
    "benarroch1993": "10.1016/S0025-6196(12)62272-1",
    "taskforce1996": "10.1161/01.CIR.93.5.1043",
    "laborde2017": "10.3389/fpsyg.2017.00213",
    # brainstem auditory processing without cortex: the acoustic startle circuit.
    # Koelsch 2014 supports limbic modulation by music, not this claim.
    "koch1999": "10.1016/S0301-0082(98)00098-7",
    # replaces Bradt & Dileo 2014 (CD007169.pub3), which is a WITHDRAWN notice;
    # the 2025 Cochrane record CD016311 is only a protocol
    "bissonnette2024": "10.1136/bmjspcare-2022-003551",
}


def initials(given):
    return "".join(p[0] for p in given.replace("-", " ").replace(".", " ").split() if p)


for tag, doi in NEW.items():
    m = requests.get("https://api.crossref.org/works/" + doi, timeout=30,
                     headers={"User-Agent": "refcheck (mailto:sandler.leon@gmail.com)"}).json()["message"]
    au = ["%s %s" % (a["family"].title() if a["family"].isupper() else a["family"],
                     initials(a.get("given", ""))) for a in m.get("author", []) if "family" in a]
    REFS[tag] = {"authors": au, "title": m["title"][0],
                 "journal": m["container-title"][0].replace("&amp;", "&"),
                 "year": m["issued"]["date-parts"][0][0],
                 "volume": m.get("volume"), "page": m.get("page"), "doi": doi.lower()}

REFS["taskforce1996"]["authors"] = [
    "Task Force of the European Society of Cardiology and the North American Society "
    "of Pacing and Electrophysiology"]
REFS["taskforce1996"]["title"] = ("Heart rate variability: standards of measurement, "
                                  "physiological interpretation and clinical use")
REFS["bissonnette2024"].update({"year": 2024, "volume": "13", "page": "e503-e514"})  # PubMed issue date
REFS["smith2000"]["authors"] = ["Smith MT"]      # PubMed; Crossref drops the middle initial
REFS["laborde2017"]["volume"] = "8"
REFS["laborde2017"]["page"] = "213"

REFS["nice_ng31"] = {
    "authors": ["National Institute for Health and Care Excellence"],
    "title": "Care of dying adults in the last days of life. NICE guideline NG31",
    "journal": "London: NICE", "year": 2015, "volume": None, "page": None, "doi": None,
    "url": "https://www.nice.org.uk/guidance/ng31"}

# Cochrane: Crossref reports the current issue year as 'volume'; cite the version used
REFS["bradt2014"].update({"volume": None, "page": None, "cochrane": "(3):CD007169"})
REFS["barnes2016"].update({"volume": None, "page": None, "cochrane": "(3):CD011008"})
for k in ("thayer2009", "m3g_refute"):
    REFS[k]["journal"] = REFS[k]["journal"].replace("&amp;", "&")
REFS["oin2026"]["journal"] = REFS["oin2026"]["journal"].replace("&amp;", "&")

io.open(PATH, "w", encoding="utf-8").write(json.dumps(REFS, indent=1, ensure_ascii=False))
for k in list(NEW) + ["nice_ng31"]:
    v = REFS[k]
    print(k, "|", v["authors"][:3], "|", v["title"][:70], "|", v["journal"], v["year"], v["volume"], v["page"])
