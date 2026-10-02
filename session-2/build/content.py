"""Content for Session 2: Discussion Questions on Innovation. English, as supplied + light framing."""

INTRO = ("Session 2 moves from building one product (Session 1) to examining the claim that innovation itself "
         "is now compulsory. Both questions below are argued on two sides before ending in a probing question, "
         "so the discussion does not settle on a single verdict but exposes the assumption underneath it.")

Q = [
    dict(
        n=1, kind="Question",
        title="The Pressure to Innovate in the Digital Age",
        prompt='Analyze the statement: "Innovation is no longer an option but a prerequisite for business survival '
               'in the digital age." Provide one real-world example of a company that has succeeded through '
               'innovation to illustrate this point.',
        issue="This statement posits an absolute assumption about corporate survival, suggesting that the pace of "
              "digital technological change outstrips the adaptation cycles of traditional business models.",
        agree_label="Perspective of agreement",
        agree="The digital age alters consumer behavior extremely rapidly. Netflix is a prime example. It abandoned "
              "its safe DVD-rental model, enduring short-term losses to disrupt itself and pivot to streaming, later "
              "leveraging massive data analytics to produce original content. It survived and dominated, whereas "
              "competitor Blockbuster collapsed by clinging to outdated processes.",
        oppose_label="Opposing perspective (logical flaws)",
        oppose="Treating technological innovation as a “prerequisite” in all contexts can lead to herd "
               "mentality. Blind innovation that ignores core business fundamentals leads to cash burn, for example "
               "startups flocking to the Metaverse or Web3 without a real value proposition. In many niche "
               "industries, such as organic agriculture or high-end craftsmanship, the authenticity and "
               "sustainability of physical supply chains offer greater vitality than forced “digitalization.”",
        probe="Does every industry truly face the “digitize or die” pressure with equal intensity, or is "
              "the obsession with “innovation” sometimes just a marketing tool for tech corporations to "
              "sell software solutions to traditional businesses that do not genuinely need them?",
        example=("Netflix", "survived by disrupting its own DVD business"),
        counter_example=("Blockbuster", "collapsed by defending the status quo"),
    ),
    dict(
        n=2, kind="Group discussion",
        title="The Role of Innovation in Global Challenges",
        prompt="Evaluate the role of innovation in addressing current global challenges (such as climate change, "
               "the green energy transition, or supply chain optimization).",
        issue="Evaluating the capacity and limitations of technological / innovation tools in resolving systemic, "
              "macro-level crises.",
        agree_label="Perspective of agreement",
        agree="Innovation provides mathematical tools and technical infrastructure to optimize resources. In supply "
              "chains, big-data modeling and AI help minimize disruptions and avoid logistics waste. In the green "
              "energy transition, breakthroughs in battery-storage materials or the optimization of High-Performance "
              "Computing (HPC) enable accurate simulations of climate models.",
        oppose_label="Opposing perspective (logical flaws)",
        oppose="Technology often only addresses the “symptoms.” The root causes of climate change or "
               "supply-chain disruptions lie in geopolitical conflicts, regulatory policies, and economic models "
               "focused on profit maximization. Furthermore, technological innovation itself generates new "
               "problems: electronic waste from solar panels, or the massive energy consumption required to "
               "operate server clusters for training generative AI.",
        probe="Are we overusing our faith in “technological innovation” as a panacea (techno-solutionism) "
              "to evade the responsibility of altering the core political-economic structures and consumption "
              "habits of modern society?",
        example=("HPC climate simulation", "optimizes the forecasting tool, not the policy"),
        counter_example=("AI server clusters", "the fix that adds new energy demand"),
    ),
]

TAKEAWAY = ("Both cases follow the same shape: a real, defensible case for innovation sits next to a real, "
            "defensible limit on it. The useful move is not picking a side but asking who benefits from stating "
            "the claim as an absolute — and what it conveniently excuses.")
