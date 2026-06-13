"""Day-pillar animal wealth corpus — public-speaker narratives per branch."""

from __future__ import annotations

from typing import Any

DAY_PILLAR_WEALTH: dict[str, dict[str, Any]] = {
    "Rat": {
        "archetype": "Lord of Merchants",
        "narrative": (
            "Rat day pillars are gods of money when fully aligned. You trade what others cannot — "
            "crypto, bonds, forex, commodities, import and export, the merchant flow that does not come naturally to most. "
            "As Lord of Merchants you do business inside giant structure with you as the center of the network, even behind the scenes: "
            "banks, hotels, gas stations, convenience chains, nightlife experiences, speculative markets, conglomerates. "
            "Systems, not individual effort. Exploit the side of business that is unnatural to others and success compounds."
        ),
        "close": "Run the machine from the center — trading, speculation, and nightlife networks are your wealth throne when the system knows your name.",
        "examples": [],
        "cheat_code": "Systems at the center — trading, speculative markets, conglomerates, nightlife networks.",
        "lanes": [
            "crypto, bonds, forex, commodities",
            "import/export and merchant flow",
            "banks, hotels, gas stations, convenience chains",
            "nightlife experiences and speculative trading",
        ],
        "support": "Build inside giant structure with you as the network hub, even off-stage.",
        "end": "Solo hustle without a system — Rat wealth is systems, not lone effort.",
        "shadow": "Greedy overreach without the structure to hold it.",
        "spotlight": False,
    },
    "Ox": {
        "archetype": "Builder of Tangible Stability",
        "narrative": (
            "No one talks enough about the Ox — your objective is stability and consistency made tangible. "
            "Real estate, construction, architecture, agriculture, renovation: results you control with your hands. "
            "Home and family are your greatest strengths. Be the architect who designed it, the operator laying track, "
            "running dump trucks, digging tunnels for railways. You make urban life possible by building the stability "
            "everyone else sometimes takes for granted. Build, maintain, and participate in one of these systems — that is your cheat code."
        ),
        "close": "Make the tangible possible — urban life runs on what you build and maintain.",
        "examples": [],
        "cheat_code": "Real estate, construction, architecture, agriculture, renovation — results you can touch.",
        "lanes": [
            "real estate and property",
            "construction, tunnels, rail, heavy equipment",
            "architecture and urban infrastructure",
            "home, family, and tangible maintenance",
        ],
        "support": "Be the person who makes the tangible possible — the architect, the operator laying track.",
        "end": "Abstract hype lanes with nothing built at the end of the quarter.",
        "shadow": "Stubborn rigidity when the blueprint needs revision.",
        "spotlight": False,
    },
    "Tiger": {
        "archetype": "Main-Character Creator",
        "narrative": (
            "Tigers are leaders and creators — the third sign, kin to life-path threes. You excel where creation, entrepreneurship, "
            "music, and creative arts demand an audience. Megan Fox is a Tiger: screen presence and main-character energy in public. "
            "You draw crowds; step fully into creative space and build entrepreneurship around it. "
            "Sales works when you skip the spotlight, but attention is currency — screens, pitches, social media, anywhere eyes pay, you run the room. "
            "You are not people-pleasing; people relax because your aura is larger than life and aligned confidence is not questioned. "
            "You become the mouthpiece, the leader, the construct of what and how — accept that power with action and grit; it is not passive."
        ),
        "close": "Create where attention is the fee — accept the main-character lane with grit, not ego.",
        "examples": ["Megan Fox — Tiger day pillar, screen presence and creative main-character energy"],
        "cheat_code": "Creation, entrepreneurship, music, arts — anywhere attention is the currency.",
        "lanes": [
            "entertainment and performance",
            "sales and pitch leadership",
            "social media and influencer scale",
            "founder-led creative ventures",
        ],
        "support": "Step into creative space with action and grit — confidence puts people at ease when aligned.",
        "end": "Feeding ego — your grounded first impression is the asset; shadow ego is karmic anchor.",
        "shadow": "Ego inflation — the down-to-earth read people first get is your greatest strength.",
        "spotlight": True,
    },
    "Rabbit": {
        "archetype": "God of Manipulation (fair use)",
        "narrative": (
            "Cat and Rabbit day pillars are more philosophical than Tigers — you govern marketing, advertising, sales, and show-business management. "
            "You excel behind the celebrity: the reason any of it is achieved. Think platform operations, cam infrastructure, "
            "the owner of the camera who advertises and sells — not the face on the screen. "
            "You have a sharp eye for talent early; your power is elevating what you witnessed before the crowd did. "
            "That looks like management; it can turn exploitative — intention matters. With great power comes great responsibility. "
            "Build behind the scenes, make it all possible, reap fairly."
        ),
        "close": "See talent early, build it fairly behind the camera — manipulation in service of elevation, not extraction.",
        "examples": [],
        "cheat_code": "Marketing, advertising, management behind the talent — make the machine possible.",
        "lanes": [
            "show-business management and agency work",
            "marketing, advertising, sales architecture",
            "platform and creator economy operations",
            "talent scouting and elevation",
        ],
        "support": "See value in people early and build them fairly — behind-the-scenes ownership.",
        "end": "Exploitative manipulation or hoarding talent — heavy karma weight.",
        "shadow": "Selfish guarding of talent you spotted first.",
        "spotlight": False,
    },
    "Dragon": {
        "archetype": "Peak Presenter",
        "narrative": (
            "Dragon carries main-star celebrity energy like Tiger, but you are the presenter — public speaking, personal trainers, athletes, "
            "highly competitive and extremely driven. You want the top; your advice must be sought and respected. "
            "Innate skill at captivating an audience through tone and texture in ways others cannot replicate from any school. "
            "Only a Dragon will put in the work to ascend or abandon completely — best or leave. "
            "Massive shadow of freedom-seeking: build what you personally care about, step into superstar lane in your market, "
            "and master it through captivating engagement."
        ),
        "close": "Be the best at what you care about — captivate, master, or walk away clean.",
        "examples": [],
        "cheat_code": "Public speaking, trainers, athletes — captivate and demand mastery in your market.",
        "lanes": [
            "public speaking and audience command",
            "personal training, athletics, competitive mastery",
            "presenter-led brands",
            "top-of-market expertise",
        ],
        "support": "Say yes to the superstar lane in what you personally care about — work until mastery or exit clean.",
        "end": "Half-commitment — Dragon is best-or-leave; mediocrity drains the gift.",
        "shadow": "Freedom-seeking abandon when mastery gets hard.",
        "spotlight": True,
    },
    "Snake": {
        "archetype": "Private Tactician",
        "narrative": (
            "Snake refines Dragon energy the way Cat refines Tiger — tacticians, main character behind the scenes running the organization. "
            "Innately strategic; explaining strategy to you is like teaching water it is wet. Poker face, controlled presentation, "
            "three steps ahead, prepared for unfair life. Incredibly resilient. You thrive in private sector enforcement and intelligence, "
            "alphabet agencies, private military, syndicates run from the center. Finance futures are possible, but manager and engineer "
            "behind the curtain is the crown lane. Operate as private force — discretion, silent movement, sudden execution. "
            "Do not become predatory; foresight shapes what is, fairly. You are not a cog — you make the machine work. "
            "The less known about you, the more comfortable you are."
        ),
        "close": "Move silent, shape tactics ahead of the room, make the machine work — fair foresight, not predation.",
        "examples": [],
        "cheat_code": "Private sector systems — enforcement, finance engineering, syndicate operations behind the curtain.",
        "lanes": [
            "enforcement and intelligence architecture",
            "private military and security",
            "futures and finance management",
            "syndicate and org design from the center",
        ],
        "support": "Discretion, poker face, three steps ahead — make the machine work.",
        "end": "Predatory tactics or public overexposure — karma debt and blown cover.",
        "shadow": "Becoming predatory — foresight is for fair shaping, not extraction.",
        "spotlight": False,
    },
    "Horse": {
        "archetype": "Revolutionary Endurance",
        "narrative": (
            "Horse is a revolutionary force — stubborn, resilient, geared to wealth like Rat but through endurance. "
            "Most physical and mental stamina of the day pillars. Athletics and motivating come natural. "
            "You do not need others, yet run well with a herd. Sole proprietorship is your strongest lane: "
            "you control standards, production, sales, and shipping. Team or solo — success needs no permission."
        ),
        "close": "Own the lane end-to-end — endurance is your revolution and your revenue.",
        "examples": [],
        "cheat_code": "Sole proprietorship — you control standards, production, sales, and shipping.",
        "lanes": [
            "sole proprietorship and owner-operator brands",
            "athletics, motivation, endurance ventures",
            "team lead or solo operations",
            "logistics start to finish",
        ],
        "support": "Push standards you control end-to-end; herd optional, endurance mandatory.",
        "end": "Waiting for permission or committee consensus.",
        "shadow": "Stubborn burnout without recovery discipline.",
        "spotlight": True,
    },
    "Goat": {
        "archetype": "Magnetic Presenter",
        "narrative": (
            "Goat is deeply creative — arguably the most attractive aura among day pillars, built for modeling and on-screen presence. "
            "Social media influence, sales, music, advisors, corporate spaces where aesthetics are measured: you excel when you "
            "refine how you dress, speak, and care for yourself. People are naturally drawn; when attention is the fee, "
            "your magnetism is the product. Step fully into that powerhouse."
        ),
        "close": "Refine the aura people already feel — presentation is not vanity here, it is revenue infrastructure.",
        "examples": [],
        "cheat_code": "Modeling, aesthetics, influencer presence — attention fee collected through refined aura.",
        "lanes": [
            "modeling and on-screen creative presence",
            "social media influence and aesthetic brands",
            "sales and advisor roles valuing presentation",
            "corporate-facing polish",
        ],
        "support": "Dress, voice, self-care as revenue infrastructure — magnetic aura is the product.",
        "end": "Ignoring presentation — Goat wealth is the aura people already feel.",
        "shadow": "Vanity without craft behind the image.",
        "spotlight": True,
    },
    "Monkey": {
        "archetype": "Adaptive Problem-Solver",
        "narrative": (
            "Monkey is nearly as strategic as Snake but cannot be boxed into one career. Most adaptable sign — ninth sign, "
            "ninth numerology adaptability. You excel wherever intelligence solves complex problems inside the system. "
            "Responsive, tactical, thinking outside the box while maintaining flow. Incredible engineers; loud or quiet. "
            "You adapt to any environment and dominate where IQ is the bottleneck."
        ),
        "close": "Follow complexity wherever the bottleneck moves — adaptability is your compound interest.",
        "examples": [],
        "cheat_code": "Engineering and complex systems — excel wherever intelligence solves the bottleneck.",
        "lanes": [
            "engineering and technical architecture",
            "R&D and novel problem-solving",
            "tactical adaptation roles",
            "IQ-driven environments",
        ],
        "support": "Follow complexity — adaptability matches flexible finish order.",
        "end": "Boxed repetitive work with no novel problems.",
        "shadow": "Scattered brilliance without delivery deadlines.",
        "spotlight": True,
    },
    "Rooster": {
        "archetype": "Deliberate Healer",
        "narrative": (
            "Rooster carries high but deliberate anger — you actually care, genuinely driven to heal. "
            "Step into that and wealth unlocks: consult, advisor, lawyer, doctor, motivational speaker who creates repair. "
            "Powerhouse in healing emotionally, mentally, physically — innovative even in the science to make it happen. "
            "Personalized care is the lane; cynicism is the lock."
        ),
        "close": "Heal on purpose — personalized care is the wealth key, not the performance of caring.",
        "examples": [],
        "cheat_code": "Consulting, law, medicine, motivational healing — personalized care that innovates.",
        "lanes": [
            "consulting and advisory with genuine care",
            "law, medicine, science-backed healing",
            "motivational speaking that repairs",
            "personalized client transformation",
        ],
        "support": "Step into healing emotionally, mentally, or physically — anger response is care, not noise.",
        "end": "Cynical detachment — wealth unlocks when you care on purpose.",
        "shadow": "Sharp anger misdirected at the wrong target.",
        "spotlight": True,
    },
    "Dog": {
        "archetype": "Force of Justice",
        "narrative": (
            "Dog is attractive like Goat but thrives inside structure — government, enforcement, wherever rules exist and are defined. "
            "You enforce law and protect; you are a force of justice. Wealth comes from honorable systems where trust is the product, "
            "not gray-market chaos."
        ),
        "close": "Protect inside defined structure — justice enforced fairly is your revenue spine.",
        "examples": [],
        "cheat_code": "Government, enforcement, defined rules — protect and enforce fairly inside structure.",
        "lanes": [
            "government and public-sector structure",
            "law enforcement and compliance",
            "security and protection services",
            "institutional roles with clear rules",
        ],
        "support": "Work inside systems where law is written and justice is the product.",
        "end": "Chaotic gray-market lanes that erode trust.",
        "shadow": "Rigid judgment without mercy.",
        "spotlight": False,
    },
    "Pig": {
        "archetype": "Provider of Appetite",
        "narrative": (
            "Pig sees what people are gluttonous over before anyone else — provide that resource. "
            "Nightlife, car sales, jewelers, vice-adjacent dreams people always fund. One of the wealthiest sign patterns when disciplined. "
            "The Pig calls toward gluttony; do not become gluttonous — karma debt. Resource the appetite in others fairly; that is the cheat code."
        ),
        "close": "Feed the appetite you see early — provide the dream, never become the vice.",
        "examples": [],
        "cheat_code": "Sell what people are gluttonous for — nightlife, luxury desire, dream merchandise (fair provider).",
        "lanes": [
            "nightlife and experience hospitality",
            "auto, jewelry, luxury desire markets",
            "vice-adjacent resources people always fund",
            "dream-selling with ethical delivery",
        ],
        "support": "See appetite before others and resource it — disciplined provider pattern.",
        "end": "Personal gluttony — karma debt; resource the appetite, skip becoming the vice.",
        "shadow": "Self-indulgence while merchandising excess.",
        "spotlight": False,
    },
}

BACKSTAGE_ANIMALS = frozenset({"Rat", "Rabbit", "Snake", "Dog", "Ox", "Pig"})
SPOTLIGHT_ANIMALS = frozenset({"Tiger", "Dragon", "Goat", "Horse", "Monkey", "Rooster"})