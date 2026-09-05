"""
================================================================================
 INTERACTIVE ENGLISH EXAM (A2/B1) — Unit 8 "Shopping for Clothes"
                                    & Unit 9 "Fitness and Health"
================================================================================
Streamlit app featuring:
  - 2 completely different exam versions (Version A / Version B), chosen manually
    (no random-exam option)
  - Listening (Web Speech API, text-to-speech in the browser), Reading,
    Vocabulary/Phrasal Verbs & Expressions, Grammar (Superlatives + Modals:
    have to / should / could) and Writing (150 words)
  - Automatic on-screen grading (green/red feedback + grammar explanations)
  - Printable view / exportable to PDF (Ctrl+P) with no Streamlit controls
  - Answers persisted with st.session_state
  - Everything in the app is in English (interface + content)

Run with:  streamlit run app.py
================================================================================
"""

import html as html_lib
import re

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="English Exam · Unit 8 & 9", page_icon="🛍️", layout="wide")

# ==============================================================================
# 0. GLOBAL CSS (includes print rules)
# ==============================================================================
st.markdown(
    """
    <style>
    .stApp { background-color: #fafafa; }
    .exam-title {
        background: linear-gradient(90deg,#2c3e50,#8e44ad);
        color: white; padding: 18px 24px; border-radius: 10px; margin-bottom: 18px;
    }
    .word-bank {
        background:#fff3cd; border:2px dashed #e0a800; border-radius:10px;
        padding:14px 18px; font-size:1.05em; margin-bottom:14px;
    }
    .feedback-correct { color:#1e7e34; background:#d4edda; padding:6px 10px; border-radius:6px; margin:4px 0;}
    .feedback-wrong   { color:#a71d2a; background:#f8d7da; padding:6px 10px; border-radius:6px; margin:4px 0;}
    .explain { color:#555; font-size:0.9em; margin-left:8px; font-style:italic;}
    .print-page {
        background:white; padding:36px; border:1px solid #ddd; border-radius:6px;
        max-width:900px; margin:auto; line-height:1.55;
    }
    .print-page h1 { border-bottom:3px solid #333; padding-bottom:6px;}
    .print-page h2 { color:#2c3e50; margin-top:26px; border-left:6px solid #8e44ad; padding-left:10px;}
    .answer-box { border:1px solid #333; padding:14px; min-height:120px; margin-top:6px;}

    @media print {
        body * { visibility: hidden; }
        #printable-area, #printable-area * { visibility: visible; }
        #printable-area { position: absolute; left: 0; top: 0; width: 100%; }
        .no-print { display: none !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==============================================================================
# 1. EXAM CONTENT — TWO FULL VERSIONS
# ==============================================================================

CONTENT = {
    "A": {
        "label": "Version A — 'A Day of Shopping and Style' (Shopping & Fitness)",
        "listening": {
            "title": "Sara's Shopping Afternoon",
            "audio_text": (
                "Last Saturday, Sara decided to go shopping for a new outfit because she had a "
                "job interview the following week. She started at a small boutique downtown, but "
                "the prices there were surprisingly expensive, so she decided to try the big "
                "department store instead. At the department store, a salesperson told her that a "
                "spring sale was happening, and that almost everything was on sale that weekend. "
                "Sara looked at several blazers and finally found a dark blue one that fit her "
                "perfectly. She also needed a new pair of shoes, so she went to the footwear "
                "section on the second floor. She tried on three different pairs of flats, and "
                "she chose the most comfortable ones, even though they weren't the cheapest. "
                "After that, she remembered she needed a belt and a small purse to match her "
                "blazer, so she asked a salesperson for help finding the accessories department. "
                "The salesperson explained that accessories were on the first floor, near the "
                "front entrance, not far from the escalator. When Sara finally got to the "
                "checkout counter, she realized her total was higher than she expected, but the "
                "salesperson reminded her that everything was still thirty percent off. Sara "
                "decided to pay with her credit card instead of cash. She left the store feeling "
                "confident about her interview outfit, and she even had time to stop for coffee "
                "before heading home."
            ),
            "mc": [
                {"q": "Why did Sara go shopping?",
                 "options": ["For a vacation", "For a job interview", "For a party", "For a wedding"],
                 "answer": "For a job interview", "explain": "'because she had a job interview the following week.'"},
                {"q": "Where did Sara first go shopping?",
                 "options": ["A department store", "A small boutique downtown", "An online store", "A street market"],
                 "answer": "A small boutique downtown", "explain": "'She started at a small boutique downtown.'"},
                {"q": "What did Sara buy first at the department store?",
                 "options": ["Shoes", "A blazer", "A purse", "A belt"],
                 "answer": "A blazer", "explain": "'Sara looked at several blazers and finally found a dark blue one.'"},
                {"q": "Where is the accessories department located?",
                 "options": ["On the second floor", "In the basement", "On the first floor, near the front entrance", "On the top floor"],
                 "answer": "On the first floor, near the front entrance",
                 "explain": "'accessories were on the first floor, near the front entrance.'"},
                {"q": "How did Sara pay for her items?",
                 "options": ["Cash", "Credit card", "A gift card", "A check"],
                 "answer": "Credit card", "explain": "'Sara decided to pay with her credit card instead of cash.'"},
            ],
            "tf": [
                {"s": "Sara went shopping because of a wedding.", "answer": False,
                 "explain": "She went shopping because of a job interview, not a wedding."},
                {"s": "Sara found the boutique's prices too high.", "answer": True,
                 "explain": "'the prices there were surprisingly expensive.'"},
                {"s": "Sara chose the cheapest pair of flats.", "answer": False,
                 "explain": "'she chose the most comfortable ones, even though they weren't the cheapest.'"},
                {"s": "The department store had a spring sale.", "answer": True,
                 "explain": "'a spring sale was happening... almost everything was on sale.'"},
                {"s": "Sara paid full price for everything.", "answer": False,
                 "explain": "'everything was still thirty percent off.'"},
            ],
            "order": {
                "items": [
                    ("A", "She tried on pairs of flats in the footwear section."),
                    ("B", "She paid at the checkout with her credit card."),
                    ("C", "Sara went to the boutique downtown."),
                    ("D", "She asked a salesperson about the accessories department."),
                    ("E", "She went to the department store instead."),
                    ("F", "She found a dark blue blazer."),
                ],
                "correct": ["C", "E", "F", "A", "D", "B"],
            },
        },
        "reading": {
            "text": (
                "Many people believe that getting in shape requires an expensive gym membership, "
                "but that isn't always true. While health clubs like the Downtown Health Club and "
                "Fitness Center offer Olympic-size pools, spin classes, and personal trainers, "
                "there are plenty of low-cost or free ways to stay active. Walking, running, and "
                "hiking, for example, don't require any special equipment other than a good pair "
                "of shoes, and they can be just as effective as a strenuous workout at the gym.\n\n"
                "Of course, some activities do require specific gear. If you go mountain biking, "
                "you have to wear a helmet, and if you go kayaking or sailing, you should probably "
                "wear a life vest, even if it isn't required by law. Buying used equipment or "
                "renting it for a weekend trip can help people try new activities without spending "
                "a lot of money. Some outdoor enthusiasts say that a strenuous weekend of hiking "
                "or kayaking can be just as good a workout as a whole week at the gym.\n\n"
                "Unfortunately, staying active also comes with some risk of injury. According to "
                "physical therapist Martha Roberts, common exercise injuries include sprained "
                "ankles, sore backs, and, in more serious cases, broken bones. She explains that "
                "when a patient can't move a body part because of a cast, the muscles around it "
                "get weak, so physical therapy after an injury is often necessary to help the "
                "patient get back to normal activities safely. Roberts always tells her patients, "
                "'Bodies want to move,' meaning that staying completely still for too long can "
                "actually make recovery slower.\n\n"
                "In the end, experts agree that the best exercise plan is the one a person will "
                "actually continue to do, whether that's a fancy gym membership or a free hike in "
                "a local park. The key is consistency: exercising a little every day is generally "
                "healthier than doing one extremely strenuous workout once a month and then doing "
                "nothing for weeks. For most people, a mix of low-cost outdoor activities and "
                "occasional visits to a gym or fitness class offers the best balance of variety, "
                "motivation, and cost."
            ),
            "questions": [
                {"type": "mc", "q": "According to the text, what is a low-cost way to stay active?",
                 "options": ["Joining an expensive gym", "Walking, running, or hiking", "Hiring a personal trainer"],
                 "answer": "Walking, running, or hiking", "explain": "'Walking, running, and hiking... don't require any special equipment.'"},
                {"type": "tfn", "q": "You should wear a life vest when kayaking, even though it isn't required by law.",
                 "answer": "True", "explain": "'if you go kayaking or sailing, you should probably wear a life vest, even if it isn't required by law.'"},
                {"type": "tfn", "q": "Mountain biking requires you to wear a helmet.",
                 "answer": "True", "explain": "'If you go mountain biking, you have to wear a helmet.'"},
                {"type": "mc", "q": "According to Martha Roberts, what happens to muscles when a body part is in a cast?",
                 "options": ["They get stronger", "They get weak", "They heal faster"],
                 "answer": "They get weak", "explain": "'the muscles around it get weak.'"},
                {"type": "tfn", "q": "Physical therapy is never necessary after an injury.",
                 "answer": "False", "explain": "'physical therapy after an injury is often necessary.'"},
                {"type": "mc", "q": "What does Martha Roberts mean when she says 'Bodies want to move'?",
                 "options": ["Exercise is dangerous", "Staying still for too long can slow down recovery", "People should exercise every hour"],
                 "answer": "Staying still for too long can slow down recovery",
                 "explain": "'staying completely still for too long can actually make recovery slower.'"},
                {"type": "tfn", "q": "The text mentions the exact price of a gym membership.",
                 "answer": "Not Mentioned", "explain": "The text never gives a specific price for a gym membership."},
                {"type": "mc", "q": "In paragraph 3, the word 'sprained' is closest in meaning to:",
                 "options": ["broken", "injured or twisted", "strengthened"],
                 "answer": "injured or twisted", "explain": "A sprained ankle is a common, twisted-joint injury, not a broken bone."},
                {"type": "mc", "q": "What can we infer is the main message of the article?",
                 "options": ["Everyone needs a gym membership", "Consistency and variety matter more than expensive equipment", "Outdoor activities are always dangerous"],
                 "answer": "Consistency and variety matter more than expensive equipment",
                 "explain": "The conclusion emphasizes consistency and a mix of low-cost activities over fancy equipment."},
                {"type": "mc", "q": "Why does the author mention both hiking and gym workouts in the conclusion?",
                 "options": ["To argue that hiking is better", "To show there are different valid paths to staying fit", "To recommend avoiding gyms entirely"],
                 "answer": "To show there are different valid paths to staying fit",
                 "explain": "The text presents both options as valid, saying the best plan is 'the one a person will actually continue to do.'"},
            ],
        },
        "vocab": {
            "bank": ["try on", "put on", "sign up for", "work out", "look for",
                     "check out", "warm up", "cool down"],
            "sentences": [
                {"s": "Can I ___ this jacket before I buy it?", "answer": ["try on"]},
                {"s": "It's cold outside, so ___ your coat before we go.", "answer": ["put on"]},
                {"s": "I want to ___ the new yoga class at the gym.", "answer": ["sign up for"]},
                {"s": "She likes to ___ at the gym three times a week.", "answer": ["work out"]},
                {"s": "We had to ___ a smaller size because the shoes were too big.", "answer": ["look for"]},
                {"s": "Please ___ before you leave the store; the cashier is over there.", "answer": ["check out"]},
                {"s": "Always ___ before you start exercising, to avoid injury.", "answer": ["warm up"]},
                {"s": "After running, it's important to ___ slowly instead of stopping suddenly.", "answer": ["cool down"]},
            ],
        },
        "grammar": {
            "mc": [
                {"q": "This jacket is _____ one in the whole store.",
                 "options": ["the most expensive", "the most expensivest", "more expensive", "expensivest"],
                 "answer": "the most expensive", "explain": "Superlative of a long adjective: the most + adjective."},
                {"q": "Of all the trainers, Mike is _____.",
                 "options": ["the best", "the goodest", "more good", "bestest"],
                 "answer": "the best", "explain": "'good' is irregular: good → better → the best."},
                {"q": "You _____ wear a helmet if you go mountain biking; it's the law in some places.",
                 "options": ["should", "have to", "could", "shouldn't"],
                 "answer": "have to", "explain": "'have to' expresses an obligation (a rule/law), not just advice."},
                {"q": "It's just a suggestion: you _____ try the spin class if you want to.",
                 "options": ["have to", "has to", "could", "must"],
                 "answer": "could", "explain": "'could' presents an option, not an obligation."},
                {"q": "These are _____ shoes I've ever tried on.",
                 "options": ["the most comfortable", "the comfortablest", "more comfortable", "most comfortablier"],
                 "answer": "the most comfortable", "explain": "Superlative of a long adjective: the most + adjective."},
                {"q": "My sister _____ work late tonight, so she can't come to the gym.",
                 "options": ["have to", "has to", "could", "should to"],
                 "answer": "has to", "explain": "Third-person singular (she) needs 'has to', not 'have to'."},
                {"q": "This store has _____ selection in town.",
                 "options": ["the biggest", "the most big", "bigger", "the most biggest"],
                 "answer": "the biggest", "explain": "'big' is a short adjective: the + adjective + -est."},
                {"q": "If you're tired, you _____ rest instead of exercising.",
                 "options": ["have to", "has to", "should", "should to"],
                 "answer": "should", "explain": "'should' gives advice; note modals are followed by the base form, never 'to'."},
            ],
            "fillin": [
                {"s": "This is _______ (cheap) pair of sandals in the store.", "answer": ["the cheapest"]},
                {"s": "This blazer is _______ (nice) one I've seen all day.", "answer": ["the nicest"]},
                {"s": "These are _______ (comfortable) running shoes I own.", "answer": ["the most comfortable"]},
                {"s": "That gym has _______ (big) pool in the city.", "answer": ["the biggest"]},
                {"s": "This is _______ (bad) haircut I've ever had!", "answer": ["the worst"]},
            ],
        },
        "writing": {
            "topics": [
                "Describe your favorite outfit and why you like to wear it.",
                "Write about a time you went shopping for something special (an interview, a party, a trip).",
                "Describe your ideal exercise routine. What activities do you do to stay fit?",
                "Write about a time you got injured or hurt while doing a sport or activity.",
            ]
        },
    },
    "B": {
        "label": "Version B — 'Getting Back in Shape' (Fitness & Shopping)",
        "listening": {
            "title": "Diego's Weekend Workout Plan",
            "audio_text": (
                "Last weekend, Diego decided it was time to get back in shape after months of "
                "working from home. On Saturday morning, he woke up early and went for a run on "
                "the track near his apartment, even though he hadn't run in a long time and his "
                "legs felt sore afterward. In the afternoon, he called his friend Paula and asked "
                "if she wanted to go bike riding with him on Sunday. Paula agreed, but she said "
                "she had to finish some work first, so they decided to meet at ten o'clock instead "
                "of nine. On Sunday morning, Diego went to a sports store to buy a helmet, because "
                "he didn't have one and he knew he should always wear one when riding a bike. At "
                "the store, a salesperson told him the store's best-selling helmet was also the "
                "lightest one they had, so Diego decided to buy that model. After that, he met "
                "Paula at the park, and they went mountain biking for almost two hours on a trail "
                "through the woods. Everything was going well until Diego hit a rock and fell off "
                "his bike, hurting his knee. Paula helped him get up, and even though his knee was "
                "a little swollen, he could still walk, so they decided he didn't have to go to "
                "the hospital. Instead, they went home, and Diego put ice on his knee and rested "
                "for the remainder of the day. Despite the small accident, Diego said it had still "
                "been one of the most active and fun weekends he'd had in months."
            ),
            "mc": [
                {"q": "What did Diego do on Saturday morning?",
                 "options": ["He went swimming", "He went for a run", "He lifted weights", "He went hiking"],
                 "answer": "He went for a run", "explain": "'he woke up early and went for a run on the track.'"},
                {"q": "Why did Diego and Paula change their meeting time?",
                 "options": ["Diego was sick", "Paula had to finish some work", "It was raining", "The park was closed"],
                 "answer": "Paula had to finish some work", "explain": "'she said she had to finish some work first.'"},
                {"q": "Why did Diego buy a helmet?",
                 "options": ["It was required to enter the park", "He knew he should always wear one when biking", "It was a gift", "His old one was stolen"],
                 "answer": "He knew he should always wear one when biking",
                 "explain": "'he knew he should always wear one when riding a bike.'"},
                {"q": "What happened to Diego during the bike ride?",
                 "options": ["He got lost", "He fell off his bike and hurt his knee", "His bike broke", "He ran out of water"],
                 "answer": "He fell off his bike and hurt his knee", "explain": "'Diego hit a rock and fell off his bike, hurting his knee.'"},
                {"q": "What did Diego do for his knee after the accident?",
                 "options": ["He went to the hospital", "He put ice on it and rested", "He kept exercising", "He ignored it"],
                 "answer": "He put ice on it and rested", "explain": "'Diego put ice on his knee and rested for the remainder of the day.'"},
            ],
            "tf": [
                {"s": "Diego went running on Saturday morning.", "answer": True,
                 "explain": "'On Saturday morning, he... went for a run.'"},
                {"s": "Diego and Paula originally planned to meet at ten o'clock.", "answer": False,
                 "explain": "They originally planned nine o'clock, then changed it to ten."},
                {"s": "The salesperson recommended the lightest helmet in the store.", "answer": True,
                 "explain": "'the store's best-selling helmet was also the lightest one they had.'"},
                {"s": "Diego had to go to the hospital because of his knee.", "answer": False,
                 "explain": "'they decided he didn't have to go to the hospital.'"},
                {"s": "Diego said the weekend was boring.", "answer": False,
                 "explain": "'it had still been one of the most active and fun weekends he'd had in months.'"},
            ],
            "order": {
                "items": [
                    ("A", "He met Paula at the park."),
                    ("B", "He put ice on his knee and rested."),
                    ("C", "Diego went for a run on the track."),
                    ("D", "He fell off his bike and hurt his knee."),
                    ("E", "He called Paula to plan a bike ride."),
                    ("F", "He bought a helmet at a sports store."),
                ],
                "correct": ["C", "E", "F", "A", "D", "B"],
            },
        },
        "reading": {
            "text": (
                "When Jennifer got a promotion that required frequent international travel, she "
                "quickly discovered that clothing customs can be very different from one country "
                "to another. In her first trip to a country with a very conservative business "
                "culture, she learned that both men and women were expected to wear formal suits "
                "every day, even during the hottest weeks of summer. Wearing anything more casual, "
                "she was told, could actually offend her business partners and make them think she "
                "wasn't taking the meetings seriously.\n\n"
                "On a later trip to a different country, Jennifer noticed that the office dress "
                "code was much more relaxed. Employees there often wore what people call 'business "
                "casual': simple slacks and a blouse or a shirt, without a jacket or a tie. "
                "However, she also learned that some clothing items, like shorts or sleeveless "
                "tops, were still considered inappropriate in an office setting, even in a country "
                "with generally liberal clothing customs.\n\n"
                "The biggest lesson Jennifer learned was that it's always a good idea to research "
                "local dress codes before packing for a business trip. She started asking local "
                "colleagues for advice or searching online for the dos and don'ts of a particular "
                "destination. This small amount of preparation helped her avoid several awkward "
                "situations, and it made her business partners feel respected because she had made "
                "an effort to follow their customs.\n\n"
                "Jennifer's company eventually created a short guide for new employees who "
                "traveled internationally, explaining the basic clothing expectations for the "
                "company's most common destinations. The guide reminded travelers that when in "
                "doubt, it's usually safer to dress more formally than necessary rather than risk "
                "looking too casual. According to the guide, a well-prepared traveler is far more "
                "likely to make a good first impression, no matter which country they are "
                "visiting."
            ),
            "questions": [
                {"type": "mc", "q": "What did Jennifer learn about the conservative country she visited?",
                 "options": ["Casual clothes were expected", "Formal suits were expected every day", "There was no dress code at all"],
                 "answer": "Formal suits were expected every day", "explain": "'both men and women were expected to wear formal suits every day.'"},
                {"type": "tfn", "q": "Wearing casual clothes in the conservative country made a good impression.",
                 "answer": "False", "explain": "'Wearing anything more casual... could actually offend her business partners.'"},
                {"type": "mc", "q": "What is 'business casual,' according to the text?",
                 "options": ["Wearing a suit and tie every day", "Simple slacks and a blouse or shirt, without a jacket or tie", "Wearing shorts and sandals"],
                 "answer": "Simple slacks and a blouse or shirt, without a jacket or tie",
                 "explain": "'business casual: simple slacks and a blouse or a shirt, without a jacket or a tie.'"},
                {"type": "tfn", "q": "Shorts and sleeveless tops were considered appropriate office wear in the more liberal country.",
                 "answer": "False", "explain": "'some clothing items, like shorts or sleeveless tops, were still considered inappropriate.'"},
                {"type": "mc", "q": "What did Jennifer start doing before her business trips?",
                 "options": ["Buying new clothes for every trip", "Researching local dress codes in advance", "Asking her boss to travel for her"],
                 "answer": "Researching local dress codes in advance",
                 "explain": "'she started asking local colleagues for advice or searching online.'"},
                {"type": "tfn", "q": "Jennifer's research helped her avoid awkward situations.",
                 "answer": "True", "explain": "'This small amount of preparation helped her avoid several awkward situations.'"},
                {"type": "tfn", "q": "The company's guide recommends dressing more casually than necessary if you're not sure.",
                 "answer": "False", "explain": "The guide says it's safer to dress 'more formally than necessary', not more casually."},
                {"type": "mc", "q": "In paragraph 3, the phrase 'dos and don'ts' is closest in meaning to:",
                 "options": ["prices and discounts", "rules about what to do and not do", "types of clothing"],
                 "answer": "rules about what to do and not do",
                 "explain": "'Dos and don'ts' refers to recommended and forbidden behaviors/customs."},
                {"type": "mc", "q": "Why do you think Jennifer's company created a guide for new employees?",
                 "options": ["To help them save money", "To help them avoid cultural misunderstandings while traveling", "To require everyone to wear the same uniform"],
                 "answer": "To help them avoid cultural misunderstandings while traveling",
                 "explain": "The guide explains clothing expectations so new travelers don't repeat Jennifer's early mistakes."},
                {"type": "mc", "q": "What is the main lesson of the passage?",
                 "options": ["Business casual is the best dress code everywhere", "Researching local customs helps travelers make a better impression", "Formal suits are always the safest choice everywhere"],
                 "answer": "Researching local customs helps travelers make a better impression",
                 "explain": "The whole passage builds toward the value of preparation and cultural awareness."},
            ],
        },
        "vocab": {
            "bank": ["try on", "put on", "take off", "sign up for", "work out",
                     "look for", "pay for", "check out"],
            "sentences": [
                {"s": "Could you ___ that sweater? I want to see how it fits you.", "answer": ["try on"]},
                {"s": "It's freezing outside, so ___ a scarf before you leave.", "answer": ["put on"]},
                {"s": "Please ___ your shoes before entering the yoga studio.", "answer": ["take off"]},
                {"s": "Did you ___ the new spin class yet?", "answer": ["sign up for"]},
                {"s": "He likes to ___ every morning before work.", "answer": ["work out"]},
                {"s": "We need to ___ a bigger tent for our camping trip.", "answer": ["look for"]},
                {"s": "How would you like to ___, cash or credit?", "answer": ["pay for"]},
                {"s": "Let's ___ before the mall closes.", "answer": ["check out"]},
            ],
        },
        "grammar": {
            "mc": [
                {"q": "This is _____ trail in the whole park.",
                 "options": ["the most difficult", "the difficultest", "more difficult", "most difficulter"],
                 "answer": "the most difficult", "explain": "Superlative of a long adjective: the most + adjective."},
                {"q": "Of all the runners, Ana is _____.",
                 "options": ["the fastest", "the most fast", "fastest more", "the fastiest"],
                 "answer": "the fastest", "explain": "'fast' is a short adjective: the + adjective + -est."},
                {"q": "You _____ wear running shoes at the gym; sandals aren't allowed.",
                 "options": ["could", "have to", "should to", "has to"],
                 "answer": "have to", "explain": "'have to' expresses a rule/obligation, not just a suggestion."},
                {"q": "It's optional, but you _____ try the new treadmill if you want.",
                 "options": ["have to", "has to", "could", "must"],
                 "answer": "could", "explain": "'could' presents an option, not an obligation."},
                {"q": "These are _____ jeans I've ever bought.",
                 "options": ["the most comfortable", "the comfortablest", "more comfortable", "most comfortablier"],
                 "answer": "the most comfortable", "explain": "Superlative of a long adjective: the most + adjective."},
                {"q": "My brother _____ work this weekend, so he can't join the hike.",
                 "options": ["have to", "has to", "could", "should to"],
                 "answer": "has to", "explain": "Third-person singular (he) needs 'has to', not 'have to'."},
                {"q": "This mall has _____ selection of shoes in the city.",
                 "options": ["the biggest", "the most big", "bigger", "the most biggest"],
                 "answer": "the biggest", "explain": "'big' is a short adjective: the + adjective + -est."},
                {"q": "If your knee hurts, you _____ stop exercising and rest.",
                 "options": ["have to", "has to", "should", "should to"],
                 "answer": "should", "explain": "'should' gives advice; modals are followed by the base form, never 'to'."},
            ],
            "fillin": [
                {"s": "This is _______ (expensive) jacket in the store.", "answer": ["the most expensive"]},
                {"s": "These are _______ (comfortable) shoes I've ever worn.", "answer": ["the most comfortable"]},
                {"s": "That gym has _______ (good) equipment in town.", "answer": ["the best"]},
                {"s": "This is _______ (bad) accident I've ever had!", "answer": ["the worst"]},
                {"s": "Of all the trails, this one is _______ (short).", "answer": ["the shortest"]},
            ],
        },
        "writing": {
            "topics": [
                "Describe a piece of clothing or an accessory that is very important to you.",
                "Write about the best or worst shopping experience you've ever had.",
                "Write about a sport or physical activity you would like to try for the first time.",
                "Describe an accident or injury you had (or imagine one) during an outdoor activity.",
            ]
        },
    },
}

CONNECTORS = [
    "first", "then", "after that", "next", "finally", "however", "because", "so",
    "also", "in addition", "on the other hand", "for example", "but", "and",
]

# ==============================================================================
# 2. UTILITIES
# ==============================================================================

def tts_button(text: str, uid: str, label: str = "▶ Play Audio"):
    """Robust HTML/JS text-to-speech button using the browser's Web Speech API.

    The narration text is placed inside a hidden element's *text content*
    (not inside a quoted JS string in an onclick attribute), which avoids the
    classic bug where quotes in the text break the surrounding HTML/JS.
    """
    text_escaped = html_lib.escape(text)
    html_code = f"""
    <div>
      <p id="tts-text-{uid}" style="display:none;">{text_escaped}</p>
      <button id="tts-play-{uid}"
        style="background:#2c3e50;color:white;border:none;padding:10px 18px;
               border-radius:8px;cursor:pointer;font-size:15px;">
        {label}
      </button>
      <button id="tts-stop-{uid}"
        style="background:#c0392b;color:white;border:none;padding:10px 14px;
               border-radius:8px;cursor:pointer;font-size:15px;margin-left:6px;">
        ⏹ Stop
      </button>
      <span id="tts-status-{uid}" style="margin-left:10px;color:#555;font-size:13px;"></span>
      <script>
        (function() {{
          var synth = window.speechSynthesis;
          var playBtn = document.getElementById("tts-play-{uid}");
          var stopBtn = document.getElementById("tts-stop-{uid}");
          var textEl = document.getElementById("tts-text-{uid}");
          var statusEl = document.getElementById("tts-status-{uid}");

          function pickVoice() {{
            var voices = synth.getVoices();
            return voices.find(function(v) {{ return v.lang === "en-US"; }}) ||
                   voices.find(function(v) {{ return v.lang && v.lang.indexOf("en") === 0; }}) ||
                   null;
          }}

          function speak() {{
            if (!synth) {{
              statusEl.textContent = "Text-to-speech is not supported in this browser.";
              return;
            }}
            synth.cancel();
            var utter = new SpeechSynthesisUtterance(textEl.textContent);
            utter.lang = "en-US";
            utter.rate = 0.92;
            utter.pitch = 1.0;
            var v = pickVoice();
            if (v) {{ utter.voice = v; }}
            utter.onstart = function() {{ statusEl.textContent = "Playing..."; }};
            utter.onend = function() {{ statusEl.textContent = "Finished."; }};
            utter.onerror = function() {{ statusEl.textContent = "Playback error. Try again."; }};
            synth.speak(utter);
          }}

          if (synth && synth.onvoiceschanged !== undefined) {{
            synth.onvoiceschanged = function() {{ /* voices ready */ }};
          }}

          playBtn.addEventListener("click", speak);
          stopBtn.addEventListener("click", function() {{
            synth.cancel();
            statusEl.textContent = "Stopped.";
          }});
        }})();
      </script>
    </div>
    """
    components.html(html_code, height=70)


def init_state():
    if "option" not in st.session_state:
        st.session_state.option = "A"
    if "print_mode" not in st.session_state:
        st.session_state.print_mode = False
    for mod in ["listening", "reading", "vocab", "grammar", "writing"]:
        for opt in ["A", "B"]:
            flag = f"{opt}_{mod}_checked"
            if flag not in st.session_state:
                st.session_state[flag] = False


def reset_answers_for_option(opt):
    prefix = f"{opt}_"
    keys_to_delete = [k for k in st.session_state.keys() if k.startswith(prefix)]
    for k in keys_to_delete:
        del st.session_state[k]
    for mod in ["listening", "reading", "vocab", "grammar", "writing"]:
        st.session_state[f"{opt}_{mod}_checked"] = False


# ==============================================================================
# 3. RENDER: LISTENING MODULE
# ==============================================================================

def render_listening(opt):
    data = CONTENT[opt]["listening"]
    st.subheader(f"🎧 Listening Comprehension — {data['title']}")
    st.caption("Click the button below to listen to the narration in English. You can play it as many times as you need.")
    tts_button(data["audio_text"], uid=f"listening_{opt}")
    with st.expander("📄 Show transcript (optional, for the teacher)"):
        st.write(data["audio_text"])

    checked = st.session_state[f"{opt}_listening_checked"]
    score, total = 0, 0

    st.markdown("#### a) Multiple Choice")
    for i, item in enumerate(data["mc"]):
        key = f"{opt}_listening_mc_{i}"
        display_opts = ["-- Select --"] + item["options"]
        sel = st.radio(f"{i+1}. {item['q']}", display_opts, key=key)
        total += 1
        if checked:
            if sel == item["answer"]:
                score += 1
                st.markdown(f"<div class='feedback-correct'>✅ Correct — {item['answer']}"
                            f"<span class='explain'>{item['explain']}</span></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='feedback-wrong'>❌ Incorrect. Correct answer: {item['answer']}"
                            f"<span class='explain'>{item['explain']}</span></div>", unsafe_allow_html=True)

    st.markdown("#### b) True / False")
    for i, item in enumerate(data["tf"]):
        key = f"{opt}_listening_tf_{i}"
        display_opts = ["-- Select --", "True", "False"]
        sel = st.radio(f"{i+1}. {item['s']}", display_opts, key=key)
        total += 1
        correct_text = "True" if item["answer"] else "False"
        if checked:
            if sel == correct_text:
                score += 1
                st.markdown(f"<div class='feedback-correct'>✅ Correct — {correct_text}"
                            f"<span class='explain'>{item['explain']}</span></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='feedback-wrong'>❌ Incorrect. Correct answer: {correct_text}"
                            f"<span class='explain'>{item['explain']}</span></div>", unsafe_allow_html=True)

    st.markdown("#### c) Put the events in chronological order")
    st.caption("Listen again if needed, then assign the correct order (position 1 = first event).")
    items = data["order"]["items"]
    n_items = len(items)
    letters = [it[0] for it in items]
    for letter, text in items:
        st.write(f"**{letter}.** {text}")
    order_answers = []
    cols = st.columns(n_items)
    for pos in range(n_items):
        with cols[pos]:
            key = f"{opt}_listening_order_{pos}"
            sel = st.selectbox(f"Position {pos+1}", ["-"] + letters, key=key)
            order_answers.append(sel)
    total += 1
    if checked:
        if order_answers == data["order"]["correct"]:
            score += 1
            st.markdown(f"<div class='feedback-correct'>✅ Correct order! "
                        f"{' → '.join(data['order']['correct'])}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='feedback-wrong'>❌ Incorrect order. Correct order: "
                        f"{' → '.join(data['order']['correct'])}</div>", unsafe_allow_html=True)

    if st.button("✅ Check Answers (Listening)", key=f"{opt}_btn_listening"):
        st.session_state[f"{opt}_listening_checked"] = True
        st.rerun()

    if checked:
        st.info(f"Listening Score: **{score} / {total}**")


# ==============================================================================
# 4. RENDER: READING MODULE
# ==============================================================================

def render_reading(opt):
    data = CONTENT[opt]["reading"]
    st.subheader("📖 Reading Comprehension")
    for para in data["text"].split("\n\n"):
        st.write(para)
    st.markdown("---")

    checked = st.session_state[f"{opt}_reading_checked"]
    score, total = 0, 0

    for i, item in enumerate(data["questions"]):
        total += 1
        key = f"{opt}_reading_q_{i}"
        if item["type"] == "mc":
            display_opts = ["-- Select --"] + item["options"]
            sel = st.radio(f"{i+1}. {item['q']}", display_opts, key=key)
        else:
            display_opts = ["-- Select --", "True", "False", "Not Mentioned"]
            sel = st.radio(f"{i+1}. {item['q']}", display_opts, key=key)
        if checked:
            if sel == item["answer"]:
                score += 1
                st.markdown(f"<div class='feedback-correct'>✅ Correct — {item['answer']}"
                            f"<span class='explain'>{item['explain']}</span></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='feedback-wrong'>❌ Incorrect. Correct answer: {item['answer']}"
                            f"<span class='explain'>{item['explain']}</span></div>", unsafe_allow_html=True)

    if st.button("✅ Check Answers (Reading)", key=f"{opt}_btn_reading"):
        st.session_state[f"{opt}_reading_checked"] = True
        st.rerun()

    if checked:
        st.info(f"Reading Score: **{score} / {total}**")


# ==============================================================================
# 5. RENDER: VOCABULARY MODULE
# ==============================================================================

def render_vocab(opt):
    data = CONTENT[opt]["vocab"]
    st.subheader("📝 Vocabulary & Expressions")
    bank_html = " &nbsp;•&nbsp; ".join([f"<b>{w}</b>" for w in data["bank"]])
    st.markdown(f"<div class='word-bank'>📦 <b>Word Bank:</b> {bank_html}</div>", unsafe_allow_html=True)
    st.caption("Complete each sentence using an exact phrase from the word bank above.")

    checked = st.session_state[f"{opt}_vocab_checked"]
    score, total = 0, 0

    for i, item in enumerate(data["sentences"]):
        total += 1
        key = f"{opt}_vocab_{i}"
        sel = st.text_input(f"{i+1}. {item['s']}", key=key, placeholder="type your answer here")
        if checked:
            correct = sel.strip().lower() in [a.lower() for a in item["answer"]]
            if correct:
                score += 1
                st.markdown(f"<div class='feedback-correct'>✅ Correct — {item['answer'][0]}</div>",
                            unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='feedback-wrong'>❌ Incorrect. Correct answer: {item['answer'][0]}</div>",
                            unsafe_allow_html=True)

    if st.button("✅ Check Answers (Vocabulary)", key=f"{opt}_btn_vocab"):
        st.session_state[f"{opt}_vocab_checked"] = True
        st.rerun()

    if checked:
        st.info(f"Vocabulary Score: **{score} / {total}**")


# ==============================================================================
# 6. RENDER: GRAMMAR MODULE
# ==============================================================================

def render_grammar(opt):
    data = CONTENT[opt]["grammar"]
    st.subheader("🔤 Grammar & Structures — Superlatives & Modals (have to / should / could)")

    checked = st.session_state[f"{opt}_grammar_checked"]
    score, total = 0, 0

    st.markdown("#### a) Multiple Choice")
    for i, item in enumerate(data["mc"]):
        total += 1
        key = f"{opt}_grammar_mc_{i}"
        display_opts = ["-- Select --"] + item["options"]
        sel = st.radio(f"{i+1}. {item['q']}", display_opts, key=key)
        if checked:
            if sel == item["answer"]:
                score += 1
                st.markdown(f"<div class='feedback-correct'>✅ Correct — {item['answer']}"
                            f"<span class='explain'>{item['explain']}</span></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='feedback-wrong'>❌ Incorrect. Correct answer: {item['answer']}"
                            f"<span class='explain'>{item['explain']}</span></div>", unsafe_allow_html=True)

    st.markdown("#### b) Complete with the correct superlative form")
    for i, item in enumerate(data["fillin"]):
        total += 1
        key = f"{opt}_grammar_fill_{i}"
        sel = st.text_input(f"{i+1}. {item['s']}", key=key, placeholder="type your answer here")
        if checked:
            correct = sel.strip().lower() in [a.lower() for a in item["answer"]]
            if correct:
                score += 1
                st.markdown(f"<div class='feedback-correct'>✅ Correct — {item['answer'][0]}</div>",
                            unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='feedback-wrong'>❌ Incorrect. Correct answer: {item['answer'][0]}</div>",
                            unsafe_allow_html=True)

    if st.button("✅ Check Answers (Grammar)", key=f"{opt}_btn_grammar"):
        st.session_state[f"{opt}_grammar_checked"] = True
        st.rerun()

    if checked:
        st.info(f"Grammar Score: **{score} / {total}**")


# ==============================================================================
# 7. RENDER: WRITING MODULE
# ==============================================================================

def render_writing(opt):
    data = CONTENT[opt]["writing"]
    st.subheader("✍️ Writing — 150 words")

    key_topic = f"{opt}_writing_topic"
    topic = st.radio("Choose ONE topic:", data["topics"], key=key_topic)

    key_text = f"{opt}_writing_text"
    text = st.text_area("Write your composition here (in English):", height=260, key=key_text)

    words = [w for w in re.split(r"\s+", text.strip()) if w]
    n_words = len(words)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Words written", n_words, delta=n_words - 150)
    with col2:
        pct = min(100, int((n_words / 150) * 100)) if n_words else 0
        st.progress(pct / 100)
        st.caption(f"{pct}% of the 150-word goal")

    if st.button("✅ Analyze my Writing", key=f"{opt}_btn_writing"):
        st.session_state[f"{opt}_writing_checked"] = True

    if st.session_state.get(f"{opt}_writing_checked"):
        found_connectors = [c for c in CONNECTORS if c in text.lower()]
        st.markdown("##### 📊 Automatic Feedback")
        if n_words == 0:
            st.markdown("<div class='feedback-wrong'>❌ You haven't written anything yet.</div>", unsafe_allow_html=True)
        elif n_words < 100:
            st.markdown(f"<div class='feedback-wrong'>⚠️ Your text has only {n_words} words. "
                        f"Try to get closer to 150 words.</div>", unsafe_allow_html=True)
        elif 100 <= n_words <= 180:
            st.markdown(f"<div class='feedback-correct'>✅ Good length: {n_words} words "
                        f"(goal: ~150).</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='feedback-wrong'>⚠️ Your text is a bit long ({n_words} words). "
                        f"Try to be more concise.</div>", unsafe_allow_html=True)

        if found_connectors:
            st.markdown(f"<div class='feedback-correct'>✅ You used {len(found_connectors)} connector(s): "
                        f"{', '.join(sorted(set(found_connectors)))}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='feedback-wrong'>⚠️ No connectors were detected (first, then, "
                        "however, because, in addition...). Try using some to better organize your ideas.</div>",
                        unsafe_allow_html=True)


# ==============================================================================
# 8. PRINTABLE VIEW
# ==============================================================================

def render_printable(opt):
    data = CONTENT[opt]
    st.warning("Printable View mode is on. Use the button below or Ctrl+P / Cmd+P to print or save as PDF.")

    print_btn_html = """
    <button onclick="window.print()"
        style="background:#27ae60;color:white;border:none;padding:12px 22px;
               border-radius:8px;cursor:pointer;font-size:16px;margin-bottom:14px;">
        🖨️ Print / Save as PDF
    </button>
    """
    components.html(print_btn_html, height=60)

    listening = data["listening"]
    reading = data["reading"]
    vocab = data["vocab"]
    grammar = data["grammar"]
    writing = data["writing"]

    html = ["<div id='printable-area' class='print-page'>"]
    html.append(f"<h1>English Exam — {data['label']}</h1>")
    html.append("<p><b>Name:</b> ______________________________ &nbsp;&nbsp; <b>Date:</b> ______________</p>")

    # Listening
    html.append("<h2>1. Listening Comprehension</h2>")
    html.append(f"<p><i>Listen to \"{listening['title']}\" and answer the questions below.</i></p>")
    html.append("<p><b>a) Multiple Choice</b></p><ol>")
    for item in listening["mc"]:
        html.append(f"<li>{item['q']}<br>")
        html.append(" &nbsp; ".join([f"( &nbsp; ) {o}" for o in item["options"]]) + "</li><br>")
    html.append("</ol>")
    html.append("<p><b>b) True / False</b></p><ol>")
    for item in listening["tf"]:
        html.append(f"<li>{item['s']} &nbsp; ( &nbsp; ) True &nbsp; ( &nbsp; ) False</li><br>")
    html.append("</ol>")
    html.append("<p><b>c) Put the events in order</b></p>")
    for letter, text in listening["order"]["items"]:
        html.append(f"<p>___ &nbsp; <b>{letter}.</b> {text}</p>")

    # Reading
    html.append("<h2>2. Reading Comprehension</h2>")
    for para in reading["text"].split("\n\n"):
        html.append(f"<p>{para}</p>")
    html.append("<ol>")
    for item in reading["questions"]:
        html.append(f"<li>{item['q']}<br>")
        if item["type"] == "mc":
            html.append(" &nbsp; ".join([f"( &nbsp; ) {o}" for o in item["options"]]) + "</li><br>")
        else:
            html.append("( &nbsp; ) True &nbsp; ( &nbsp; ) False &nbsp; ( &nbsp; ) Not Mentioned</li><br>")
    html.append("</ol>")

    # Vocabulary
    html.append("<h2>3. Vocabulary & Expressions</h2>")
    html.append(f"<p><b>Word Bank:</b> {' , '.join(vocab['bank'])}</p><ol>")
    for item in vocab["sentences"]:
        html.append(f"<li>{item['s']}</li><br>")
    html.append("</ol>")

    # Grammar
    html.append("<h2>4. Grammar — Superlatives & Modals</h2><ol>")
    for item in grammar["mc"]:
        html.append(f"<li>{item['q']}<br>")
        html.append(" &nbsp; ".join([f"( &nbsp; ) {o}" for o in item["options"]]) + "</li><br>")
    for item in grammar["fillin"]:
        html.append(f"<li>{item['s']}</li><br>")
    html.append("</ol>")

    # Writing
    html.append("<h2>5. Writing (150 words)</h2><p>Choose ONE topic:</p><ul>")
    for t in writing["topics"]:
        html.append(f"<li>{t}</li>")
    html.append("</ul>")
    html.append("<div class='answer-box'>" + "<br>".join(["&nbsp;"] * 10) + "</div>")

    html.append("</div>")
    st.markdown("\n".join(html), unsafe_allow_html=True)


# ==============================================================================
# 9. MAIN APP / SIDEBAR
# ==============================================================================

def main():
    init_state()

    with st.sidebar:
        st.title("⚙️ Exam Settings")

        chosen = st.radio(
            "Choose the exam version:",
            options=["A", "B"],
            format_func=lambda x: CONTENT[x]["label"],
            index=0 if st.session_state.option == "A" else 1,
            key="option_radio",
        )
        st.session_state.option = chosen

        st.markdown("---")
        st.session_state.print_mode = st.checkbox(
            "🖨️ Printable View / Export to PDF", value=st.session_state.print_mode
        )

        st.markdown("---")
        if st.button("🔄 Reset answers for this version"):
            reset_answers_for_option(st.session_state.option)
            st.rerun()

        st.markdown("---")
        st.caption(
            "Unit 8 — *Shopping for Clothes*  \n"
            "Unit 9 — *Fitness and Health*  \n"
            "Level: A2 / B1"
        )

    opt = st.session_state.option

    st.markdown(
        f"<div class='exam-title'><h2>🛍️🏃 English Exam — Units 8 & 9</h2>"
        f"<p>{CONTENT[opt]['label']}</p></div>",
        unsafe_allow_html=True,
    )

    if st.session_state.print_mode:
        render_printable(opt)
        return

    tabs = st.tabs(["🎧 Listening", "📖 Reading", "📝 Vocabulary", "🔤 Grammar", "✍️ Writing"])
    with tabs[0]:
        render_listening(opt)
    with tabs[1]:
        render_reading(opt)
    with tabs[2]:
        render_vocab(opt)
    with tabs[3]:
        render_grammar(opt)
    with tabs[4]:
        render_writing(opt)


if __name__ == "__main__":
    main()
