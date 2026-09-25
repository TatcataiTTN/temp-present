"""Bias audit for the MCQ bank: answer position, answer length, and duplicate options."""
import json
from collections import Counter
from pathlib import Path

qs = [q for q in json.loads((Path(__file__).resolve().parent.parent / "data" / "questions.json").read_text(encoding="utf-8"))["questions"] if q["type"] == "mcq"]
pos = Counter(q["options"].index(q["answer"]) for q in qs)
n = len(qs)
print(f"MCQ count: {n}")
print("Correct-answer position:", {k: pos.get(k, 0) for k in range(4)})
exp = n / 4
chi2 = sum((pos.get(k, 0) - exp) ** 2 / exp for k in range(4))
print(f"chi-square = {chi2:.2f} (df=3, critical 7.81 at p=0.05)")
longest = sum(1 for q in qs if len(q["answer"]) == max(len(o) for o in q["options"]))
print(f"Correct answer is the longest option in {longest}/{n} questions (chance ~ {n/4:.1f})")
ok = chi2 < 7.81 and longest / n < 0.5
dups = [q["id"] for q in qs if len(set(q["options"])) != len(q["options"])]
print("Duplicate options:", dups or "none")
print("AUDIT", "PASS" if ok and not dups else "FAIL")
raise SystemExit(0 if ok and not dups else 1)
