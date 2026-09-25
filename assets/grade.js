// Grading + hụi payout maths. Shared by the browser (practice page) and Node (tests/verify.mjs).
(function (root) {
  // "18,000,000", "18 000 000", "18.000.000" (Vietnamese grouping) and "18000000" all mean 18000000.
  function parseNumber(s) {
    var t = String(s == null ? "" : s).trim();
    if (!t) return NaN;
    if (/^\d{1,3}(\.\d{3})+$/.test(t)) t = t.replace(/\./g, "");
    t = t.replace(/[,\s_]/g, "");
    return /^-?\d+(\.\d+)?$/.test(t) ? Number(t) : NaN;
  }
  function grade(q, given) {
    if (q.type === "mcq") return given === q.answer;
    if (q.type === "num") { var n = parseNumber(given); return !isNaN(n) && n === q.answer; }
    return false;
  }
  // Simplified models (state the assumptions in the question text).
  function deadPot(members, contribution) { return (members - 1) * contribution; }
  function livePot(members, contribution, cycle, bid) {
    var collected = cycle - 1;                  // members who already took the pot pay in full
    var living = members - collected - 1;       // members still waiting pay contribution - bid
    return collected * contribution + living * (contribution - bid);
  }
  function totalPaid(list) { return list.reduce(function (a, b) { return a + b; }, 0); }
  function progressPct(done, total) { return Math.round(done / total * 100); }
  var api = { parseNumber: parseNumber, grade: grade, deadPot: deadPot, livePot: livePot, totalPaid: totalPaid, progressPct: progressPct };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else root.HuiMath = api;
})(typeof window !== "undefined" ? window : globalThis);
