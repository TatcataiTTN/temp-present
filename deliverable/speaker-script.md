# Speaker script (English, ~10 min)

**Slide 1 (Title, ~30s)**

Good morning everyone. Today's exercise is SCAMPER, a method for improving an existing product. My product is an app for keeping track of hụi, the traditional rotating savings circles. I will show the market gap behind it, what the app does today, and how seven SCAMPER questions turn it into a new version.

**Slide 2 (A big informal market, ~40s)**

In Vietnam, informal savings and credit circles such as hụi and bốc bát họ are part of daily life, so demand for them is high. Right next to them we see black credit and a large number of pawnshops. That tells us two things: the market is big, and many households are not served by formal finance.

**Slide 3 (Market gap diagram, ~90s)**

Let me put this in one picture. On the left, two needs: saving towards a lump sum, and borrowing cash quickly. In the middle, what people use today. On the right, what is missing. In this large market there is essentially no neutral intermediary that can hold and freeze the money in a reasonable, transparent way, so all the trust sits with one host, and when the host fails everyone loses. There is also no channel that converts a credit-card limit into a predictable flat-fee cost, so people who need cash go to informal lenders. Our app does not solve all of this. It is the first layer at the bottom: a trusted record of who paid what and when, which any future escrow or flat-fee service would need.

**Slide 4 (The product today, ~35s)**

Here is the product today. It is a Flutter app for Android and iOS. All data is stored on the phone in SQLite, so it works fully offline. It supports two kinds of circles: dead hụi, where nobody pays interest, and live hụi, where members bid and interest applies. For every cycle you mark paid or unpaid, enter the real amount and add a note. A basic dashboard shows the total paid, what remains, and overall progress.

**Slide 5 (Architecture diagram, ~50s)**

This diagram shows how the app is built and where the new features plug in. The app follows MVVM. Screens in the presentation layer watch view-models built with Riverpod. View-models use domain models, such as dead and live hụi and the progress rules. The data layer uses Drift on top of an SQLite file that never leaves the phone, and GoRouter handles navigation. The orange boxes at the bottom are the SCAMPER changes: each one lands in exactly one layer, so the redesign is small and safe.

**Slide 6 (One hụi cycle, ~45s)**

If you have never joined a circle, here is the idea. Ten people each pay a fixed amount every cycle. In each cycle one member collects the whole pot, and the turn moves on until everyone has collected once. Watch the highlighted member: that person receives the pot in this cycle, and earlier receivers are marked as collected. Dead hụi is exactly this. In live hụi, members bid an interest amount to collect earlier. It all works on trust, which is why a clear record matters.

**Slide 7 (SCAMPER overview, ~30s)**

SCAMPER gives us seven lenses: Substitute, Combine, Adapt, Modify, Put to another use, Eliminate, and Rearrange or Reverse. For each lens I ask one open question about the app, and I keep only ideas that lower friction for a real hụi player. We will go through them in three groups.

**Slide 8 (Substitute + Combine, ~55s)**

Substitute. Today users type every amount. We replace typing with a one-tap Paid button that defaults to the agreed amount, with an optional photo of the transfer receipt. Combine. The ledger entry, the reminder and the payment QR code live on one card, so the question who owes what and when, and the action pay now, are on the same screen. Both ideas remove steps and need no server.

**Slide 9 (Adapt + Modify, ~55s)**

Adapt. Loan and banking apps show a colour-coded due and overdue timeline. Hụi players deserve the same clarity. We also adapt how chat apps share pictures, so a receipt can go to the circle's group in one tap. Modify. Cycle length becomes flexible: weekly, every ten days or monthly. We add a large-text mode for older players and a bigger, clearer progress ring.

**Slide 10 (Put to another use + Eliminate + Rearrange/Reverse, ~65s)**

Put to another use. The same ledger can track a personal savings goal, and can serve other circle types such as chit funds or tontines. It also becomes a simple proof of payment history. Eliminate. No sign-up, no internet requirement, no advertising, and no hand calculation, because the app computes bid payouts automatically. Rearrange or Reverse. Today the host's list of circles comes first. We reverse the point of view and open on this week: what I owe, with the host view one tap away.

**Slide 11 (The sketch, ~55s)**

This is my sketch of the new version. Read it from top to bottom. At the top, a toggle switches between player and host view. The offline chip reminds users there is no account. The ring shows progress, and the slider changes the text size. Each card has a one-tap Paid button, a late label in the timeline style, and a bell and QR icon. The bottom tab adds Goals. Every letter on the right matches a SCAMPER technique, so you can trace each change back to a question.

**Slide 12 (Close, ~50s)**

To close. The new version keeps the promise of the current app: free, private and offline. It removes friction: fewer taps to record a payment, a reminder before the due date, and nothing to sign up for. And it points to the bigger opportunity we started with. A trustworthy record is the first building block for an escrow-style service or a flat-fee credit product for this market. Next steps: build a clickable prototype and test it with five real hụi players. Thank you, and I am happy to take questions.
