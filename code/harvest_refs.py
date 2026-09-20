# -*- coding: utf-8 -*-
"""Find and verify the literature this hypothesis actually rests on.

The draft asserts that N400 semantic-mismatch responses have been recorded in
actively dying hospice patients. That is the load-bearing empirical claim of the
whole paper, so it is checked first and separately: the hospice EEG work and the
N400 work are, as far as the literature goes, different experiments measuring
different components, and conflating them would be the error a reviewer finds.
"""
import json, time, urllib.parse, urllib.request

MAIL = "sandler.leon@gmail.com"
QUERIES = {
 # the load-bearing claim
 "blundon2020":   "Electrophysiological evidence of preserved hearing at the end of life Blundon Gallagher Ward",
 "kotchoubey2005":"Information processing in severe disorders of consciousness vegetative state event-related brain potentials Kotchoubey",
 "steppacher2013":"N400 predicts recovery from disorders of consciousness Steppacher Kissler",
 # auditory pathway
 "ledoux1998":    "Fear and the brain where have we been LeDoux amygdala auditory thalamus",
 "kraus2010":     "Music training for the development of auditory skills Kraus Chandrasekaran brainstem",
 # neurovisceral integration
 "thayer2009":    "Claude Bernard and the heart-brain connection neurovisceral integration Thayer Lane",
 "critchley2004": "Neural systems supporting interoceptive awareness Critchley Wiens Rotshtein Dolan",
 # hypnosis and pain
 "rainville1997": "Pain affect encoded in human anterior cingulate but not somatosensory cortex Rainville Duncan Price",
 "montgomery2000":"A meta-analysis of hypnotically induced analgesia how effective is hypnosis Montgomery DuHamel Redd",
 "jensen2015":    "Hypnotic approaches for chronic pain management clinical implications of recent research Jensen Patterson",
 # palliative pharmacology
 "klepstad2005":  "Routes for administration of opioids morphine metabolites clinical relevance M3G M6G",
 "smith2000":     "Neuroexcitatory effects of morphine and hydromorphone evidence implicating the 3-glucuronide metabolites Smith",
 "wiffen2016":    "Morphine for cancer pain Cochrane systematic review Wiffen Wee Moore",
 # anxiety, hyperalgesia, dyspnea
 "banzett2015":   "Multidimensional dyspnea profile an instrument for clinical and laboratory research Banzett",
 "ploner2011":    "Prestimulus functional connectivity determines pain perception in humans Ploner Lee Wiech",
 "wiech2008":     "Neurocognitive aspects of pain perception Wiech Ploner Tracey",
}


def search(q):
    url = ("https://api.crossref.org/works?rows=3&select=DOI,title,container-title,issued,author,volume,page,type"
           "&query.bibliographic=" + urllib.parse.quote(q))
    r = urllib.request.Request(url, headers={"User-Agent": "ref-harvest/1.0 (mailto:%s)" % MAIL})
    with urllib.request.urlopen(r, timeout=45) as resp:
        return json.load(resp)["message"]["items"]


out = {}
for tag, q in QUERIES.items():
    try:
        items = search(q)
    except Exception as e:
        print("%-16s SEARCH FAILED %s" % (tag, e)); continue
    m = items[0]
    title = (m.get("title") or ["?"])[0]
    jr = (m.get("container-title") or ["?"])[0]
    yr = (m.get("issued", {}).get("date-parts") or [[None]])[0][0]
    auth = m.get("author") or []
    out[tag] = {"doi": m["DOI"], "title": title, "journal": jr, "year": yr,
                "authors": ["%s %s" % (a.get("family", "?"),
                                       "".join(w[0] for w in (a.get("given") or "").split()))
                            for a in auth],
                "volume": m.get("volume"), "page": m.get("page"), "type": m.get("type")}
    print("%-16s %-34s %s (%s)" % (tag, m["DOI"], jr[:32], yr))
    print("%16s %s" % ("", title[:88]))
    time.sleep(0.25)

json.dump(out, open("_refs.json", "w"), indent=1)
print("\nharvested %d" % len(out))
