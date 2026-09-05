"""
================================================================================
 EXAMEN INTERACTIVO DE INGLÉS (A2/B1) — Unit 5 "Eating in Restaurants"
                                        & Unit 7 "Vacations and Travel"
================================================================================
App en Streamlit con:
  - 2 modelos de examen totalmente distintos (Opción A / Opción B) + modo aleatorio
  - Listening (Web Speech API), Reading, Vocabulary/Phrasal Verbs, Grammar
    (comparatives & superlatives) y Writing (150 palabras)
  - Corrección automática en pantalla (verde/rojo + explicación)
  - Vista imprimible / exportable a PDF (Ctrl+P) sin controles de Streamlit
  - Persistencia de respuestas con st.session_state

Ejecutar con:  streamlit run app.py
================================================================================
"""

import json
import random
import re

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="English Exam · Unit 5 & 7", page_icon="✈️", layout="wide")

# ==============================================================================
# 0. CSS GLOBAL (incluye reglas de impresión)
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
    .blank-line { display:inline-block; border-bottom:1px solid #333; min-width:220px; height:18px; }
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
# 1. CONTENIDO DE LOS DOS MODELOS DE EXAMEN
# ==============================================================================

CONTENT = {
    "A": {
        "label": "Opción A — 'A Trip with Surprises' (Travel & Food)",
        "listening": {
            "title": "Laura's Vacation Story",
            "audio_text": (
                "Last month, Laura went on a vacation to Costa Rica. She took a direct flight "
                "from New York, and the flight was very long but quite comfortable. When she "
                "arrived, she stayed at a small hotel near the beach. On the first day, she went "
                "snorkeling and saw a lot of fish. On the second day, she took a tour of a "
                "rainforest. Unfortunately, on the third day, someone stole her camera at the "
                "market. Luckily, her passport and money were safe in her hotel room. She was "
                "upset, but she said the trip was still amazing. She got back home last Sunday, "
                "and she already wants to go on vacation again."
            ),
            "mc": [
                {
                    "q": "What kind of flight did Laura take?",
                    "options": ["A non-stop flight", "A flight with two stops", "A bus", "A cruise"],
                    "answer": "A non-stop flight",
                    "explain": "El texto dice 'She took a direct flight' = non-stop flight.",
                },
                {
                    "q": "How was the flight?",
                    "options": ["Short and scary", "Long but comfortable", "Short and bumpy", "Long and boring"],
                    "answer": "Long but comfortable",
                    "explain": "'very long but quite comfortable'.",
                },
                {
                    "q": "What did someone steal from Laura?",
                    "options": ["Her passport", "Her money", "Her camera", "Her luggage"],
                    "answer": "Her camera",
                    "explain": "'someone stole her camera at the market'.",
                },
            ],
            "tf": [
                {"s": "Laura went to Costa Rica last month.", "answer": True,
                 "explain": "'Last month, Laura went on a vacation to Costa Rica.'"},
                {"s": "She flew with a stopover (a flight with a stop).", "answer": False,
                 "explain": "Fue un vuelo directo (non-stop / direct flight)."},
                {"s": "Laura's passport was also stolen.", "answer": False,
                 "explain": "'her passport and money were safe in her hotel room.'"},
            ],
            "order": {
                "items": [
                    ("A", "She went snorkeling and saw a lot of fish."),
                    ("B", "Someone stole her camera at the market."),
                    ("C", "Laura took a direct flight to Costa Rica."),
                    ("D", "She took a tour of the rainforest."),
                    ("E", "She checked into a small hotel near the beach."),
                ],
                "correct": ["C", "E", "A", "D", "B"],
            },
        },
        "reading": {
            "text": (
                "Last summer, the Ramirez family took an unforgettable vacation to Thailand. "
                "They flew on a direct flight that took about eighteen hours, and even though it "
                "was really long, everyone said it was pretty comfortable because the airline gave "
                "them good food and movies. When they landed, they were incredibly excited to try "
                "the local food, especially the famous street food that Thailand is known for "
                "around the world.\n\n"
                "During their trip, they visited food stands and carts everywhere. They tried "
                "spicy soups, fried noodles, and fresh fruit. The mother, Elena, loved the "
                "seafood, especially the grilled shrimp, because it was healthier than the fried "
                "dishes. The father, Carlos, was more of a meat and potatoes man, so he preferred "
                "the grilled chicken and rice, which he said was the tastiest meal of the entire "
                "trip. Their daughter, Sofia, tried a strange fruit for the first time and said it "
                "was the sweetest thing she had ever eaten.\n\n"
                "Unfortunately, not everything went perfectly. On the fourth day, they missed "
                "their train to another city because of terrible traffic, and Carlos got a little "
                "seasick during a boat tour to some islands. Despite these small hassles, the "
                "family agreed that this vacation was more exciting than any other trip they had "
                "taken before, and they can't wait to go back."
            ),
            "questions": [
                {"type": "mc", "q": "How long was the flight to Thailand?",
                 "options": ["About 8 hours", "About 18 hours", "About 24 hours"],
                 "answer": "About 18 hours", "explain": "'a direct flight that took about eighteen hours'."},
                {"type": "mc", "q": "Why did Carlos prefer the grilled chicken?",
                 "options": ["Because it was cheap", "Because he thought it was the tastiest meal", "Because it was healthy"],
                 "answer": "Because he thought it was the tastiest meal",
                 "explain": "'which he said was the tastiest meal of the entire trip.'"},
                {"type": "tfn", "q": "The family arrived in Thailand by cruise ship.",
                 "answer": "False", "explain": "Llegaron en avión (direct flight)."},
                {"type": "tfn", "q": "Elena thought seafood was healthier than fried food.",
                 "answer": "True", "explain": "'she loved the seafood... because it was healthier than the fried dishes.'"},
                {"type": "tfn", "q": "Sofia didn't like trying new fruit.",
                 "answer": "False", "explain": "Dijo que era 'the sweetest thing she had ever eaten', algo positivo."},
                {"type": "tfn", "q": "The family stayed in Thailand for two weeks.",
                 "answer": "Not Mentioned", "explain": "El texto nunca menciona cuántos días/semanas duró el viaje."},
                {"type": "mc", "q": "What happened on the fourth day?",
                 "options": ["They missed a train", "They lost their luggage", "Someone stole their money"],
                 "answer": "They missed a train", "explain": "'they missed their train to another city'."},
                {"type": "tfn", "q": "Carlos felt seasick during a boat tour.",
                 "answer": "True", "explain": "'Carlos got a little seasick during a boat tour to some islands.'"},
            ],
        },
        "vocab": {
            "bank": ["check in", "check out", "take off", "land", "go away", "get up", "eat out", "pick up"],
            "sentences": [
                {"s": "We need to ___ at the airport two hours before the flight.", "answer": ["check in"]},
                {"s": "The plane will ___ in ten minutes, so turn off your phone.", "answer": ["take off"]},
                {"s": "After a long flight, we were happy when the plane finally ___ safely.", "answer": ["land", "landed"]},
                {"s": "On Saturdays, my family loves to ___ instead of cooking at home.", "answer": ["eat out"]},
                {"s": "We ___ from the hotel at 11:00 and took a taxi to the station.", "answer": ["checked out", "check out"]},
                {"s": "Did you ___ any souvenirs at the market?", "answer": ["pick up", "picked up"]},
            ],
        },
        "grammar": {
            "mc": [
                {"q": "The cruise was _____ than the bus trip.",
                 "options": ["more relaxing", "relaxinger", "most relaxing", "more relax"],
                 "answer": "more relaxing", "explain": "Comparativo de adjetivo largo: more + adjetivo + than."},
                {"q": "This is _____ restaurant in the city.",
                 "options": ["the most expensive", "the most expensivest", "most expensive", "more expensive"],
                 "answer": "the most expensive", "explain": "Superlativo: the most + adjetivo largo."},
                {"q": "Fried food is _____ than steamed food.",
                 "options": ["unhealthier", "more unhealthy", "most unhealthy", "more healthier"],
                 "answer": "more unhealthy", "explain": "'unhealthy' es un adjetivo largo: more unhealthy. ('more healthier' es un doble comparativo, error clásico)."},
                {"q": "Which flight was _____, the morning one or the night one?",
                 "options": ["cheap", "cheaper", "the cheapest", "most cheap"],
                 "answer": "cheaper", "explain": "Comparando solo 2 opciones se usa el comparativo (-er), no el superlativo."},
                {"q": "That was _____ vacation I've ever had!",
                 "options": ["the best", "the goodest", "more good", "gooder"],
                 "answer": "the best", "explain": "'good' es irregular: good → better → the best."},
            ],
            "fillin": [
                {"s": "The Greek salad is _______ (healthy) than the cheeseburger.", "answer": ["healthier"]},
                {"s": "This was _______ (scary) flight of my life!", "answer": ["the scariest"]},
                {"s": "The train was _______ (comfortable) than the bus.", "answer": ["more comfortable"]},
            ],
        },
        "writing": {
            "topics": [
                "Describe the best vacation you've ever taken. Where did you go? What did you do?",
                "Write about your favorite restaurant. What kind of food do they serve? Why do you like it?",
                "Describe a bad travel experience you had (or imagine one). What went wrong?",
            ]
        },
    },
    "B": {
        "label": "Opción B — 'A Weekend in Cusco' (Travel & Food)",
        "listening": {
            "title": "Marco's Weekend Trip",
            "audio_text": (
                "Last weekend, Marco and his sister Ana went on a short trip to Cusco, Peru. "
                "They took a train instead of a bus because they wanted to see the scenery, and "
                "the train ride was really scenic, just like people said. It was quite cold, but "
                "not too uncomfortable. When they arrived, they visited an old market and tried "
                "some traditional street food, like grilled corn and empanadas. On Saturday "
                "night, they went to a restaurant and ordered a big plate of roasted beef with "
                "potatoes. It was delicious, but Ana said the portion was kind of small for the "
                "price. On Sunday morning, they woke up early to take a bus tour of the "
                "mountains, but unfortunately, the bus had mechanical problems and they had to "
                "wait two hours. In the end, they still had a great time and said it was one of "
                "their favorite weekends of the year."
            ),
            "mc": [
                {
                    "q": "Why did they choose the train instead of the bus?",
                    "options": ["It was faster", "It was cheaper", "They wanted to see the scenery", "It was more comfortable"],
                    "answer": "They wanted to see the scenery",
                    "explain": "'they took a train ... because they wanted to see the scenery'.",
                },
                {
                    "q": "What did they eat on Saturday night?",
                    "options": ["Grilled corn", "Roasted beef with potatoes", "Empanadas", "Seafood"],
                    "answer": "Roasted beef with potatoes",
                    "explain": "'they went to a restaurant and ordered a big plate of roasted beef with potatoes.'",
                },
                {
                    "q": "What went wrong on Sunday?",
                    "options": ["They missed the bus", "The bus had mechanical problems", "It rained all day", "Someone stole their bags"],
                    "answer": "The bus had mechanical problems",
                    "explain": "'the bus had mechanical problems and they had to wait two hours.'",
                },
            ],
            "tf": [
                {"s": "Marco and Ana traveled to Cusco by plane.", "answer": False,
                 "explain": "Viajaron en tren ('They took a train...')."},
                {"s": "Ana thought the restaurant portion was small.", "answer": True,
                 "explain": "'Ana said the portion was kind of small for the price.'"},
                {"s": "They had to wait two hours because of a mechanical problem.", "answer": True,
                 "explain": "'the bus had mechanical problems and they had to wait two hours.'"},
            ],
            "order": {
                "items": [
                    ("A", "They had dinner at a restaurant on Saturday night."),
                    ("B", "The bus had mechanical problems."),
                    ("C", "Marco and Ana took a scenic train to Cusco."),
                    ("D", "They woke up early on Sunday for a bus tour."),
                    ("E", "They visited an old market and tried street food."),
                ],
                "correct": ["C", "E", "A", "D", "B"],
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
                "days and eating out as a special treat."
            ),
            "questions": [
                {"type": "mc", "q": "What cooking methods do more people prefer today?",
                 "options": ["Boiling and stewing", "Sautéing and steaming", "Frying and roasting"],
                 "answer": "Sautéing and steaming", "explain": "'more people prefer quick methods like sautéing or steaming'."},
                {"type": "tfn", "q": "Fried food is considered healthier than steamed food.",
                 "answer": "False", "explain": "El texto dice lo contrario: steamed/grilled food es más saludable."},
                {"type": "tfn", "q": "Restaurants only serve desserts.",
                 "answer": "False", "explain": "Ofrecen sándwiches, entrées, mariscos, ensaladas, postres, etc."},
                {"type": "tfn", "q": "Eating out is more popular in small towns than in big cities.",
                 "answer": "Not Mentioned", "explain": "El texto solo menciona 'especially in big cities', no compara con pueblos pequeños."},
                {"type": "mc", "q": "According to the text, what is one advantage of cooking at home?",
                 "options": ["It's always faster", "It's usually cheaper", "It tastes better"],
                 "answer": "It's usually cheaper", "explain": "'It's usually cheaper than eating out'."},
                {"type": "tfn", "q": "Nutritionists say fried homemade meals are the healthiest option.",
                 "answer": "False", "explain": "Dicen que las comidas 'grilled or steamed' son las más saludables, no las fritas."},
                {"type": "mc", "q": "What is the 'best solution' mentioned in the text?",
                 "options": ["Eating out every day", "A balance of cooking and eating out", "Only cooking at home"],
                 "answer": "A balance of cooking and eating out", "explain": "'a balance: cooking at home most days and eating out as a special treat.'"},
            ],
        },
        "vocab": {
            "bank": ["wake up", "get back", "run out (of)", "go out", "find out", "give up"],
            "sentences": [
                {"s": "We ___ at 5 a.m. to catch our flight.", "answer": ["woke up"]},
                {"s": "When did you ___ from your trip?", "answer": ["get back", "got back"]},
                {"s": "We ___ of clean clothes on the last day of the trip.", "answer": ["ran out"]},
                {"s": "Let's ___ for dinner tonight instead of cooking.", "answer": ["go out"]},
                {"s": "Did you ___ what happened to your luggage?", "answer": ["find out"]},
                {"s": "I don't want to ___ my seat, even if they offer a voucher.", "answer": ["give up"]},
            ],
        },
        "grammar": {
            "mc": [
                {"q": "This soup is _____ than that one.",
                 "options": ["spicier", "more spicy", "spicyer", "most spicy"],
                 "answer": "spicier", "explain": "'spicy' termina en -y: se cambia a -ier (spicy → spicier)."},
                {"q": "She had _____ vacation of her whole life.",
                 "options": ["the most amazing", "the amazingest", "more amazing", "most amazinger"],
                 "answer": "the most amazing", "explain": "Superlativo de adjetivo largo: the most + adjetivo."},
                {"q": "The seafood dish is _____ than the meat dish.",
                 "options": ["more expensiver", "more expensive", "expensiver", "most expensive"],
                 "answer": "more expensive", "explain": "Adjetivo largo: more + adjetivo + than (nunca 'more expensiver')."},
                {"q": "Which trip was _____, the one to Peru or the one to Brazil?",
                 "options": ["longer", "more long", "the longest", "long"],
                 "answer": "longer", "explain": "Comparando 2 cosas se usa el comparativo: long → longer."},
                {"q": "That was _____ meal I've ever eaten!",
                 "options": ["worse", "the worst", "more bad", "badder"],
                 "answer": "the worst", "explain": "'bad' es irregular: bad → worse → the worst."},
            ],
            "fillin": [
                {"s": "This restaurant is _______ (good) than the one downtown.", "answer": ["better"]},
                {"s": "That was _______ (bumpy) flight I've ever taken!", "answer": ["the bumpiest"]},
                {"s": "Homemade food is usually _______ (healthy) than fast food.", "answer": ["healthier"]},
            ],
        },
        "writing": {
            "topics": [
                "Describe your ideal vacation destination and why you'd like to go there.",
                "Write about a meal you cooked or ate that you'll never forget.",
                "Compare eating at home vs. eating at a restaurant. Which do you prefer and why?",
            ]
        },
    },
}

CONNECTORS = [
    "first", "then", "after that", "next", "finally", "however", "because", "so",
    "also", "in addition", "on the other hand", "for example", "but", "and",
]

# ==============================================================================
# 2. UTILIDADES
# ==============================================================================

def tts_button(text: str, label: str = "🔊 Escuchar / Play audio"):
    """Botón HTML/JS que reproduce texto usando la Web Speech API del navegador."""
    safe_text = json.dumps(text)
    html_code = f"""
    <div>
      <button
        onclick="window.speechSynthesis.cancel();
                 var u = new SpeechSynthesisUtterance({safe_text});
                 u.lang='en-US'; u.rate=0.95;
                 window.speechSynthesis.speak(u);"
        style="background:#2c3e50;color:white;border:none;padding:10px 18px;
               border-radius:8px;cursor:pointer;font-size:15px;">
        {label}
      </button>
      <button
        onclick="window.speechSynthesis.cancel();"
        style="background:#c0392b;color:white;border:none;padding:10px 14px;
               border-radius:8px;cursor:pointer;font-size:15px;margin-left:6px;">
        ⏹ Detener
      </button>
    </div>
    """
    components.html(html_code, height=60)


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
# 3. RENDER: MÓDULO LISTENING
# ==============================================================================

def render_listening(opt):
    data = CONTENT[opt]["listening"]
    st.subheader(f"🎧 Listening Comprehension — {data['title']}")
    st.caption("Presiona el botón para escuchar la narración en inglés (voz sintetizada del navegador).")
    tts_button(data["audio_text"])
    with st.expander("📄 Ver transcripción (opcional, para el profesor)"):
        st.write(data["audio_text"])

    checked = st.session_state[f"{opt}_listening_checked"]
    score, total = 0, 0

    st.markdown("#### a) Selección múltiple")
    for i, item in enumerate(data["mc"]):
        key = f"{opt}_listening_mc_{i}"
        display_opts = ["-- Selecciona --"] + item["options"]
        sel = st.radio(f"{i+1}. {item['q']}", display_opts, key=key)
        total += 1
        if checked:
            if sel == item["answer"]:
                score += 1
                st.markdown(f"<div class='feedback-correct'>✅ Correcto — {item['answer']}"
                            f"<span class='explain'>{item['explain']}</span></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='feedback-wrong'>❌ Incorrecto. Respuesta correcta: {item['answer']}"
                            f"<span class='explain'>{item['explain']}</span></div>", unsafe_allow_html=True)

    st.markdown("#### b) Verdadero / Falso (True / False)")
    for i, item in enumerate(data["tf"]):
        key = f"{opt}_listening_tf_{i}"
        display_opts = ["-- Selecciona --", "True", "False"]
        sel = st.radio(f"{i+1}. {item['s']}", display_opts, key=key)
        total += 1
        correct_text = "True" if item["answer"] else "False"
        if checked:
            if sel == correct_text:
                score += 1
                st.markdown(f"<div class='feedback-correct'>✅ Correcto — {correct_text}"
                            f"<span class='explain'>{item['explain']}</span></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='feedback-wrong'>❌ Incorrecto. Respuesta correcta: {correct_text}"
                            f"<span class='explain'>{item['explain']}</span></div>", unsafe_allow_html=True)

    st.markdown("#### c) Ordena los eventos cronológicamente")
    st.caption("Escucha de nuevo si es necesario y asigna el orden correcto (1 = primero, 5 = último).")
    items = data["order"]["items"]
    for letter, text in items:
        st.write(f"**{letter}.** {text}")
    order_answers = []
    cols = st.columns(5)
    for pos in range(5):
        with cols[pos]:
            key = f"{opt}_listening_order_{pos}"
            sel = st.selectbox(f"Posición {pos+1}", ["-", "A", "B", "C", "D", "E"], key=key)
            order_answers.append(sel)
    total += 1
    if checked:
        if order_answers == data["order"]["correct"]:
            score += 1
            st.markdown(f"<div class='feedback-correct'>✅ ¡Orden correcto! "
                        f"{' → '.join(data['order']['correct'])}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='feedback-wrong'>❌ Orden incorrecto. Orden correcto: "
                        f"{' → '.join(data['order']['correct'])}</div>", unsafe_allow_html=True)

    if st.button("✅ Comprobar Respuestas (Listening)", key=f"{opt}_btn_listening"):
        st.session_state[f"{opt}_listening_checked"] = True
        st.rerun()

    if checked:
        st.info(f"Puntaje Listening: **{score} / {total}**")


# ==============================================================================
# 4. RENDER: MÓDULO READING
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
            display_opts = ["-- Selecciona --"] + item["options"]
            sel = st.radio(f"{i+1}. {item['q']}", display_opts, key=key)
        else:
            display_opts = ["-- Selecciona --", "True", "False", "Not Mentioned"]
            sel = st.radio(f"{i+1}. {item['q']}", display_opts, key=key)
        if checked:
            if sel == item["answer"]:
                score += 1
                st.markdown(f"<div class='feedback-correct'>✅ Correcto — {item['answer']}"
                            f"<span class='explain'>{item['explain']}</span></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='feedback-wrong'>❌ Incorrecto. Respuesta correcta: {item['answer']}"
                            f"<span class='explain'>{item['explain']}</span></div>", unsafe_allow_html=True)

    if st.button("✅ Comprobar Respuestas (Reading)", key=f"{opt}_btn_reading"):
        st.session_state[f"{opt}_reading_checked"] = True
        st.rerun()

    if checked:
        st.info(f"Puntaje Reading: **{score} / {total}**")


# ==============================================================================
# 5. RENDER: MÓDULO VOCABULARY / PHRASAL VERBS
# ==============================================================================

def render_vocab(opt):
    data = CONTENT[opt]["vocab"]
    st.subheader("📝 Vocabulary & Phrasal Verbs")
    bank_html = " &nbsp;•&nbsp; ".join([f"<b>{w}</b>" for w in data["bank"]])
    st.markdown(f"<div class='word-bank'>📦 <b>Word Bank:</b> {bank_html}</div>", unsafe_allow_html=True)
    st.caption("Completa cada oración usando una frase exacta del cuadro de palabras.")

    checked = st.session_state[f"{opt}_vocab_checked"]
    score, total = 0, 0

    for i, item in enumerate(data["sentences"]):
        total += 1
        key = f"{opt}_vocab_{i}"
        sel = st.text_input(f"{i+1}. {item['s']}", key=key, placeholder="escribe tu respuesta aquí")
        if checked:
            correct = sel.strip().lower() in [a.lower() for a in item["answer"]]
            if correct:
                score += 1
                st.markdown(f"<div class='feedback-correct'>✅ Correcto — {item['answer'][0]}</div>",
                            unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='feedback-wrong'>❌ Incorrecto. Respuesta correcta: {item['answer'][0]}</div>",
                            unsafe_allow_html=True)

    if st.button("✅ Comprobar Respuestas (Vocabulary)", key=f"{opt}_btn_vocab"):
        st.session_state[f"{opt}_vocab_checked"] = True
        st.rerun()

    if checked:
        st.info(f"Puntaje Vocabulary: **{score} / {total}**")


# ==============================================================================
# 6. RENDER: MÓDULO GRAMMAR
# ==============================================================================

def render_grammar(opt):
    data = CONTENT[opt]["grammar"]
    st.subheader("🔤 Grammar & Structures — Comparatives & Superlatives")

    checked = st.session_state[f"{opt}_grammar_checked"]
    score, total = 0, 0

    st.markdown("#### a) Selección múltiple")
    for i, item in enumerate(data["mc"]):
        total += 1
        key = f"{opt}_grammar_mc_{i}"
        display_opts = ["-- Selecciona --"] + item["options"]
        sel = st.radio(f"{i+1}. {item['q']}", display_opts, key=key)
        if checked:
            if sel == item["answer"]:
                score += 1
                st.markdown(f"<div class='feedback-correct'>✅ Correcto — {item['answer']}"
                            f"<span class='explain'>{item['explain']}</span></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='feedback-wrong'>❌ Incorrecto. Respuesta correcta: {item['answer']}"
                            f"<span class='explain'>{item['explain']}</span></div>", unsafe_allow_html=True)

    st.markdown("#### b) Completa con la forma comparativa/superlativa correcta")
    for i, item in enumerate(data["fillin"]):
        total += 1
        key = f"{opt}_grammar_fill_{i}"
        sel = st.text_input(f"{i+1}. {item['s']}", key=key, placeholder="escribe tu respuesta aquí")
        if checked:
            correct = sel.strip().lower() in [a.lower() for a in item["answer"]]
            if correct:
                score += 1
                st.markdown(f"<div class='feedback-correct'>✅ Correcto — {item['answer'][0]}</div>",
                            unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='feedback-wrong'>❌ Incorrecto. Respuesta correcta: {item['answer'][0]}</div>",
                            unsafe_allow_html=True)

    if st.button("✅ Comprobar Respuestas (Grammar)", key=f"{opt}_btn_grammar"):
        st.session_state[f"{opt}_grammar_checked"] = True
        st.rerun()

    if checked:
        st.info(f"Puntaje Grammar: **{score} / {total}**")


# ==============================================================================
# 7. RENDER: MÓDULO WRITING
# ==============================================================================

def render_writing(opt):
    data = CONTENT[opt]["writing"]
    st.subheader("✍️ Writing — 150 words")

    key_topic = f"{opt}_writing_topic"
    topic = st.radio("Elige UN tema:", data["topics"], key=key_topic)

    key_text = f"{opt}_writing_text"
    text = st.text_area("Escribe tu redacción aquí (en inglés):", height=260, key=key_text)

    words = [w for w in re.split(r"\s+", text.strip()) if w]
    n_words = len(words)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Palabras escritas", n_words, delta=n_words - 150)
    with col2:
        pct = min(100, int((n_words / 150) * 100)) if n_words else 0
        st.progress(pct / 100)
        st.caption(f"{pct}% de la meta de 150 palabras")

    if st.button("✅ Analizar mi Redacción", key=f"{opt}_btn_writing"):
        st.session_state[f"{opt}_writing_checked"] = True

    if st.session_state.get(f"{opt}_writing_checked"):
        found_connectors = [c for c in CONNECTORS if c in text.lower()]
        st.markdown("##### 📊 Feedback automático")
        if n_words == 0:
            st.markdown("<div class='feedback-wrong'>❌ Aún no has escrito nada.</div>", unsafe_allow_html=True)
        elif n_words < 100:
            st.markdown(f"<div class='feedback-wrong'>⚠️ Tu texto tiene solo {n_words} palabras. "
                        f"Intenta acercarte a 150 palabras.</div>", unsafe_allow_html=True)
        elif 100 <= n_words <= 180:
            st.markdown(f"<div class='feedback-correct'>✅ Buena extensión: {n_words} palabras "
                        f"(meta: ~150).</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='feedback-wrong'>⚠️ Tu texto es un poco largo ({n_words} palabras). "
                        f"Trata de ser más conciso.</div>", unsafe_allow_html=True)

        if found_connectors:
            st.markdown(f"<div class='feedback-correct'>✅ Usaste {len(found_connectors)} conector(es): "
                        f"{', '.join(sorted(set(found_connectors)))}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='feedback-wrong'>⚠️ No se detectaron conectores (first, then, "
                        "however, because, in addition...). Intenta usar algunos para organizar mejor tus ideas.</div>",
                        unsafe_allow_html=True)


# ==============================================================================
# 8. VISTA IMPRIMIBLE
# ==============================================================================

def render_printable(opt):
    data = CONTENT[opt]
    st.warning("Modo Vista Imprimible activado. Usa el botón de abajo o Ctrl+P / Cmd+P para imprimir o guardar como PDF.")

    print_btn_html = """
    <button onclick="window.print()"
        style="background:#27ae60;color:white;border:none;padding:12px 22px;
               border-radius:8px;cursor:pointer;font-size:16px;margin-bottom:14px;">
        🖨️ Imprimir / Guardar como PDF
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
    html.append("<p><b>c) Put the events in order (1-5)</b></p>")
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
# 9. APP PRINCIPAL / SIDEBAR
# ==============================================================================

def main():
    init_state()

    with st.sidebar:
        st.title("⚙️ Configuración del examen")

        chosen = st.radio(
            "Selecciona el modelo de examen:",
            options=["A", "B"],
            format_func=lambda x: CONTENT[x]["label"],
            index=0 if st.session_state.option == "A" else 1,
            key="option_radio",
        )
        st.session_state.option = chosen

        if st.button("🎲 Generar Examen Aleatorio"):
            st.session_state.option = random.choice(["A", "B"])
            st.rerun()

        st.markdown("---")
        st.session_state.print_mode = st.checkbox(
            "🖨️ Vista Imprimible / Exportar a PDF", value=st.session_state.print_mode
        )

        st.markdown("---")
        if st.button("🔄 Reiniciar respuestas de esta opción"):
            reset_answers_for_option(st.session_state.option)
            st.rerun()

        st.markdown("---")
        st.caption(
            "Unit 5 — *Eating in Restaurants*  \n"
            "Unit 7 — *Vacations and Travel*  \n"
            "Nivel: A2 / B1"
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
