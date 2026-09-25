"""Hand-written question bank. Contains NO answers for numeric questions:
compute_expected.py runs each `calc` to produce the expected value."""

TECHNIQUES = ["Substitute", "Combine", "Adapt", "Modify", "Put to another use", "Eliminate", "Rearrange/Reverse"]

# One short idea per technique for the HụiKeeper 2.0 concept (all ~50 characters, to avoid length bias).
IDEAS = {
    "Substitute": "Replace typing amounts with a one-tap 'Paid' button",
    "Combine": "Merge the ledger, reminders and a payment QR code",
    "Adapt": "Borrow the due/overdue timeline from loan apps",
    "Modify": "Add flexible cycle lengths and a large-text mode",
    "Put to another use": "Reuse the ledger as a personal savings-goal tracker",
    "Eliminate": "Remove sign-up and hand calculation of bid payouts",
    "Rearrange/Reverse": "Show the player's view first instead of the host's",
}

# Idea -> technique, phrased differently from IDEAS so the two question types test different wording.
CLASSIFY = [
    ("The team swaps the paper notebook for a phone ledger.", "Substitute"),
    ("A backpack gets a built-in charger, so two products become one.", "Combine"),
    ("Designers copy how chat apps share a picture so receipts can go to a group.", "Adapt"),
    ("Text size, button size and cycle length all become adjustable.", "Modify"),
    ("A ledger built for hụi is also used to track a personal savings goal.", "Put to another use"),
    ("The app no longer asks users to create an account.", "Eliminate"),
    ("The home screen shows what a player owes this week, not the host's list.", "Rearrange/Reverse"),
]

FACT = [
    {
        "stem": "Which of these is NOT one of the seven SCAMPER techniques?",
        "correct": "Prioritize", "wrong": ["Combine", "Adapt", "Eliminate"],
        "explain": "SCAMPER = Substitute, Combine, Adapt, Modify, Put to another use, Eliminate, Rearrange/Reverse.",
    },
    {
        "stem": "What does the letter P in SCAMPER stand for?",
        "correct": "Put to another use", "wrong": ["Predict", "Plan ahead", "Prototype"],
        "explain": "P asks: who else could use this product, or where else could it be used?",
    },
]

# Numeric questions: `calc` is the reference solution, run by compute_expected.py.
NUMERIC = [
    {
        "id": "n1", "technique": "Modify",
        "stem": "Dead hụi (no interest): 10 members each pay 2,000,000 VND per cycle. In simplified form the receiver does not pay in their own cycle. How much VND does the receiver collect?",
        "hint": "Everyone except the receiver pays.",
        "params": {"members": 10, "contribution": 2_000_000},
        "calc": "deadPot",
        "explain": "({members} - 1) x {contribution:,} = {answer:,} VND.",
    },
    {
        "id": "n2", "technique": "Adapt",
        "stem": "Live hụi (with interest): 10 members, base contribution 1,000,000 VND. In cycle 3 the winner bids a discount of 200,000 VND. Members who already collected pay in full; members still waiting pay base minus the bid; the winner pays nothing. How much VND does the winner collect?",
        "hint": "Two members collected in cycles 1 and 2; seven are still waiting.",
        "params": {"members": 10, "contribution": 1_000_000, "cycle": 3, "bid": 200_000},
        "calc": "livePot",
        "explain": "{collected} x {contribution:,} + {living} x ({contribution:,} - {bid:,}) = {answer:,} VND.",
    },
    {
        "id": "n3", "technique": "Substitute",
        "stem": "The app records these actual payments (VND): 2,000,000; 2,000,000; 1,800,000; 2,000,000; 2,000,000; 1,500,000. The plan is 10 cycles x 2,000,000. How much VND remains to be paid?",
        "hint": "Remaining = planned total - total actually paid.",
        "params": {"paid": [2_000_000, 2_000_000, 1_800_000, 2_000_000, 2_000_000, 1_500_000], "planned": 20_000_000},
        "calc": "remaining",
        "explain": "Paid = {paid_sum:,}; remaining = {planned:,} - {paid_sum:,} = {answer:,} VND.",
    },
    {
        "id": "n4", "technique": "Eliminate",
        "stem": "7 of 12 cycles are marked as paid. What is the progress percentage, rounded to the nearest whole number?",
        "hint": "7 / 12 x 100.",
        "params": {"done": 7, "total": 12},
        "calc": "progressPct",
        "explain": "{done} / {total} x 100 = {raw:.2f}, rounded to {answer}%.",
    },
]
