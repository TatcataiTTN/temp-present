"""Single source of content for every page (English)."""

TECH = [
    dict(k="S", name="Substitute", q="What can be replaced or swapped?",
         prompts=["Which part, material or person could be swapped for something else?",
                  "Which rule, place or step could be replaced?",
                  "Would a simpler process do the same job?"],
         everyday="Umbrella: swap the opaque fabric for a clear dome so you can see where you walk.",
         idea="Replace typing every amount with a one-tap “Paid” button that defaults to the agreed amount, plus an optional photo of the transfer receipt.",
         why="Recording a payment takes seconds instead of a form."),
    dict(k="C", name="Combine", q="What can be merged into one?",
         prompts=["Which two features, products or services could become one?",
                  "Which purposes could be served in the same place?",
                  "Which users’ needs meet on one screen?"],
         everyday="School backpack: add a built-in power bank so bag and charger are one item.",
         idea="Put the ledger entry, the reminder and a payment QR code on the same card, so “who owes what, when” and “pay now” sit together.",
         why="Fewer screens between knowing a due date and settling it."),
    dict(k="A", name="Adapt", q="What else is like this, and what can be copied from it?",
         prompts=["What similar problem has another field already solved?",
                  "Which idea from a different product could be borrowed?",
                  "What could this imitate from nature or industry?"],
         everyday="Face mask: adapt the fabric layers of sportswear for breathability.",
         idea="Borrow the colour-coded due / overdue timeline of loan apps, and the “share a picture” flow of chat apps for sending receipts to the circle’s group.",
         why="Users already understand these patterns, so there is nothing new to learn."),
    dict(k="M", name="Modify", q="What can be made bigger, smaller, faster, slower or different?",
         prompts=["What could be magnified, exaggerated or made stronger?",
                  "What could be minimised or simplified?",
                  "What about shape, size, colour or frequency could change?"],
         everyday="Time-management app: shrink the daily view to one glanceable number.",
         idea="Make cycle length flexible (weekly, every ten days, monthly), add a large-text mode for older players, and enlarge the progress ring.",
         why="One app fits many circle rhythms and many kinds of users."),
    dict(k="P", name="Put to another use", q="Who else could use it, and where else?",
         prompts=["Who else could use this product?",
                  "Where else could it be used?",
                  "What would it become in a different setting?"],
         everyday="Umbrella: use it as a sun shade or a market-stall canopy.",
         idea="Reuse the ledger as a personal savings-goal tracker, as a template for other rotating-savings circles, and as a simple proof of payment history.",
         why="The same data model creates value beyond hụi."),
    dict(k="E", name="Eliminate", q="What can be removed without losing the core value?",
         prompts=["What step exists only out of habit?",
                  "What could be removed to make it simpler?",
                  "What would the minimal version look like?"],
         everyday="Backpack: remove extra pockets to make a lighter, single-compartment bag.",
         idea="No sign-up, no internet requirement, no ads, and no hand calculation, because the app works out bid payouts automatically.",
         why="Less friction, less risk, and full privacy on the device."),
    dict(k="R", name="Rearrange / Reverse", q="What if the order, roles or layout were reversed?",
         prompts=["What if the sequence of steps were reversed?",
                  "What if the roles of user and provider swapped?",
                  "What if the layout were turned inside out?"],
         everyday="Umbrella: open it upside down to collect rain water.",
         idea="Reverse the point of view: open on “This week — what I owe” for players, with the host view one tap away, instead of the host’s list of circles.",
         why="The home screen answers the question users actually ask first."),
]

MARKET = [
    "Hụi and bốc bát họ circles are a normal part of everyday finance, so demand is high.",
    "Black credit and pawnshops thrive next to them, which shows how large the underserved market is.",
    "There is essentially no neutral intermediary that holds (freezes) the pot in a fair, transparent way. Trust rests on one host.",
    "There is no channel that converts a credit-card limit into a predictable flat-fee cost, so people fall back on informal lenders.",
]

# (slide title, visible-html, speaker notes, seconds)
NOTES = {
    1: ("Good morning everyone. Today's exercise is SCAMPER, a method for improving an existing product. "
        "My product is an app for keeping track of hụi, the traditional rotating savings circles. "
        "I will show the market gap behind it, what the app does today, and how seven SCAMPER questions turn it into a new version.", 30),
    2: ("In Vietnam, informal savings and credit circles such as hụi and bốc bát họ are part of daily life, so demand for them is high. "
        "Right next to them we see black credit and a large number of pawnshops. That tells us the market is big, and that many people are not served by formal finance. "
        "Here is the gap. In this large market there is essentially no neutral intermediary that can hold and freeze the money in a reasonable, transparent way. "
        "Today, all the trust sits with one host, and when the host fails, everyone loses. "
        "There is also no channel that converts a credit-card limit into a predictable flat-fee cost, so people who need cash go to informal lenders instead. "
        "Our app does not solve all of this. It is the first layer: a clear, shared record of who paid what and when. Any future escrow or flat-fee service would need exactly that record.", 100),
    3: ("Here is the product today. It is a Flutter app for Android and iOS. All data is stored on the phone in SQLite, so it works fully offline. "
        "It supports two kinds of circles: dead hụi, where nobody pays interest, and live hụi, where members bid and interest applies. "
        "For every cycle you mark paid or unpaid, enter the real amount and add a note. A basic dashboard shows the total paid, what remains, and overall progress. "
        "Under the hood it follows an MVVM architecture with Riverpod, Drift and GoRouter.", 45),
    4: ("If you have never joined a circle, here is the idea. Ten people each pay a fixed amount every cycle. In each cycle one member collects the whole pot, "
        "and the turn moves on until everyone has collected once. Watch the highlighted member: that person receives the pot in this cycle, and earlier receivers are marked as collected. "
        "Dead hụi is exactly this. In live hụi, members bid an interest amount to collect earlier. It all works on trust, which is why a clear record matters.", 45),
    5: ("SCAMPER gives us seven lenses: Substitute, Combine, Adapt, Modify, Put to another use, Eliminate, and Rearrange or Reverse. "
        "For each lens I ask one open question about the app, and I keep only ideas that lower friction for a real hụi player. We will go through them in three groups.", 40),
    6: ("Substitute. Today users type every amount. We replace typing with a one-tap Paid button that defaults to the agreed amount, with an optional photo of the transfer receipt. "
        "Combine. The ledger entry, the reminder and the payment QR code live on one card, so the question who owes what and when, and the action pay now, are on the same screen. "
        "Both ideas remove steps and need no server.", 60),
    7: ("Adapt. Loan and banking apps show a colour-coded due and overdue timeline. Hụi players deserve the same clarity. We also adapt how chat apps share pictures, so a receipt can go to the circle's group in one tap. "
        "Modify. Cycle length becomes flexible: weekly, every ten days or monthly. We add a large-text mode for older players and a bigger, clearer progress ring.", 60),
    8: ("Put to another use. The same ledger can track a personal savings goal, and can serve other circle types such as chit funds or tontines. It also becomes a simple proof of payment history. "
        "Eliminate. No sign-up, no internet requirement, no advertising, and no hand calculation, because the app computes bid payouts automatically. "
        "Rearrange or Reverse. Today the host's list of circles comes first. We reverse the point of view and open on this week: what I owe, with the host view one tap away.", 75),
    9: ("This is my sketch of the new version. Read it from top to bottom. At the top, a toggle switches between player and host view. The offline chip reminds users there is no account. "
        "The ring shows progress, and the slider changes the text size. Each card has a one-tap Paid button, a late label in the timeline style, and a bell and QR icon. The bottom tab adds Goals. "
        "Every letter on the right matches a SCAMPER technique, so you can trace each change back to a question.", 75),
    10: ("To close. The new version keeps the promise of the current app: free, private and offline. It removes friction: fewer taps to record a payment, a reminder before the due date, and nothing to sign up for. "
         "And it points to the bigger opportunity we started with. A trustworthy record is the first building block for an escrow-style service or a flat-fee credit product for this market. "
         "Next steps: build a clickable prototype and test it with five real hụi players. Thank you, and I am happy to take questions.", 70),
}
