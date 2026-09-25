"""Builds data/questions.json. Numeric answers come from running the reference solutions here.
MCQ options are shuffled with a fixed seed so the correct answer is not positioned predictably."""
import json, random, sys
from pathlib import Path
from questions_source import TECHNIQUES, IDEAS, CLASSIFY, FACT, NUMERIC

SEED = 20260925
rng = random.Random(SEED)
OUT = Path(__file__).resolve().parent.parent / "data" / "questions.json"


def dead_pot(p): return (p["members"] - 1) * p["contribution"]


def live_pot(p):
    collected = p["cycle"] - 1
    living = p["members"] - collected - 1
    return collected * p["contribution"] + living * (p["contribution"] - p["bid"]), collected, living


CALCS = {
    "deadPot": lambda p: (dead_pot(p), {}),
    "livePot": lambda p: (live_pot(p)[0], {"collected": live_pot(p)[1], "living": live_pot(p)[2]}),
    "remaining": lambda p: (p["planned"] - sum(p["paid"]), {"paid_sum": sum(p["paid"])}),
    "progressPct": lambda p: (round(p["done"] / p["total"] * 100), {"raw": p["done"] / p["total"] * 100}),
}


def mcq(qid, technique, stem, correct, wrong, explain):
    opts = [correct] + list(wrong)
    rng.shuffle(opts)
    return {"id": qid, "type": "mcq", "technique": technique, "stem": stem, "options": opts, "answer": correct, "explain": explain}


questions = []
# 7 "which idea is X?" questions
for i, t in enumerate(TECHNIQUES, 1):
    others = [IDEAS[x] for x in TECHNIQUES if x != t]
    wrong = rng.sample(others, 3)
    questions.append(mcq(f"p{i}", t, f'Which idea for the hụi app is an example of "{t}"?', IDEAS[t], wrong,
                         f'"{IDEAS[t]}" applies {t}.'))
# 7 "which technique is this?" questions
for i, (stem, t) in enumerate(CLASSIFY, 1):
    wrong = rng.sample([x for x in TECHNIQUES if x != t], 3)
    questions.append(mcq(f"c{i}", t, f"Which SCAMPER technique is this? {stem}", t, wrong, f"This is {t}."))
for i, f in enumerate(FACT, 1):
    questions.append(mcq(f"f{i}", None, f["stem"], f["correct"], f["wrong"], f["explain"]))
for n in NUMERIC:
    ans, extra = CALCS[n["calc"]](n["params"])
    if not isinstance(ans, int) or ans < 0:
        sys.exit(f"{n['id']}: bad reference answer {ans!r}")
    ctx = dict(n["params"], answer=ans, **extra)
    if "paid" in ctx:
        ctx = {k: v for k, v in ctx.items()}
    questions.append({"id": n["id"], "type": "num", "technique": n["technique"], "stem": n["stem"], "hint": n["hint"],
                      "params": n["params"], "answer": ans, "explain": n["explain"].format(**ctx)})

OUT.write_text(json.dumps({"seed": SEED, "questions": questions}, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"wrote {len(questions)} questions -> {OUT}")
for q in questions:
    if q["type"] == "num":
        print(" ", q["id"], q["answer"], "|", q["explain"])
