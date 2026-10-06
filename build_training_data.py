"""
build_training_data.py - Requirement 1: build the prompt dataset from the survey.

Every response is built from figures computed from the Marketing Research survey
(no invented numbers). Each topic is combined with several respondent segments and
several prompt styles, which gives the "prompt variations" the brief asks for.

Run:  python build_training_data.py
Writes: training_data.jsonl (for fine_tune.py) and prompt_summary.md (for the report)
"""
import os
import re
import json
import glob
import random
from collections import Counter

import pandas as pd
import pyreadstat

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_FILE = os.path.join(BASE_DIR, "training_data.jsonl")
SUMMARY_FILE = os.path.join(BASE_DIR, "prompt_summary.md")
MIN_N = 30  # segments smaller than this are skipped (too small to report fairly)

sav_files = glob.glob(os.path.join(BASE_DIR, "Kaggle dataset", "*.sav"))
if not sav_files:
    raise SystemExit("No .sav file found in 'Kaggle dataset'.")
df, meta = pyreadstat.read_sav(sav_files[0], apply_value_formats=True, formats_as_category=True)


def label(col):
    """The real survey question text for a column (falls back to the column name)."""
    return meta.column_names_to_labels.get(col) or col


# ------------------------------------------------------------------ helpers
AGREE = {"Agree", "Strongly Agree"}
LIKERT = AGREE | {"Neutral", "Disagree", "Strongly Disagree"}


def clean(s):
    return s.dropna().astype(str)


def num(s):
    return pd.to_numeric(s, errors="coerce")


def describe(d, col):
    """One sentence about a column, whatever its answer type (Likert, Yes/No, other)."""
    if col not in d.columns:
        return None
    s = clean(d[col])
    if s.empty:
        return None
    if s.isin(LIKERT).any():
        return f"{round(100 * s.isin(AGREE).mean())}% agreed with '{label(col)}'."
    if s.isin({"Yes", "No"}).any():
        return f"{round(100 * (s == 'Yes').mean())}% answered Yes to '{label(col)}'."
    top = s.value_counts(normalize=True)
    return f"The most common answer to '{label(col)}' was '{top.index[0]}' ({round(100 * top.iloc[0])}%)."


def at_least(facts, k):
    facts = [f for f in facts if f]
    return facts if len(facts) >= k else None


# ------------------------------------------------------------------ topics
def t_visit_frequency(d):
    visits = num(d["VISITS"]).mean()
    facts = [describe(d, "HOWOFT")]
    if pd.notna(visits):
        facts.append(f"The average for '{label('VISITS')}' was {visits:.1f}.")
    return at_least(facts, 2)


def t_conversion(d):
    pair = pd.DataFrame({"a": d["DIDBUY"].astype(object), "v": num(d["VISITS"])}).dropna()
    pair["a"] = pair["a"].astype(str)
    g = pair.groupby("a")["v"].agg(["mean", "size"])
    g = g[g["size"] >= 10].sort_values("size", ascending=False).head(3)
    if len(g) < 2:
        return None
    return [f"For '{label('DIDBUY')}', respondents answering '{k}' averaged {r['mean']:.1f} website visits (n={int(r['size'])})."
            for k, r in g.iterrows()]


def t_attitudes(d):
    return at_least([describe(d, c) for c in ["LIKENET", "SAFEWEB", "EASYUSE", "SECURE"]], 2)


def t_channels(d):
    res = []
    for c in ["BILLBRD", "BANNER", "SURFING", "SENGINE", "TV", "THEATER", "NWSPAPER", "FRIEND", "OTHER"]:
        if c in d.columns:
            s = clean(d[c])
            if s.isin({"Yes", "No"}).any():
                res.append((c, round(100 * (s == "Yes").mean())))
    if len(res) < 3:
        return None
    res.sort(key=lambda x: -x[1])
    facts = [f"'{label(c)}' was reported by {p}% of respondents." for c, p in res[:3]]
    facts.append(f"The least reported was '{label(res[-1][0])}' ({res[-1][1]}%).")
    return facts


def t_trend(d):
    return at_least([describe(d, c) for c in ["RESEARCH", "GOODTOOL", "HELPFUL"]], 2)


def t_pricing(d):
    facts = []
    for c in ["STICKER", "ACTUAL", "WORTH"]:
        m = num(d[c]).mean() if c in d.columns else float("nan")
        if pd.notna(m):
            facts.append(f"The average for '{label(c)}' was ${m:,.0f}.")
    facts += [describe(d, "TRADEIN"), describe(d, "PRICE")]
    return at_least(facts, 2)


def t_switching(d):
    return at_least([describe(d, c) for c in ["ANOTHER", "NOTUSE", "HASSLE", "LIKEPROC"]], 2)


TOPICS = [
    ("Consumer behavior", "visit frequency", t_visit_frequency, "how often people buy things through the Internet and how many times they visit the website"),
    ("Consumer behavior", "visits and buying", t_conversion, "how the number of website visits relates to whether people bought their vehicle on the site"),
    ("Consumer behavior", "online attitudes", t_attitudes, "attitudes toward the Internet and the Auto Online website"),
    ("Market trends", "advertising channels", t_channels, "how respondents found out about Auto Online"),
    ("Market trends", "shift to online research", t_trend, "how respondents use the Internet to research vehicle purchases"),
    ("Competitor analysis", "pricing transparency", t_pricing, "vehicle prices, trade-in values and perceived value when buying online"),
    ("Competitor analysis", "switching and gaps", t_switching, "reservations about online dealerships compared with the traditional dealership process"),
]
# ------------------------------------------------ prompt styles (variations)
STYLES = [
    ("question", "What do the survey results show about {core} among {seg}?"),
    ("instruction", "Summarize {core} for {seg} using the survey data."),
    ("analyst persona", "As a market research analyst, describe {core} for {seg}."),
    ("strategist persona", "As a marketing strategist, what should we know about {core} among {seg}?"),
    ("bullet format", "List the key findings on {core} for {seg} as bullet points."),
    ("descriptive-only", "Describe {core} for {seg}. Stick to what the data shows and do not generalize beyond the sample."),  
]


def compose(style, facts, n):
    note = f"(Based on {n} respondents; these figures are descriptive, not causal.)"
    if style == "bullet format":
        return "\n".join(f"- {f}" for f in facts) + "\n" + note
    body = " ".join(facts)
    if style == "strategist persona":
        body += " Treat this as a starting point to check against other data before acting."
    return f"{body} {note}"


# ------------------------------------------------------------- segments
def income_tier(lab):
    if pd.isna(lab):
        return None
    nums = [int(x.replace(",", "")) for x in re.findall(r"\$([\d,]+)", str(lab))]
    if not nums:
        return None
    low = 0 if str(lab).lower().startswith("under") else nums[0]
    return "lower-income" if low < 50000 else "middle-income" if low < 95000 else "higher-income"


df["AGE"] = num(df["AGE"])
df["_income_tier"] = df["INCOME"].map(income_tier)

segments = {"all respondents in the survey": pd.Series(True, index=df.index)}
for g in clean(df["GENDER"]).unique():
    segments[f"{g.lower()} respondents"] = df["GENDER"].astype(str) == g
segments["respondents under 30"] = df["AGE"] < 30
segments["respondents aged 30 to 44"] = (df["AGE"] >= 30) & (df["AGE"] < 45)
segments["respondents aged 45 and over"] = df["AGE"] >= 45
for t in ["lower-income", "middle-income", "higher-income"]:
    segments[f"{t} respondents"] = df["_income_tier"] == t
for edu in clean(df["EDUCATE"]).value_counts().head(3).index:
    segments[f"respondents whose education was '{edu}'"] = df["EDUCATE"].astype(str) == edu
# RACE is deliberately NOT used to generate prompts: it is only audited in bias_check.py.

kept, skipped = {}, []
for name, mask in segments.items():
    n = int(mask.sum())
    if n >= MIN_N:
        kept[name] = mask
    else:
        skipped.append((name, n))

# ------------------------------------------------------------- generate
examples = []
for ti, (aspect, topic, fn, core) in enumerate(TOPICS):
    for si, (seg, mask) in enumerate(kept.items()):
        d = df[mask]
        facts = fn(d)
        if not facts:
            continue
        for k in (0, 3):  # two different prompt styles per topic/segment pair
            style, template = STYLES[(ti + si + k) % len(STYLES)]
            prompt = template.format(core=core, seg=seg)
            text = f"Prompt: {prompt}\nInsight: {compose(style, facts, int(mask.sum()))}"
            examples.append({"text": text, "aspect": aspect, "style": style, "segment": seg})

random.Random(42).shuffle(examples)
with open(OUT_FILE, "w", encoding="utf-8") as f:
    for ex in examples:
        f.write(json.dumps({"text": ex["text"]}, ensure_ascii=False) + "\n")

# ------------------------------------------------------------- summary
lines = [f"# Prompt dataset summary", "", f"Total examples: {len(examples)} (source: {os.path.basename(sav_files[0])}, {len(df)} respondents)", ""]
lines += ["## By aspect"] + [f"- {k}: {v}" for k, v in Counter(e["aspect"] for e in examples).items()]
lines += ["", "## By prompt style"] + [f"- {k}: {v}" for k, v in Counter(e["style"] for e in examples).items()]
lines += ["", f"## Respondent segments used (minimum n = {MIN_N})"] + [f"- {k}: n={int(m.sum())}" for k, m in kept.items()]
if skipped:
    lines += ["", "## Segments skipped (too small)"] + [f"- {k}: n={n}" for k, n in skipped]
print("\n".join(lines))
with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print(f"\nWrote {len(examples)} training examples to training_data.jsonl")
