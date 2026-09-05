"""
================================================================================
 INTERACTIVE ENGLISH EXAM (A2/B1) — Unit 5 "Eating in Restaurants"
                                    & Unit 7 "Vacations and Travel"
================================================================================
Streamlit app featuring:
  - 2 completely different exam versions (Version A / Version B), chosen manually
  - Listening (Web Speech API, text-to-speech in the browser), Reading,
    Vocabulary/Phrasal Verbs, Grammar (comparatives & superlatives) and
    Writing (150 words)
  - Automatic on-screen grading (green/red feedback + grammar explanations)
  - Printable view / exportable to PDF (Ctrl+P) with no Streamlit controls
  - Answers persisted with st.session_state

Run with:  streamlit run app.py
================================================================================
"""

import html as html_lib
import re

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="English Exam · Unit 5 & 7", page_icon="✈️", layout="wide")

# ==============================================================================
# 0. GLOBAL CSS (includes print rules)
# ==============================================================================
st.markdown(
    """
    <style>
    .stApp { background-color: #fafafa; }
    .exam-title {
        background: linear-gradient(90deg,#2c3e50,#e74c3c);
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
    .print-page h2 { color:#2c3e50; margin-top:26px; border-left:6px solid #e74c3c; padding-left:10px;}
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
        "label": "Version A — 'A Trip with Surprises' (Travel & Food)",
        "listening": {
            "title": "Laura's Vacation Story",
            "audio_text": (
                "Last month, Laura went on a two-week vacation to Costa Rica. She took a direct "
                "flight from New York, and even though the flight was very long, it was quite "
                "comfortable because the airline gave her a good seat and free snacks. When she "
                "arrived, she stayed at a small hotel near the beach, and the weather was warm "
                "and sunny every day. On the first day, she went snorkeling and saw a lot of "
                "colorful fish near the coral reef. On the second day, she took a guided tour of "
                "a rainforest, where she saw monkeys and exotic birds. On the third day, "
                "something unpleasant happened: someone stole her camera at the local market "
                "while she wasn't paying attention. Luckily, her passport and money were safe in "
                "her hotel room, so it wasn't a disaster. On the fourth day, she decided to relax "
                "at the hotel pool instead of going out, because she was still a little upset "
                "about the camera. On the fifth day, she went sport fishing with a small group of "
                "tourists and caught two fish, which the hotel restaurant cooked for dinner that "
                "same night. Finally, on the last day, she packed her suitcase, checked out of "
                "the hotel early in the morning, and took a taxi to the airport. She got back "
                "home last Sunday night, tired but happy, and she already wants to go on "
                "vacation again next year."
            ),
            "mc": [
                {"q": "How long was Laura's vacation?",
                 "options": ["One week", "Two weeks", "Ten days", "One month"],
                 "answer": "Two weeks", "explain": "'Laura went on a two-week vacation to Costa Rica.'"},
                {"q": "What did the airline give her during the flight?",
                 "options": ["A blanket", "A good seat and free snacks", "A private room", "Nothing"],
                 "answer": "A good seat and free snacks", "explain": "'the airline gave her a good seat and free snacks.'"},
                {"q": "What did Laura see during the rainforest tour?",
                 "options": ["Only birds", "Monkeys and exotic birds", "A waterfall", "Wild elephants"],
                 "answer": "Monkeys and exotic birds", "explain": "'she saw monkeys and exotic birds.'"},
                {"q": "Why did Laura relax at the hotel pool on the fourth day?",
                 "options": ["It was raining", "She was tired from fishing", "She was still upset about the stolen camera", "The tour was cancelled"],
                 "answer": "She was still upset about the stolen camera",
                 "explain": "'because she was still a little upset about the camera.'"},
                {"q": "What happened to the fish Laura caught while sport fishing?",
                 "options": ["She took them home", "She released them back into the sea", "The hotel restaurant cooked them for dinner", "She gave them to a friend"],
                 "answer": "The hotel restaurant cooked them for dinner",
                 "explain": "'which the hotel restaurant cooked for dinner that same night.'"},
            ],
            "tf": [
                {"s": "Laura's vacation lasted two weeks.", "answer": True,
                 "explain": "'a two-week vacation to Costa Rica.'"},
                {"s": "The weather in Costa Rica was cold and rainy.", "answer": False,
                 "explain": "'the weather was warm and sunny every day.'"},
                {"s": "Laura lost her passport at the market.", "answer": False,
                 "explain": "It was her camera, not her passport, that was stolen."},
                {"s": "Laura went sport fishing on the fifth day.", "answer": True,
                 "explain": "'On the fifth day, she went sport fishing...'"},
                {"s": "Laura checked out of the hotel in the afternoon on the last day.", "answer": False,
                 "explain": "'checked out of the hotel early in the morning.'"},
            ],
            "order": {
                "items": [
                    ("A", "She took a guided tour of the rainforest."),
                    ("B", "She relaxed at the hotel pool."),
                    ("C", "Laura took a direct flight to Costa Rica."),
                    ("D", "She went sport fishing and caught two fish."),
                    ("E", "She went snorkeling near the coral reef."),
                    ("F", "Someone stole her camera at the market."),
                ],
                "correct": ["C", "E", "A", "F", "B", "D"],
            },
        },
        "reading": {
            "text": (
                "Last summer, the Ramirez family took an unforgettable ten-day vacation to "
                "Thailand. They flew on a direct flight that took about eighteen hours, and even "
                "though it was really long, everyone said it was pretty comfortable because the "
                "airline gave them good food and movies. When they landed, they were incredibly "
                "excited to try the local food, especially the famous street food that Thailand "
                "is known for around the world.\n\n"
                "During their trip, they visited food stands and carts everywhere. They tried "
                "spicy soups, fried noodles, and fresh fruit. The mother, Elena, loved the "
                "seafood, especially the grilled shrimp, because it was healthier than the fried "
                "dishes. The father, Carlos, was more of a meat and potatoes man, so he preferred "
                "the grilled chicken and rice, which he said was the tastiest meal of the entire "
                "trip. Their daughter, Sofia, tried a strange fruit for the first time and said it "
                "was the sweetest thing she had ever eaten.\n\n"
                "Unfortunately, not everything went perfectly, and the trip had a few hassles "
                "along the way. On the fourth day, they missed their train to another city "
                "because of terrible traffic, and Carlos got a little seasick during a boat tour "
                "to some islands. Despite these small hassles, the family agreed that this "
                "vacation was more exciting than any other trip they had taken before.\n\n"
                "By the end of the ten-day trip, the Ramirez family had eaten in more than a "
                "dozen different restaurants and food stalls, and they had tried dishes they had "
                "never even heard of before leaving home. When they finally landed back in the "
                "United States, Sofia said she already missed the smell of the spices from the "
                "night markets, and Carlos admitted that airport food back home now seemed pretty "
                "boring compared to what they had eaten in Thailand. Elena, always practical, "
                "said she had learned a few new recipes that she planned to cook at home, even "
                "though she knew they probably wouldn't taste exactly the same without the "
                "fresh, local ingredients."
            ),
            "questions": [
                {"type": "mc", "q": "How long was the flight to Thailand?",
                 "options": ["About 8 hours", "About 18 hours", "About 24 hours"],
                 "answer": "About 18 hours", "explain": "'a direct flight that took about eighteen hours.'"},
                {"type": "mc", "q": "Why did Carlos prefer the grilled chicken?",
                 "options": ["Because it was cheap", "Because he thought it was the tastiest meal", "Because it was healthy"],
                 "answer": "Because he thought it was the tastiest meal",
                 "explain": "'which he said was the tastiest meal of the entire trip.'"},
                {"type": "tfn", "q": "The family arrived in Thailand by cruise ship.",
                 "answer": "False", "explain": "They arrived by direct flight, not by ship."},
                {"type": "tfn", "q": "Elena thought seafood was healthier than fried food.",
                 "answer": "True", "explain": "'she loved the seafood... because it was healthier than the fried dishes.'"},
                {"type": "tfn", "q": "The family's trip lasted exactly ten days.",
                 "answer": "True", "explain": "'an unforgettable ten-day vacation' / 'the ten-day trip.'"},
                {"type": "mc", "q": "What happened on the fourth day?",
                 "options": ["They missed a train", "They lost their luggage", "Someone stole their money"],
                 "answer": "They missed a train", "explain": "'they missed their train to another city.'"},
                {"type": "tfn", "q": "Carlos felt seasick during a boat tour.",
                 "answer": "True", "explain": "'Carlos got a little seasick during a boat tour to some islands.'"},
                {"type": "mc", "q": "In paragraph 3, the word 'hassles' is closest in meaning to:",
                 "options": ["exciting adventures", "small problems or difficulties", "delicious meals"],
                 "answer": "small problems or difficulties",
                 "explain": "'Hassles' describes minor inconveniences, like missing a train or feeling seasick."},
                {"type": "mc", "q": "What can we infer about Sofia's feelings toward the trip, based on paragraph 4?",
                 "options": ["She was happy to return to her normal food", "She missed the food and culture of Thailand", "She didn't like Thai food at all"],
                 "answer": "She missed the food and culture of Thailand",
                 "explain": "'Sofia said she already missed the smell of the spices from the night markets.'"},
                {"type": "mc", "q": "Why does Carlos say that airport food back home 'seemed pretty boring' after the trip?",
                 "options": ["Because airport food is always bad", "Because the food in Thailand was much more flavorful and different", "Because he doesn't like airports"],
                 "answer": "Because the food in Thailand was much more flavorful and different",
                 "explain": "The comparison implies the Thai food set a much higher, more exciting standard."},
            ],
        },
        "vocab": {
            "bank": ["check in", "check out", "take off", "land", "go away", "get up",
                     "eat out", "pick up", "look for", "find out"],
            "sentences": [
                {"s": "We need to ___ at the airport two hours before the flight.", "answer": ["check in"]},
                {"s": "The plane will ___ in ten minutes, so turn off your phone.", "answer": ["take off"]},
                {"s": "After a long flight, we were happy when the plane finally ___ safely.", "answer": ["land", "landed"]},
                {"s": "On Saturdays, my family loves to ___ instead of cooking at home.", "answer": ["eat out"]},
                {"s": "We ___ from the hotel at 11:00 and took a taxi to the station.", "answer": ["checked out", "check out"]},
                {"s": "Did you ___ any souvenirs at the market?", "answer": ["pick up", "picked up"]},
                {"s": "We had to ___ a good restaurant near the hotel.", "answer": ["look for"]},
                {"s": "Did you ___ what time the tour starts tomorrow?", "answer": ["find out"]},
            ],
        },
        "grammar": {
            "mc": [
                {"q": "The cruise was _____ than the bus trip.",
                 "options": ["more relaxing", "relaxinger", "most relaxing", "more relax"],
                 "answer": "more relaxing", "explain": "Comparative of a long adjective: more + adjective + than."},
                {"q": "This is _____ restaurant in the city.",
                 "options": ["the most expensive", "the most expensivest", "most expensive", "more expensive"],
                 "answer": "the most expensive", "explain": "Superlative: the most + long adjective."},
                {"q": "Fried food is _____ than steamed food.",
                 "options": ["unhealthier", "more unhealthy", "most unhealthy", "more healthier"],
                 "answer": "more unhealthy", "explain": "'unhealthy' is a long adjective: more unhealthy. ('more healthier' is a classic double-comparative mistake.)"},
                {"q": "Which flight was _____, the morning one or the night one?",
                 "options": ["cheap", "cheaper", "the cheapest", "most cheap"],
                 "answer": "cheaper", "explain": "Comparing only 2 options requires the comparative (-er), not the superlative."},
                {"q": "That was _____ vacation I've ever had!",
                 "options": ["the best", "the goodest", "more good", "gooder"],
                 "answer": "the best", "explain": "'good' is irregular: good → better → the best."},
                {"q": "Of all the beaches we visited, this one was _____.",
                 "options": ["the most beautiful", "the beautifulest", "more beautiful", "most beautifuler"],
                 "answer": "the most beautiful", "explain": "Superlative of a long adjective: the most + adjective."},
                {"q": "My suitcase is _____ than yours.",
                 "options": ["heavier", "more heavy", "heaviest", "most heavy"],
                 "answer": "heavier", "explain": "'heavy' ends in -y: change y to i and add -er → heavier."},
                {"q": "This was _____ trip of the whole year.",
                 "options": ["the funnest", "the most fun", "more fun", "funnier"],
                 "answer": "the most fun", "explain": "'fun' as an adjective usually takes 'the most fun' in the superlative."},
            ],
            "fillin": [
                {"s": "The Greek salad is _______ (healthy) than the cheeseburger.", "answer": ["healthier"]},
                {"s": "This was _______ (scary) flight of my life!", "answer": ["the scariest"]},
                {"s": "The train was _______ (comfortable) than the bus.", "answer": ["more comfortable"]},
                {"s": "The market was _______ (crowded) than we expected.", "answer": ["more crowded"]},
                {"s": "That was _______ (relaxing) vacation I've had in years.", "answer": ["the most relaxing"]},
            ],
        },
        "writing": {
            "topics": [
                "Describe the best vacation you've ever taken. Where did you go? What did you do?",
                "Write about your favorite restaurant. What kind of food do they serve? Why do you like it?",
                "Describe a bad travel experience you had (or imagine one). What went wrong?",
                "Write about the strangest or most unusual food you have ever tried on a trip.",
            ]
        },
    },
    "B": {
        "label": "Version B — 'A Weekend in Cusco' (Travel & Food)",
        "listening": {
            "title": "Marco's Weekend Trip",
            "audio_text": (
                "Last weekend, Marco and his sister Ana went on a short trip to Cusco, Peru. "
                "They took a train instead of a bus because they wanted to see the scenery, and "
                "the train ride was really scenic, just like people said. It was quite cold, but "
                "not too uncomfortable, so they wore warm jackets the whole time. When they "
                "arrived on Friday afternoon, they checked into a small hotel near the main "
                "square and then walked around the city center for a couple of hours. On Friday "
                "night, they visited an old market and tried some traditional street food, like "
                "grilled corn and empanadas. On Saturday morning, they took a walking tour of "
                "some ancient ruins outside the city, and their guide explained a lot about local "
                "history. On Saturday night, they went to a nice restaurant and ordered a big "
                "plate of roasted beef with potatoes. It was delicious, but Ana said the portion "
                "was kind of small for the price. On Sunday morning, they woke up early to take a "
                "bus tour of the mountains, but unfortunately, the bus had mechanical problems "
                "and they had to wait two hours at the side of the road. In the end, they finally "
                "reached the mountains in the early afternoon, and they still had a great time. "
                "They agreed it was one of their favorite weekends of the year, even with the bus "
                "delay."
            ),
            "mc": [
                {"q": "Why did they choose the train instead of the bus?",
                 "options": ["It was faster", "It was cheaper", "They wanted to see the scenery", "It was more comfortable"],
                 "answer": "They wanted to see the scenery", "explain": "'they took a train ... because they wanted to see the scenery.'"},
                {"q": "What did they do right after arriving on Friday afternoon?",
                 "options": ["They went straight to bed", "They walked around the city center", "They took a bus tour", "They went sport fishing"],
                 "answer": "They walked around the city center", "explain": "'they checked into a small hotel... and then walked around the city center.'"},
                {"q": "What did they eat on Saturday night?",
                 "options": ["Grilled corn", "Roasted beef with potatoes", "Empanadas", "Seafood"],
                 "answer": "Roasted beef with potatoes", "explain": "'they went to a nice restaurant and ordered a big plate of roasted beef with potatoes.'"},
                {"q": "What went wrong on Sunday?",
                 "options": ["They missed the bus", "The bus had mechanical problems", "It rained all day", "Someone stole their bags"],
                 "answer": "The bus had mechanical problems", "explain": "'the bus had mechanical problems and they had to wait two hours.'"},
                {"q": "When did they finally reach the mountains?",
                 "options": ["Sunday morning", "Sunday early afternoon", "Saturday night", "Monday"],
                 "answer": "Sunday early afternoon", "explain": "'they finally reached the mountains in the early afternoon.'"},
            ],
            "tf": [
                {"s": "Marco and Ana traveled to Cusco by plane.", "answer": False,
                 "explain": "They traveled by train ('They took a train...')."},
                {"s": "Ana thought the restaurant portion was small.", "answer": True,
                 "explain": "'Ana said the portion was kind of small for the price.'"},
                {"s": "They had to wait two hours because of a mechanical problem.", "answer": True,
                 "explain": "'the bus had mechanical problems and they had to wait two hours.'"},
                {"s": "They took a walking tour of ancient ruins on Saturday morning.", "answer": True,
                 "explain": "'On Saturday morning, they took a walking tour of some ancient ruins.'"},
                {"s": "They never reached the mountains because of the bus problem.", "answer": False,
                 "explain": "'they finally reached the mountains in the early afternoon.'"},
            ],
            "order": {
                "items": [
                    ("A", "They had dinner at a restaurant on Saturday night."),
                    ("B", "The bus had mechanical problems."),
                    ("C", "Marco and Ana took a scenic train to Cusco."),
                    ("D", "They woke up early on Sunday for a bus tour."),
                    ("E", "They visited an old market and tried street food."),
                    ("F", "They took a walking tour of ancient ruins."),
                ],
                "correct": ["C", "E", "F", "A", "D", "B"],
            },
        },
        "reading": {
            "text": (
                "Many people around the world are changing the way they cook and eat at home. In "
                "the past, families spent hours boiling, stewing, or roasting big meals every "
                "single day. Today, however, more people prefer quick methods like sautéing or "
                "steaming because they don't have much free time. Some people say that steamed "
                "and grilled food is healthier than fried food, so they are trying to eat fewer "
                "fried dishes and more vegetables.\n\n"
                "At the same time, eating out has become more popular than ever, especially in "
                "big cities. Restaurants now offer everything from simple sandwiches to fancy "
                "entrées with fresh seafood and dairy products. Some restaurants are famous for "
                "their desserts, like chocolate cake or apple pie, while others are known for "
                "healthy salads with lots of fruits and vegetables. Many customers say that "
                "eating at a good restaurant is more relaxing than cooking after a long day at "
                "work.\n\n"
                "Nevertheless, cooking at home still has its advantages. It's usually cheaper "
                "than eating out, and you can control exactly what goes into your food, like how "
                "much salt or sugar you add. Nutritionists often say that homemade meals, "
                "especially grilled or steamed dishes, are the healthiest option in the long run. "
                "In the end, the best solution for most people is a balance: cooking at home most "
                "days and eating out as a special treat.\n\n"
                "Interestingly, food trends often move in the opposite direction as well. Some "
                "chefs who used to work in fancy restaurants are now choosing to open small "
                "street-food stalls instead, because they enjoy the fast pace and the direct "
                "contact with customers. They say that cooking street food requires just as much "
                "skill as preparing a five-course meal, even though the ingredients might be "
                "simpler and the prices much lower. This shows that in the modern food world, "
                "there isn't only one 'right' way to cook or eat — there are many different paths "
                "that all lead to delicious results."
            ),
            "questions": [
                {"type": "mc", "q": "What cooking methods do more people prefer today?",
                 "options": ["Boiling and stewing", "Sautéing and steaming", "Frying and roasting"],
                 "answer": "Sautéing and steaming", "explain": "'more people prefer quick methods like sautéing or steaming.'"},
                {"type": "tfn", "q": "Fried food is considered healthier than steamed food.",
                 "answer": "False", "explain": "The text says the opposite: steamed/grilled food is healthier."},
                {"type": "tfn", "q": "Restaurants only serve desserts.",
                 "answer": "False", "explain": "They offer sandwiches, entrées, seafood, salads, desserts, etc."},
                {"type": "tfn", "q": "Some chefs left fancy restaurants to open street-food stalls.",
                 "answer": "True", "explain": "'Some chefs who used to work in fancy restaurants are now choosing to open small street-food stalls.'"},
                {"type": "mc", "q": "According to the text, what is one advantage of cooking at home?",
                 "options": ["It's always faster", "It's usually cheaper", "It tastes better"],
                 "answer": "It's usually cheaper", "explain": "'It's usually cheaper than eating out.'"},
                {"type": "tfn", "q": "Nutritionists say fried homemade meals are the healthiest option.",
                 "answer": "False", "explain": "They say grilled or steamed dishes are the healthiest, not fried ones."},
                {"type": "mc", "q": "What is the 'best solution' mentioned in the text?",
                 "options": ["Eating out every day", "A balance of cooking and eating out", "Only cooking at home"],
                 "answer": "A balance of cooking and eating out", "explain": "'a balance: cooking at home most days and eating out as a special treat.'"},
                {"type": "mc", "q": "In paragraph 3, the word 'advantages' is closest in meaning to:",
                 "options": ["problems", "benefits", "recipes"],
                 "answer": "benefits", "explain": "'Advantages' means positive points or benefits of something."},
                {"type": "mc", "q": "Why do some chefs think street food 'requires just as much skill' as fine dining?",
                 "options": ["Because street food is always more expensive", "Because making good food fast and simple is still a skillful process", "Because street food uses fancier ingredients"],
                 "answer": "Because making good food fast and simple is still a skillful process",
                 "explain": "The text contrasts simpler ingredients/lower prices with the same level of skill required."},
                {"type": "mc", "q": "What is the main idea of the whole passage?",
                 "options": ["Cooking at home is always better than eating out", "There are many valid ways to cook and eat, each with pros and cons", "Street food is unhealthy and should be avoided"],
                 "answer": "There are many valid ways to cook and eat, each with pros and cons",
                 "explain": "The passage compares home cooking, restaurants, and street food without declaring one absolute winner."},
            ],
        },
        "vocab": {
            "bank": ["wake up", "get back", "run out (of)", "go out", "find out",
                     "give up", "look for", "turn on"],
            "sentences": [
                {"s": "We ___ at 5 a.m. to catch our flight.", "answer": ["woke up"]},
                {"s": "When did you ___ from your trip?", "answer": ["get back", "got back"]},
                {"s": "We ___ of clean clothes on the last day of the trip.", "answer": ["ran out"]},
                {"s": "Let's ___ for dinner tonight instead of cooking.", "answer": ["go out"]},
                {"s": "Did you ___ what happened to your luggage?", "answer": ["find out"]},
                {"s": "I don't want to ___ my seat, even if they offer a voucher.", "answer": ["give up"]},
                {"s": "We had to ___ a new hotel because ours was fully booked.", "answer": ["look for"]},
                {"s": "Please ___ the air conditioner; it's really hot in here.", "answer": ["turn on"]},
            ],
        },
        "grammar": {
            "mc": [
                {"q": "This soup is _____ than that one.",
                 "options": ["spicier", "more spicy", "spicyer", "most spicy"],
                 "answer": "spicier", "explain": "'spicy' ends in -y: change y to i and add -er → spicier."},
                {"q": "She had _____ vacation of her whole life.",
                 "options": ["the most amazing", "the amazingest", "more amazing", "most amazinger"],
                 "answer": "the most amazing", "explain": "Superlative of a long adjective: the most + adjective."},
                {"q": "The seafood dish is _____ than the meat dish.",
                 "options": ["more expensiver", "more expensive", "expensiver", "most expensive"],
                 "answer": "more expensive", "explain": "Long adjective: more + adjective + than (never 'more expensiver')."},
                {"q": "Which trip was _____, the one to Peru or the one to Brazil?",
                 "options": ["longer", "more long", "the longest", "long"],
                 "answer": "longer", "explain": "Comparing 2 things requires the comparative: long → longer."},
                {"q": "That was _____ meal I've ever eaten!",
                 "options": ["worse", "the worst", "more bad", "badder"],
                 "answer": "the worst", "explain": "'bad' is irregular: bad → worse → the worst."},
                {"q": "Of all the dishes on the menu, this one is _____.",
                 "options": ["the spiciest", "the most spicy", "spicier", "more spiciest"],
                 "answer": "the spiciest", "explain": "'spicy' ends in -y: the + adjective(y→i) + -est → the spiciest."},
                {"q": "My meal was _____ than his.",
                 "options": ["tastier", "more tasty", "most tasty", "tastiest"],
                 "answer": "tastier", "explain": "'tasty' ends in -y: change y to i and add -er → tastier."},
                {"q": "This was _____ restaurant we've ever visited.",
                 "options": ["the worst", "the baddest", "more bad", "worse"],
                 "answer": "the worst", "explain": "'bad' is irregular: bad → worse → the worst."},
            ],
            "fillin": [
                {"s": "This restaurant is _______ (good) than the one downtown.", "answer": ["better"]},
                {"s": "That was _______ (bumpy) flight I've ever taken!", "answer": ["the bumpiest"]},
                {"s": "Homemade food is usually _______ (healthy) than fast food.", "answer": ["healthier"]},
                {"s": "The portions here are _______ (small) than at the other restaurant.", "answer": ["smaller"]},
                {"s": "That was _______ (delicious) meal I've had this year.", "answer": ["the most delicious"]},
            ],
        },
        "writing": {
            "topics": [
                "Describe your ideal vacation destination and why you'd like to go there.",
                "Write about a meal you cooked or ate that you'll never forget.",
                "Compare eating at home vs. eating at a restaurant. Which do you prefer and why?",
                "Write a short review of a restaurant you visited recently, as if you were posting it online.",
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
    classic bug where apostrophes/quotes in the text break the HTML/JS.
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

          // Some browsers load voices asynchronously.
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
# 5. RENDER: VOCABULARY / PHRASAL VERBS MODULE
# ==============================================================================

def render_vocab(opt):
    data = CONTENT[opt]["vocab"]
    st.subheader("📝 Vocabulary & Phrasal Verbs")
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
    st.subheader("🔤 Grammar & Structures — Comparatives & Superlatives")

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

    st.markdown("#### b) Complete with the correct comparative/superlative form")
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
    html.append("<h2>3. Vocabulary & Phrasal Verbs</h2>")
    html.append(f"<p><b>Word Bank:</b> {' , '.join(vocab['bank'])}</p><ol>")
    for item in vocab["sentences"]:
        html.append(f"<li>{item['s']}</li><br>")
    html.append("</ol>")

    # Grammar
    html.append("<h2>4. Grammar — Comparatives & Superlatives</h2><ol>")
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
            "Unit 5 — *Eating in Restaurants*  \n"
            "Unit 7 — *Vacations and Travel*  \n"
            "Level: A2 / B1"
        )

    opt = st.session_state.option

    st.markdown(
        f"<div class='exam-title'><h2>✈️🍽️ English Exam — Units 5 & 7</h2>"
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
