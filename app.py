# ==============================================================================
# APP DE PRÁCTICA DE INGLÉS (A2-B1) - STREAMLIT
# ==============================================================================
# CÓMO INSTALAR (una sola vez):
#   pip install streamlit pandas
#
# CÓMO EJECUTAR:
#   streamlit run app.py
#
# La app se abrirá en el navegador (normalmente http://localhost:8501).
# Cada estudiante debe abrir la misma URL (si están en la misma red, la
# profesora puede compartir su IP local, ej: streamlit run app.py --server.address=0.0.0.0
# y los alumnos entran a http://IP_DE_LA_PROFESORA:8501)
# ==============================================================================

import streamlit as st
import random
import re
import time
import io
import threading
from datetime import datetime
import pandas as pd

# ------------------------------------------------------------------------------
# CONFIGURACIÓN GENERAL DE LA PÁGINA
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="English Practice - A2/B1",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="expanded",
)

TEACHER_PASSWORD = "teacher123"

UNIT_NAMES = {
    "U1": "Unidad 1: Getting to Know You",
    "U2": "Unidad 2: Events and Places",
    "U3": "Unidad 3: How We Feel",
    "U4": "Unidad 4: Talking about People",
    "U5": "Unidad 5: Eating in Restaurants",
    "U6": "Unidad 6: Living with Technology",
    "U7": "Unidad 7: Vacations and Travel",
    "U8": "Unidad 8: Shopping for Clothes",
    "U9": "Unidad 9: Fitness and Health",
    "U10": "Unidad 10: Life Goals and Plans",
    "GEN": "Repaso General (Todas las Unidades)",
}

# ------------------------------------------------------------------------------
# BANCO DE PREGUNTAS
# Cada pregunta "regular" tiene: id, unit, type, prompt, options (si aplica),
# answer, explanation.
# type puede ser: mcq, fill, reorder, quant, comp, writing
# ------------------------------------------------------------------------------
QUESTIONS = [
    # ---------------- UNIDAD 1 ----------------
    {"id": "U1-1", "unit": "U1", "type": "mcq",
     "prompt": "Choose the correct possessive adjective: 'This is Maria. ___ job is a doctor.'",
     "options": ["Her", "His", "Their", "Your"], "answer": "Her",
     "explanation": "Usamos 'Her' porque Maria es mujer (femenino singular)."},
    {"id": "U1-2", "unit": "U1", "type": "fill",
     "prompt": "Complete: My brother is a ___ (persona que enseña en una escuela).",
     "answer": "teacher",
     "explanation": "'Teacher' = profesor/a. Vocabulario de profesiones."},
    {"id": "U1-3", "unit": "U1", "type": "reorder",
     "prompt": "Reordena las palabras para formar una pregunta: name / What / your / is",
     "answer": "What is your name",
     "explanation": "Estructura de pregunta con 'What' + verbo 'to be' + sujeto."},
    {"id": "U1-4", "unit": "U1", "type": "fill",
     "prompt": "Completa con la contracción correcta: '___ her job?' (What is)",
     "answer": "What's",
     "explanation": "'What is' se contrae como 'What's' en el habla informal."},
    {"id": "U1-5", "unit": "U1", "type": "mcq",
     "prompt": "Choose the correct possessive adjective: 'I have a car. ___ car is red.'",
     "options": ["My", "Your", "Our", "Their"], "answer": "My",
     "explanation": "'My' se usa para 'yo' (I)."},
    {"id": "U1-6", "unit": "U1", "type": "fill",
     "prompt": "Complete: She works in a hospital. She is a ___.",
     "answer": "nurse",
     "explanation": "'Nurse' = enfermera/o, profesión relacionada a hospitales."},
    {"id": "U1-7", "unit": "U1", "type": "reorder",
     "prompt": "Reordena: engineer / an / He / is",
     "answer": "He is an engineer",
     "explanation": "Sujeto + verbo 'to be' + artículo 'an' (antes de vocal) + profesión."},
    {"id": "U1-8", "unit": "U1", "type": "mcq",
     "prompt": "Choose the correct question word: '___ is your last name?'",
     "options": ["What", "Who", "Where", "When"], "answer": "What",
     "explanation": "'What' se usa para preguntar por información como nombres."},
    {"id": "U1-9", "unit": "U1", "type": "fill",
     "prompt": "Complete with the possessive adjective for 'them': ___ parents are teachers.",
     "answer": "Their",
     "explanation": "'Their' corresponde al pronombre 'they' (ellos/ellas)."},
    {"id": "U1-10", "unit": "U1", "type": "writing",
     "prompt": "Write two sentences about yourself: your name and your job/profession.",
     "answer": "", "explanation": "Ejercicio de escritura libre; será revisado por la profesora."},

    # ---------------- UNIDAD 2 ----------------
    {"id": "U2-1", "unit": "U2", "type": "mcq",
     "prompt": "Choose the correct preposition: 'The party is ___ Saturday.'",
     "options": ["on", "in", "at", "by"], "answer": "on",
     "explanation": "Usamos 'on' con días de la semana."},
    {"id": "U2-2", "unit": "U2", "type": "fill",
     "prompt": "Complete with in/on/at: 'The concert starts ___ 8 pm.'",
     "answer": "at",
     "explanation": "Usamos 'at' con horas específicas."},
    {"id": "U2-3", "unit": "U2", "type": "reorder",
     "prompt": "Reordena: party / is / the / Where ?",
     "answer": "Where is the party",
     "explanation": "'Where' + verbo 'to be' + sujeto para preguntar por lugar."},
    {"id": "U2-4", "unit": "U2", "type": "mcq",
     "prompt": "Choose the correct preposition: 'I was born ___ 2001.'",
     "options": ["in", "on", "at", "for"], "answer": "in",
     "explanation": "Usamos 'in' con años y meses."},
    {"id": "U2-5", "unit": "U2", "type": "fill",
     "prompt": "Complete with in/on/at: 'We live ___ Guayaquil.'",
     "answer": "in",
     "explanation": "Usamos 'in' con ciudades y países."},
    {"id": "U2-6", "unit": "U2", "type": "reorder",
     "prompt": "Reordena: start / time / does / What / the movie ?",
     "answer": "What time does the movie start",
     "explanation": "Estructura de pregunta con 'What time' + auxiliar 'does'."},
    {"id": "U2-7", "unit": "U2", "type": "mcq",
     "prompt": "Choose the correct preposition: 'The book is ___ the table.'",
     "options": ["on", "in", "at", "into"], "answer": "on",
     "explanation": "Usamos 'on' para superficies (encima de)."},
    {"id": "U2-8", "unit": "U2", "type": "fill",
     "prompt": "Complete: 'She arrives ___ the airport at noon.' (in/on/at)",
     "answer": "at",
     "explanation": "Usamos 'at' con lugares puntuales como el aeropuerto."},
    {"id": "U2-9", "unit": "U2", "type": "reorder",
     "prompt": "Reordena: the meeting / is / When ?",
     "answer": "When is the meeting",
     "explanation": "'When' se usa para preguntar por tiempo/fecha."},
    {"id": "U2-10", "unit": "U2", "type": "writing",
     "prompt": "Describe a recent event you went to (where, when, and what time it started).",
     "answer": "", "explanation": "Ejercicio de escritura libre; será revisado por la profesora."},

    # ---------------- UNIDAD 3 ----------------
    {"id": "U3-1", "unit": "U3", "type": "mcq",
     "prompt": "Choose the correct modal: '___ you help me, please?'",
     "options": ["Could", "Should", "Must", "Will not"], "answer": "Could",
     "explanation": "'Could' se usa para pedir favores de forma educada."},
    {"id": "U3-2", "unit": "U3", "type": "fill",
     "prompt": "Complete: I have a headache and a fever, so I feel ___ (enfermo/a).",
     "answer": "sick",
     "explanation": "'Sick' = enfermo/a, vocabulario de síntomas."},
    {"id": "U3-3", "unit": "U3", "type": "reorder",
     "prompt": "Reordena: the doctor / I / should / call",
     "answer": "I should call the doctor",
     "explanation": "Sujeto + 'should' + verbo base + complemento."},
    {"id": "U3-4", "unit": "U3", "type": "mcq",
     "prompt": "Choose the correct modal: 'You ___ smoke in the hospital.' (prohibición)",
     "options": ["shouldn't", "could", "can", "should"], "answer": "shouldn't",
     "explanation": "'Shouldn't' se usa para dar un consejo negativo/prohibición suave."},
    {"id": "U3-5", "unit": "U3", "type": "fill",
     "prompt": "Complete: My stomach hurts. I have a ___ (dolor de estómago).",
     "answer": "stomachache",
     "explanation": "'Stomachache' = dolor de estómago."},
    {"id": "U3-6", "unit": "U3", "type": "reorder",
     "prompt": "Reordena: swim / you / Can ?",
     "answer": "Can you swim",
     "explanation": "'Can' + sujeto + verbo base para preguntar por habilidad."},
    {"id": "U3-7", "unit": "U3", "type": "mcq",
     "prompt": "Choose the correct feeling word: 'I got an A on my exam! I feel ___.'",
     "options": ["happy", "sad", "angry", "tired"], "answer": "happy",
     "explanation": "'Happy' = feliz, emoción positiva ante buenas noticias."},
    {"id": "U3-8", "unit": "U3", "type": "fill",
     "prompt": "Complete: You look tired, you ___ (deberías) rest. (should)",
     "answer": "should",
     "explanation": "'Should' se usa para dar consejos."},
    {"id": "U3-9", "unit": "U3", "type": "reorder",
     "prompt": "Reordena: rest / You / should",
     "answer": "You should rest",
     "explanation": "Sujeto + 'should' + verbo base, estructura de consejo."},
    {"id": "U3-10", "unit": "U3", "type": "writing",
     "prompt": "Describe how you feel today and give yourself one piece of advice (using should/shouldn't).",
     "answer": "", "explanation": "Ejercicio de escritura libre; será revisado por la profesora."},

    # ---------------- UNIDAD 4 ----------------
    {"id": "U4-1", "unit": "U4", "type": "fill",
     "prompt": "Complete with present simple: 'She ___ (work) at a bank.'",
     "answer": "works",
     "explanation": "Con 'she/he/it' agregamos -s/-es al verbo en presente simple."},
    {"id": "U4-2", "unit": "U4", "type": "mcq",
     "prompt": "Choose the correct family word: 'My mother's brother is my ___.'",
     "options": ["uncle", "cousin", "nephew", "grandfather"], "answer": "uncle",
     "explanation": "'Uncle' = tío, hermano de la madre o del padre."},
    {"id": "U4-3", "unit": "U4", "type": "comp",
     "prompt": "Complete the comparative: 'My sister is ___ (tall) than me.'",
     "answer": "taller",
     "explanation": "Adjetivos cortos + '-er' + than para comparar."},
    {"id": "U4-4", "unit": "U4", "type": "reorder",
     "prompt": "Reordena la pregunta: like / does / What / your father ?",
     "answer": "What does your father like",
     "explanation": "'What' + auxiliar 'does' + sujeto + verbo base."},
    {"id": "U4-5", "unit": "U4", "type": "fill",
     "prompt": "Complete (negative present simple): 'They ___ (not like) fast food.'",
     "answer": "don't like",
     "explanation": "Negativo del presente simple con 'don't' + verbo base (they/we/you/I)."},
    {"id": "U4-6", "unit": "U4", "type": "mcq",
     "prompt": "Choose the correct family word: 'My father's mother is my ___.'",
     "options": ["grandmother", "aunt", "sister", "niece"], "answer": "grandmother",
     "explanation": "'Grandmother' = abuela."},
    {"id": "U4-7", "unit": "U4", "type": "comp",
     "prompt": "Complete the comparative: 'This exercise is ___ (difficult) than the last one.' (more/less)",
     "answer": "more difficult",
     "explanation": "Adjetivos largos usan 'more' + adjetivo + than."},
    {"id": "U4-8", "unit": "U4", "type": "fill",
     "prompt": "Complete: 'He ___ (not have) a sister.' (negative present simple)",
     "answer": "doesn't have",
     "explanation": "Con he/she/it usamos 'doesn't' + verbo base."},
    {"id": "U4-9", "unit": "U4", "type": "reorder",
     "prompt": "Reordena: brother / play / Does / your / soccer ?",
     "answer": "Does your brother play soccer",
     "explanation": "'Does' + sujeto + verbo base + complemento, pregunta presente simple."},
    {"id": "U4-10", "unit": "U4", "type": "writing",
     "prompt": "Describe a family member: who they are, what they do, and compare them to you (using 'than').",
     "answer": "", "explanation": "Ejercicio de escritura libre; será revisado por la profesora."},

    # ---------------- UNIDAD 5 ----------------
    {"id": "U5-1", "unit": "U5", "type": "quant",
     "prompt": "Choose some/any: 'I don't have ___ money.'",
     "options": ["any", "some"], "answer": "any",
     "explanation": "Usamos 'any' en oraciones negativas."},
    {"id": "U5-2", "unit": "U5", "type": "quant",
     "prompt": "Choose a little/a few: 'I have ___ friends at this school.' (countable)",
     "options": ["a few", "a little"], "answer": "a few",
     "explanation": "'A few' se usa con sustantivos contables (friends)."},
    {"id": "U5-3", "unit": "U5", "type": "mcq",
     "prompt": "Choose the correct question: '___ money do you have?' (uncountable)",
     "options": ["How much", "How many", "How", "What"], "answer": "How much",
     "explanation": "'How much' se usa con sustantivos incontables como 'money'."},
    {"id": "U5-4", "unit": "U5", "type": "fill",
     "prompt": "Complete: Can I have the ___, please? (lista de platos/precios en un restaurante)",
     "answer": "menu",
     "explanation": "'Menu' = menú/carta del restaurante."},
    {"id": "U5-5", "unit": "U5", "type": "quant",
     "prompt": "Choose some/any: 'Would you like ___ coffee?'",
     "options": ["some", "any"], "answer": "some",
     "explanation": "'Some' se usa en preguntas de ofrecimiento."},
    {"id": "U5-6", "unit": "U5", "type": "quant",
     "prompt": "Choose a little/a few: 'There is ___ sugar in the coffee.' (uncountable)",
     "options": ["a little", "a few"], "answer": "a little",
     "explanation": "'A little' se usa con sustantivos incontables (sugar)."},
    {"id": "U5-7", "unit": "U5", "type": "mcq",
     "prompt": "Choose the correct question: '___ apples do you want?' (countable)",
     "options": ["How many", "How much", "How", "What"], "answer": "How many",
     "explanation": "'How many' se usa con sustantivos contables como 'apples'."},
    {"id": "U5-8", "unit": "U5", "type": "fill",
     "prompt": "Complete: Please, can you bring the ___ (cuenta a pagar)?",
     "answer": "bill",
     "explanation": "'Bill' = cuenta/factura del restaurante."},
    {"id": "U5-9", "unit": "U5", "type": "reorder",
     "prompt": "Reordena: table / a / for two / like / I'd",
     "answer": "I'd like a table for two",
     "explanation": "Frase útil en restaurantes para pedir mesa."},
    {"id": "U5-10", "unit": "U5", "type": "writing",
     "prompt": "Write what you would order at a restaurant (starter, main dish, and drink).",
     "answer": "", "explanation": "Ejercicio de escritura libre; será revisado por la profesora."},

    # ---------------- UNIDAD 6 ----------------
    {"id": "U6-1", "unit": "U6", "type": "mcq",
     "prompt": "Choose present simple or continuous: 'Right now, I ___ (text/texting) my friend.'",
     "options": ["am texting", "text", "texts", "texted"], "answer": "am texting",
     "explanation": "Usamos presente continuo para acciones que ocurren en este momento."},
    {"id": "U6-2", "unit": "U6", "type": "fill",
     "prompt": "Complete with a frequency adverb: 'I ___ (siempre) check my phone in the morning.'",
     "answer": "always",
     "explanation": "'Always' = siempre, adverbio de frecuencia."},
    {"id": "U6-3", "unit": "U6", "type": "mcq",
     "prompt": "Choose -ed or -ing: 'This video game is very ___.' (produces the feeling)",
     "options": ["interesting", "interested", "boring adjective wrong", "bored"], "answer": "interesting",
     "explanation": "'-ing' describe la cosa que produce el sentimiento (el juego es interesante)."},
    {"id": "U6-4", "unit": "U6", "type": "reorder",
     "prompt": "Reordena: doing / are / What / you ?",
     "answer": "What are you doing",
     "explanation": "Pregunta en presente continuo: 'What' + 'are' + sujeto + verbo-ing."},
    {"id": "U6-5", "unit": "U6", "type": "mcq",
     "prompt": "Choose present simple or continuous: 'She usually ___ (watch/watching) videos at night.'",
     "options": ["watches", "watch", "is watching", "watched"], "answer": "watches",
     "explanation": "Usamos presente simple para hábitos y rutinas (usually)."},
    {"id": "U6-6", "unit": "U6", "type": "fill",
     "prompt": "Complete: She ___ (nunca) uses social media at school. (never)",
     "answer": "never",
     "explanation": "'Never' = nunca, adverbio de frecuencia."},
    {"id": "U6-7", "unit": "U6", "type": "mcq",
     "prompt": "Choose -ed or -ing: 'I am ___ because I finished all my games.' (feeling)",
     "options": ["bored", "boring", "interesting", "tired adjective wrong"], "answer": "bored",
     "explanation": "'-ed' describe cómo se siente la persona (yo estoy aburrido)."},
    {"id": "U6-8", "unit": "U6", "type": "reorder",
     "prompt": "Reordena: computer / uses / He / his",
     "answer": "He uses his computer",
     "explanation": "Sujeto + verbo (con -s) + posesivo + objeto."},
    {"id": "U6-9", "unit": "U6", "type": "fill",
     "prompt": "Complete with a frequency adverb (occasionally/sometimes): 'I ___ play video games on weekends.'",
     "answer": "sometimes",
     "explanation": "'Sometimes' = a veces, adverbio de frecuencia."},
    {"id": "U6-10", "unit": "U6", "type": "writing",
     "prompt": "Describe your technology habits: what devices you use and how often (using frequency adverbs).",
     "answer": "", "explanation": "Ejercicio de escritura libre; será revisado por la profesora."},

    # ---------------- UNIDAD 7 ----------------
    {"id": "U7-1", "unit": "U7", "type": "fill",
     "prompt": "Complete with past simple: 'Yesterday, I ___ (go) to the beach.' (irregular)",
     "answer": "went",
     "explanation": "'Go' es irregular: pasado simple = 'went'."},
    {"id": "U7-2", "unit": "U7", "type": "mcq",
     "prompt": "Choose the correct object pronoun: 'I saw Maria and I talked to ___.'",
     "options": ["her", "she", "hers", "he"], "answer": "her",
     "explanation": "'Her' es el pronombre de objeto para 'she' (Maria)."},
    {"id": "U7-3", "unit": "U7", "type": "reorder",
     "prompt": "Reordena: last year / travel / did / you / Where ?",
     "answer": "Where did you travel last year",
     "explanation": "'Where' + 'did' + sujeto + verbo base para preguntas en pasado."},
    {"id": "U7-4", "unit": "U7", "type": "fill",
     "prompt": "Complete with past simple: 'They ___ (buy) souvenirs at the market.' (irregular)",
     "answer": "bought",
     "explanation": "'Buy' es irregular: pasado simple = 'bought'."},
    {"id": "U7-5", "unit": "U7", "type": "fill",
     "prompt": "Complete: Before the flight, you must check in at the ___ (mostrador del aeropuerto).",
     "answer": "counter",
     "explanation": "'Check-in counter' = mostrador de check-in en el aeropuerto."},
    {"id": "U7-6", "unit": "U7", "type": "mcq",
     "prompt": "Choose the correct object pronoun: 'This gift is for you and me. Give it to ___.'",
     "options": ["us", "we", "our", "ours"], "answer": "us",
     "explanation": "'Us' es el pronombre de objeto de 'we'."},
    {"id": "U7-7", "unit": "U7", "type": "reorder",
     "prompt": "Reordena: fly / to Peru / did / How / you ?",
     "answer": "How did you fly to Peru",
     "explanation": "'How' + 'did' + sujeto + verbo base, pregunta en pasado."},
    {"id": "U7-8", "unit": "U7", "type": "fill",
     "prompt": "Complete with past simple: 'We ___ (see) an amazing sunset.' (irregular)",
     "answer": "saw",
     "explanation": "'See' es irregular: pasado simple = 'saw'."},
    {"id": "U7-9", "unit": "U7", "type": "fill",
     "prompt": "Complete: I need to show my passport and ___ (boleto) at the gate.",
     "answer": "ticket",
     "explanation": "'Ticket' = boleto/pasaje."},
    {"id": "U7-10", "unit": "U7", "type": "writing",
     "prompt": "Describe your last vacation: where you went, what you did, and how you felt.",
     "answer": "", "explanation": "Ejercicio de escritura libre; será revisado por la profesora."},

    # ---------------- UNIDAD 8 ----------------
    {"id": "U8-1", "unit": "U8", "type": "mcq",
     "prompt": "Choose the correct clothing word: 'I need new ___ for running.' (calzado)",
     "options": ["shoes", "shirt", "hat", "belt"], "answer": "shoes",
     "explanation": "'Shoes' = zapatos."},
    {"id": "U8-2", "unit": "U8", "type": "comp",
     "prompt": "Complete the comparative: 'This jacket is ___ (expensive) than that one.'",
     "answer": "more expensive",
     "explanation": "Adjetivos largos usan 'more' + adjetivo + than."},
    {"id": "U8-3", "unit": "U8", "type": "comp",
     "prompt": "Complete the superlative: 'This is ___ (cheap) shirt in the store.'",
     "answer": "the cheapest",
     "explanation": "Adjetivos cortos forman el superlativo con 'the' + adjetivo + '-est'."},
    {"id": "U8-4", "unit": "U8", "type": "fill",
     "prompt": "Complete: What ___ (talla) do you wear? Small, medium or large?",
     "answer": "size",
     "explanation": "'Size' = talla."},
    {"id": "U8-5", "unit": "U8", "type": "mcq",
     "prompt": "Choose the correct clothing word: 'It's cold, wear a ___.' (prenda de abrigo)",
     "options": ["jacket", "sandals", "shorts", "swimsuit"], "answer": "jacket",
     "explanation": "'Jacket' = chaqueta, prenda de abrigo."},
    {"id": "U8-6", "unit": "U8", "type": "comp",
     "prompt": "Complete the superlative: 'These are ___ (comfortable) shoes I own.' (more/most)",
     "answer": "the most comfortable",
     "explanation": "Adjetivos largos forman el superlativo con 'the most' + adjetivo."},
    {"id": "U8-7", "unit": "U8", "type": "comp",
     "prompt": "Complete the comparative: 'My shoes are ___ (big) than yours.'",
     "answer": "bigger",
     "explanation": "Adjetivos cortos que terminan en consonante+vocal+consonante duplican la última letra + er."},
    {"id": "U8-8", "unit": "U8", "type": "reorder",
     "prompt": "Reordena: dress / try / this / Can / on / I ?",
     "answer": "Can I try this dress on",
     "explanation": "Frase útil para probarse ropa en una tienda."},
    {"id": "U8-9", "unit": "U8", "type": "fill",
     "prompt": "Complete: These pants are too big, do you have a smaller ___?",
     "answer": "size",
     "explanation": "'Size' = talla."},
    {"id": "U8-10", "unit": "U8", "type": "writing",
     "prompt": "Describe what you are wearing today and compare it to what you wore yesterday.",
     "answer": "", "explanation": "Ejercicio de escritura libre; será revisado por la profesora."},

    # ---------------- UNIDAD 9 ----------------
    {"id": "U9-1", "unit": "U9", "type": "fill",
     "prompt": "Complete: You run with your ___ (parte del cuerpo, plural de 'leg').",
     "answer": "legs",
     "explanation": "'Legs' = piernas."},
    {"id": "U9-2", "unit": "U9", "type": "mcq",
     "prompt": "Choose the correct modal: 'You ___ wear a helmet when you ride a bike.' (obligación)",
     "options": ["must", "could", "shouldn't", "may"], "answer": "must",
     "explanation": "'Must' expresa obligación/necesidad fuerte."},
    {"id": "U9-3", "unit": "U9", "type": "reorder",
     "prompt": "Reordena: exercise / should / You / every day",
     "answer": "You should exercise every day",
     "explanation": "Sujeto + 'should' + verbo base + complemento, consejo de salud."},
    {"id": "U9-4", "unit": "U9", "type": "fill",
     "prompt": "Complete: I hurt my ___ (parte del cuerpo que usas para caminar y está al final de la pierna).",
     "answer": "foot",
     "explanation": "'Foot' = pie."},
    {"id": "U9-5", "unit": "U9", "type": "mcq",
     "prompt": "Choose the correct sport: 'You need a racket and a net to play ___.'",
     "options": ["tennis", "soccer", "swimming", "boxing"], "answer": "tennis",
     "explanation": "'Tennis' requiere raqueta y red."},
    {"id": "U9-6", "unit": "U9", "type": "mcq",
     "prompt": "Choose must or should: 'For safety, you ___ stop at a red light.' (regla obligatoria)",
     "options": ["must", "should", "could", "might"], "answer": "must",
     "explanation": "'Must' se usa para reglas/leyes obligatorias."},
    {"id": "U9-7", "unit": "U9", "type": "fill",
     "prompt": "Complete: I use my ___ (parte del cuerpo, plural de 'arm') to lift weights.",
     "answer": "arms",
     "explanation": "'Arms' = brazos."},
    {"id": "U9-8", "unit": "U9", "type": "reorder",
     "prompt": "Reordena: eat / You / vegetables / should / more",
     "answer": "You should eat more vegetables",
     "explanation": "Sujeto + 'should' + verbo base + complemento, consejo de salud."},
    {"id": "U9-9", "unit": "U9", "type": "mcq",
     "prompt": "Choose the correct sport: 'You need a ball and a hoop to play ___.'",
     "options": ["basketball", "tennis", "swimming", "cycling"], "answer": "basketball",
     "explanation": "'Basketball' se juega con balón y aro."},
    {"id": "U9-10", "unit": "U9", "type": "writing",
     "prompt": "Write a simple weekly fitness plan (what exercise, how many days, and why it's good for your health).",
     "answer": "", "explanation": "Ejercicio de escritura libre; será revisado por la profesora."},

    # ---------------- UNIDAD 10 ----------------
    {"id": "U10-1", "unit": "U10", "type": "mcq",
     "prompt": "Choose going to or will: 'Look at those clouds! It ___ rain.' (predicción con evidencia)",
     "options": ["is going to", "will", "would", "was going to"], "answer": "is going to",
     "explanation": "'Going to' se usa para predicciones basadas en evidencia visible."},
    {"id": "U10-2", "unit": "U10", "type": "quant",
     "prompt": "Choose the correct indefinite pronoun: 'I don't have ___ to do this weekend.'",
     "options": ["anything", "something", "nothing", "everything"], "answer": "anything",
     "explanation": "Usamos 'anything' en oraciones negativas."},
    {"id": "U10-3", "unit": "U10", "type": "reorder",
     "prompt": "Reordena: do / going / What / to / you / are ?",
     "answer": "What are you going to do",
     "explanation": "Pregunta con futuro 'going to': 'What' + 'are' + sujeto + 'going to' + verbo."},
    {"id": "U10-4", "unit": "U10", "type": "fill",
     "prompt": "Complete with 'although': 'I passed the test, ___ I didn't study much.'",
     "answer": "although",
     "explanation": "'Although' introduce una idea contraria/inesperada."},
    {"id": "U10-5", "unit": "U10", "type": "quant",
     "prompt": "Choose the correct indefinite pronoun: 'I decided ___, I still don't know what to study.' (nada)",
     "options": ["nothing", "something", "anything", "everything"], "answer": "nothing",
     "explanation": "'Nothing' significa 'nada' en afirmativo."},
    {"id": "U10-6", "unit": "U10", "type": "mcq",
     "prompt": "Choose going to or will: 'I promise I ___ help you tomorrow.' (decisión espontánea/promesa)",
     "options": ["will", "am going to", "was", "would"], "answer": "will",
     "explanation": "'Will' se usa para promesas y decisiones espontáneas."},
    {"id": "U10-7", "unit": "U10", "type": "quant",
     "prompt": "Choose the correct indefinite pronoun: 'There is ___ in the fridge, we need to buy food.' (nada)",
     "options": ["nothing", "something", "anything", "everyone"], "answer": "nothing",
     "explanation": "'Nothing' = nada, se usa en oraciones afirmativas con sentido negativo."},
    {"id": "U10-8", "unit": "U10", "type": "reorder",
     "prompt": "Reordena: study abroad / although / it's / going to / expensive / I'm",
     "answer": "I'm going to study abroad although it's expensive",
     "explanation": "'Although' conecta dos ideas contrastantes en una sola oración."},
    {"id": "U10-9", "unit": "U10", "type": "fill",
     "prompt": "Complete: Next year, I ___ (plan) to graduate. (going to)",
     "answer": "am going to",
     "explanation": "'Going to' se usa para planes futuros ya decididos."},
    {"id": "U10-10", "unit": "U10", "type": "writing",
     "prompt": "Write about your life goals for the next 5 years (use 'going to' or 'will').",
     "answer": "", "explanation": "Ejercicio de escritura libre; será revisado por la profesora."},
]

# ------------------------------------------------------------------------------
# LECTURAS (para el examen largo). Cada lectura tiene un pasaje y 3 preguntas
# de tipo Verdadero/Falso/No se menciona.
# ------------------------------------------------------------------------------
READINGS = [
    {"id": "R-U1", "unit": "U1",
     "passage": "Carlos is 28 years old. He is an engineer and he works for a technology company in Quito. "
                "His sister, Ana, is a nurse. She works at the city hospital. Carlos likes his job because "
                "he can travel a lot for work.",
     "questions": [
         {"id": "R-U1-1", "prompt": "Carlos is a nurse.", "answer": "False"},
         {"id": "R-U1-2", "prompt": "Ana works at a hospital.", "answer": "True"},
         {"id": "R-U1-3", "prompt": "Carlos is 30 years old.", "answer": "False"},
     ]},
    {"id": "R-U2", "unit": "U2",
     "passage": "There is a big music festival in the city park on Saturday. It starts at 4 pm and finishes at "
                "11 pm. Tickets cost $15. There will be food trucks and local bands. The organizers ask people "
                "to arrive early because parking is limited.",
     "questions": [
         {"id": "R-U2-1", "prompt": "The festival is on Sunday.", "answer": "False"},
         {"id": "R-U2-2", "prompt": "Tickets cost $15.", "answer": "True"},
         {"id": "R-U2-3", "prompt": "The festival has a swimming pool.", "answer": "Not Mentioned"},
     ]},
    {"id": "R-U3", "unit": "U3",
     "passage": "Laura woke up with a headache and a sore throat. She felt very tired, so she decided to stay "
                "home and rest instead of going to work. She drank tea and took some medicine. Her doctor told "
                "her she should sleep more and drink a lot of water.",
     "questions": [
         {"id": "R-U3-1", "prompt": "Laura went to work.", "answer": "False"},
         {"id": "R-U3-2", "prompt": "Laura has a headache.", "answer": "True"},
         {"id": "R-U3-3", "prompt": "Laura's doctor gave her an injection.", "answer": "Not Mentioned"},
     ]},
    {"id": "R-U4", "unit": "U4",
     "passage": "Sofia has a big family. Her father is a chef and her mother is an accountant. She has two "
                "brothers: Luis, who is older than her, and Pedro, who is younger. Sofia is taller than Pedro "
                "but shorter than Luis.",
     "questions": [
         {"id": "R-U4-1", "prompt": "Sofia has two sisters.", "answer": "False"},
         {"id": "R-U4-2", "prompt": "Luis is older than Sofia.", "answer": "True"},
         {"id": "R-U4-3", "prompt": "Sofia's mother is a doctor.", "answer": "False"},
     ]},
    {"id": "R-U5", "unit": "U5",
     "passage": "The restaurant 'La Cocina' is famous for its seafood. On weekends, it is very busy and you "
                "need a reservation. The menu has a little variety of desserts but a lot of main dishes. Many "
                "customers say the service is fast and friendly.",
     "questions": [
         {"id": "R-U5-1", "prompt": "The restaurant is famous for its seafood.", "answer": "True"},
         {"id": "R-U5-2", "prompt": "You never need a reservation.", "answer": "False"},
         {"id": "R-U5-3", "prompt": "The restaurant is open 24 hours.", "answer": "Not Mentioned"},
     ]},
    {"id": "R-U6", "unit": "U6",
     "passage": "Daniel uses his phone every day for work and study. He always checks his email in the morning "
                "and he often watches tutorial videos at night. He thinks technology is very useful, but "
                "sometimes he feels tired of looking at screens all day.",
     "questions": [
         {"id": "R-U6-1", "prompt": "Daniel never checks his email.", "answer": "False"},
         {"id": "R-U6-2", "prompt": "Daniel watches tutorial videos.", "answer": "True"},
         {"id": "R-U6-3", "prompt": "Daniel bought a new phone last week.", "answer": "Not Mentioned"},
     ]},
    {"id": "R-U7", "unit": "U7",
     "passage": "Last summer, Maria traveled to Colombia with her family. They visited Cartagena and stayed "
                "in a small hotel near the beach. They saw beautiful sunsets and tried a lot of local food. "
                "Maria said it was the best vacation she ever had.",
     "questions": [
         {"id": "R-U7-1", "prompt": "Maria traveled alone.", "answer": "False"},
         {"id": "R-U7-2", "prompt": "Maria visited Cartagena.", "answer": "True"},
         {"id": "R-U7-3", "prompt": "Maria's flight was delayed.", "answer": "Not Mentioned"},
     ]},
    {"id": "R-U8", "unit": "U8",
     "passage": "The new shopping mall has a big clothing store with the best prices in the city. It sells "
                "shirts, jackets and shoes for men, women, and children. The store is having a sale this week: "
                "the most expensive jackets are 30% off.",
     "questions": [
         {"id": "R-U8-1", "prompt": "The store only sells shoes.", "answer": "False"},
         {"id": "R-U8-2", "prompt": "Jackets are on sale this week.", "answer": "True"},
         {"id": "R-U8-3", "prompt": "The store opened five years ago.", "answer": "Not Mentioned"},
     ]},
    {"id": "R-U9", "unit": "U9",
     "passage": "Pedro wants to be healthier this year. He goes to the gym three times a week and he must eat "
                "more vegetables. His trainer said he should also drink more water and sleep 8 hours every "
                "night. Pedro's favorite sport is basketball.",
     "questions": [
         {"id": "R-U9-1", "prompt": "Pedro goes to the gym three times a week.", "answer": "True"},
         {"id": "R-U9-2", "prompt": "Pedro's favorite sport is soccer.", "answer": "False"},
         {"id": "R-U9-3", "prompt": "Pedro's trainer is 40 years old.", "answer": "Not Mentioned"},
     ]},
    {"id": "R-U10", "unit": "U10",
     "passage": "Camila is going to graduate next year and she is planning to study abroad, although it is "
                "expensive. She will apply for a scholarship to help pay for it. Her goal is to become a "
                "doctor and help people in rural communities.",
     "questions": [
         {"id": "R-U10-1", "prompt": "Camila wants to study abroad.", "answer": "True"},
         {"id": "R-U10-2", "prompt": "Camila already graduated.", "answer": "False"},
         {"id": "R-U10-3", "prompt": "Camila wants to be a lawyer.", "answer": "False"},
     ]},
]

TF_OPTIONS = ["True", "False", "Not Mentioned"]

# ------------------------------------------------------------------------------
# ALMACÉN COMPARTIDO ENTRE SESIONES (IMPORTANTE)
# ------------------------------------------------------------------------------
# st.session_state es INDIVIDUAL por cada navegador/pestaña: si cada alumno
# abre la app desde su celular, su session_state es solo suyo y NUNCA llega
# a la sesión de la profesora. Para que los resultados se vean "en tiempo
# real" en el panel de la profesora, deben guardarse en un almacén
# COMPARTIDO por todas las sesiones que usan la misma app en el servidor.
# @st.cache_resource crea justo eso: un único objeto en memoria compartido
# por todos los usuarios mientras la app siga corriendo (se reinicia si la
# app se reinicia/duerme por inactividad en Streamlit Cloud).
# ------------------------------------------------------------------------------
@st.cache_resource
def get_shared_store():
    return {"submissions": [], "lock": threading.Lock()}


shared_store = get_shared_store()

# ------------------------------------------------------------------------------
# FUNCIONES AUXILIARES
# ------------------------------------------------------------------------------

def normalize_text(s):
    """Quita puntuación y espacios extra, pasa a minúsculas, para comparar respuestas."""
    s = str(s).strip().lower()
    s = re.sub(r"[^\w\s']", "", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def check_answer(item, given):
    """Compara la respuesta del estudiante contra la respuesta correcta."""
    if given is None:
        return False
    if item["type"] == "writing":
        # Ejercicio abierto: se da crédito por intentarlo, se marca para revisión manual.
        return len(str(given).strip()) > 0
    if item["type"] == "reorder":
        return normalize_text(given) == normalize_text(item["answer"])
    return normalize_text(given) == normalize_text(item["answer"])


def build_exam(unit, mode):
    """Construye la lista de ejercicios para el examen según la unidad y el modo.
    mode: 'short' (10 ejercicios, 15 min) o 'long' (hasta 20 ejercicios, 30 min, incluye lectura)."""
    if unit == "GEN":
        regular_pool = list(QUESTIONS)
        reading_pool = list(READINGS)
    else:
        regular_pool = [q for q in QUESTIONS if q["unit"] == unit]
        reading_pool = [r for r in READINGS if r["unit"] == unit]

    random.shuffle(regular_pool)
    random.shuffle(reading_pool)

    items = []

    if mode == "short":
        duration = 15 * 60
        chosen = regular_pool[:10]
        for q in chosen:
            items.append({**q, "kind": "regular"})
    else:
        duration = 30 * 60
        # Se incluye 1 lectura (con sus preguntas) + ejercicios regulares hasta completar 20
        reading = reading_pool[0] if reading_pool else None
        reading_qty = len(reading["questions"]) if reading else 0
        regular_needed = max(0, 20 - reading_qty)
        chosen_regular = regular_pool[:regular_needed]
        for q in chosen_regular:
            items.append({**q, "kind": "regular"})
        if reading:
            for sub in reading["questions"]:
                items.append({
                    "id": sub["id"], "unit": reading["unit"], "type": "reading_tf",
                    "prompt": sub["prompt"], "answer": sub["answer"],
                    "explanation": f"Según el texto: '{reading['passage'][:60]}...'",
                    "kind": "reading", "passage": reading["passage"],
                })

    random.shuffle(items)
    return items, duration


def format_time(seconds):
    seconds = max(0, int(seconds))
    m, s = divmod(seconds, 60)
    return f"{m:02d}:{s:02d}"


def score_to_10(correct, total):
    if total == 0:
        return 0.0
    return round((correct / total) * 10, 1)


def submit_exam():
    """Recolecta las respuestas del formulario, calcula el puntaje y guarda la entrega."""
    items = st.session_state.exam_items
    details = []
    correct_count = 0
    for item in items:
        key = f"ans_{item['id']}"
        given = st.session_state.get(key, "")
        is_correct = check_answer(item, given)
        if is_correct:
            correct_count += 1
        details.append({
            "prompt": item["prompt"],
            "type": item["type"],
            "respuesta_alumno": given if given else "(sin responder)",
            "respuesta_correcta": item["answer"] if item["type"] != "writing" else "(respuesta libre)",
            "correcto": is_correct,
            "explicacion": item["explanation"],
        })

    total = len(items)
    score = score_to_10(correct_count, total)
    elapsed = time.time() - st.session_state.exam_start_time
    duration_label = "15 min (Corto)" if st.session_state.exam_mode == "short" else "30 min (Largo)"

    submission = {
        "Nombre": st.session_state.student_name,
        "Unidad": UNIT_NAMES.get(st.session_state.exam_unit, st.session_state.exam_unit),
        "Modalidad": duration_label,
        "Tiempo empleado": format_time(elapsed),
        "Puntaje (0-10)": score,
        "Ejercicios correctos": f"{correct_count}/{total}",
        "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "detalle": details,
    }

    with shared_store["lock"]:
        shared_store["submissions"].append(submission)

    st.session_state.last_result = submission
    st.session_state.exam_active = False
    st.session_state.exam_finished = True


# ------------------------------------------------------------------------------
# INICIALIZACIÓN DE SESSION STATE
# ------------------------------------------------------------------------------
if "exam_active" not in st.session_state:
    st.session_state.exam_active = False
if "exam_finished" not in st.session_state:
    st.session_state.exam_finished = False
if "time_up" not in st.session_state:
    st.session_state.time_up = False

# ------------------------------------------------------------------------------
# SIDEBAR - SELECCIÓN DE MODO
# ------------------------------------------------------------------------------
st.sidebar.title("📚 English Practice")
app_mode = st.sidebar.radio("Selecciona tu rol:", ["Estudiante", "Profesora"])
st.sidebar.markdown("---")
st.sidebar.caption("App de práctica A2-B1 · 10 unidades · Streamlit")

# ==============================================================================
# MODO ESTUDIANTE
# ==============================================================================
if app_mode == "Estudiante":
    st.title("🧑‍🎓 Modo Estudiante")

    # -------- Si terminó el examen y aún no reinicia --------
    if st.session_state.exam_finished and st.session_state.get("last_result"):
        result = st.session_state.last_result
        st.success(f"¡Enviado a la teacher! Puntaje: **{result['Puntaje (0-10)']} / 10**")
        col1, col2, col3 = st.columns(3)
        col1.metric("Puntaje", f"{result['Puntaje (0-10)']}/10")
        col2.metric("Correctas", result["Ejercicios correctos"])
        col3.metric("Tiempo empleado", result["Tiempo empleado"])

        st.markdown("### 📝 Desglose pedagógico")
        for i, d in enumerate(result["detalle"], start=1):
            icon = "✅" if d["correcto"] else "❌"
            with st.expander(f"{icon} Ejercicio {i}: {d['prompt'][:60]}..."):
                st.write(f"**Tu respuesta:** {d['respuesta_alumno']}")
                st.write(f"**Respuesta correcta:** {d['respuesta_correcta']}")
                st.info(f"💡 Retroalimentación (A2 → B1): {d['explicacion']}")

        if st.button("🔄 Realizar otro examen"):
            st.session_state.exam_finished = False
            st.session_state.exam_active = False
            st.session_state.time_up = False
            st.session_state.pop("last_result", None)
            st.rerun()

    # -------- Si el examen está activo (en curso) --------
    elif st.session_state.exam_active:
        # Si el tiempo se acabó, se envía automáticamente
        if st.session_state.time_up:
            submit_exam()
            st.rerun()

        st.subheader(f"Examen: {UNIT_NAMES.get(st.session_state.exam_unit)}")
        st.caption(f"Estudiante: {st.session_state.student_name}")

        # --- Temporizador (fragmento que se auto-actualiza cada segundo) ---
        @st.fragment(run_every=1)
        def timer_fragment():
            elapsed = time.time() - st.session_state.exam_start_time
            remaining = st.session_state.exam_duration - elapsed
            if remaining <= 0:
                st.session_state.time_up = True
                st.rerun()
            else:
                pct = max(0.0, min(1.0, remaining / st.session_state.exam_duration))
                st.progress(pct, text=f"⏱️ Tiempo restante: {format_time(remaining)}")

        timer_fragment()

        # --- Formulario con los ejercicios ---
        with st.form(key="exam_form"):
            reading_shown = set()
            for i, item in enumerate(st.session_state.exam_items, start=1):
                key = f"ans_{item['id']}"

                if item["kind"] == "reading" and item["id"] not in reading_shown:
                    pass  # el pasaje se muestra antes de la primera pregunta de esa lectura

                if item["kind"] == "reading":
                    passage = item["passage"]
                    if passage not in reading_shown:
                        st.markdown("#### 📖 Texto de lectura")
                        st.info(passage)
                        reading_shown.add(passage)
                    st.markdown(f"**{i}. {item['prompt']}** _(True / False / Not Mentioned)_")
                    st.radio(" ", TF_OPTIONS, key=key, label_visibility="collapsed", index=None)

                elif item["type"] == "mcq":
                    st.markdown(f"**{i}. {item['prompt']}**")
                    st.radio(" ", item["options"], key=key, label_visibility="collapsed", index=None)

                elif item["type"] == "quant":
                    st.markdown(f"**{i}. {item['prompt']}**")
                    st.radio(" ", item["options"], key=key, label_visibility="collapsed", index=None)

                elif item["type"] == "fill" or item["type"] == "comp":
                    st.markdown(f"**{i}. {item['prompt']}**")
                    st.text_input(" ", key=key, label_visibility="collapsed")

                elif item["type"] == "reorder":
                    st.markdown(f"**{i}. {item['prompt']}**")
                    st.text_input("Escribe la oración completa y ordenada:", key=key)

                elif item["type"] == "writing":
                    st.markdown(f"**{i}. {item['prompt']}**")
                    st.text_area(" ", key=key, label_visibility="collapsed")

                st.markdown("---")

            submitted = st.form_submit_button("📤 Enviar a la Teacher", use_container_width=True)
            if submitted:
                submit_exam()
                st.rerun()

    # -------- Formulario de registro / configuración --------
    else:
        st.write("Completa tus datos para comenzar la práctica.")
        with st.form(key="setup_form"):
            name = st.text_input("Nombre y Apellido del Estudiante")
            unit = st.selectbox(
                "Unidad o Tema",
                options=list(UNIT_NAMES.keys()),
                format_func=lambda k: UNIT_NAMES[k],
            )
            mode_label = st.radio(
                "Tiempo / Modalidad",
                options=["Examen Corto - 15 minutos (10 ejercicios)",
                         "Examen Largo / Lectura - 30 minutos (hasta 20 ejercicios)"],
            )
            start = st.form_submit_button("▶️ Comenzar examen", use_container_width=True)

            if start:
                if not name.strip():
                    st.error("Por favor ingresa tu nombre y apellido.")
                else:
                    mode_key = "short" if mode_label.startswith("Examen Corto") else "long"
                    items, duration = build_exam(unit, mode_key)
                    if not items:
                        st.error("No hay ejercicios disponibles para esta selección.")
                    else:
                        st.session_state.student_name = name.strip()
                        st.session_state.exam_unit = unit
                        st.session_state.exam_mode = mode_key
                        st.session_state.exam_items = items
                        st.session_state.exam_duration = duration
                        st.session_state.exam_start_time = time.time()
                        st.session_state.exam_active = True
                        st.session_state.exam_finished = False
                        st.session_state.time_up = False
                        st.rerun()

# ==============================================================================
# MODO PROFESORA
# ==============================================================================
else:
    st.title("👩‍🏫 Modo Profesora")

    if "teacher_authenticated" not in st.session_state:
        st.session_state.teacher_authenticated = False

    if not st.session_state.teacher_authenticated:
        pwd = st.text_input("Ingresa la clave de profesora:", type="password")
        if st.button("Ingresar"):
            if pwd == TEACHER_PASSWORD:
                st.session_state.teacher_authenticated = True
                st.rerun()
            else:
                st.error("Clave incorrecta.")
    else:
        st.success("Acceso concedido ✅")
        subs = shared_store["submissions"]

        refresh_col1, refresh_col2 = st.columns([1, 5])
        with refresh_col1:
            if st.button("🔄 Actualizar"):
                st.rerun()
        with refresh_col2:
            st.caption("Los resultados de todos los alumnos (cualquier celular/PC) llegan aquí en tiempo real. "
                       "Usa 'Actualizar' si un alumno acaba de enviar y no ves su fila todavía.")

        if not subs:
            st.info("Todavía no hay entregas registradas en esta clase.")
        else:
            table_data = [
                {
                    "Nombre": s["Nombre"],
                    "Unidad": s["Unidad"],
                    "Modalidad": s["Modalidad"],
                    "Tiempo empleado": s["Tiempo empleado"],
                    "Puntaje (0-10)": s["Puntaje (0-10)"],
                    "Correctas": s["Ejercicios correctos"],
                    "Fecha": s["Fecha"],
                }
                for s in subs
            ]
            df = pd.DataFrame(table_data)
            st.markdown(f"### 📊 Entregas de la clase ({len(subs)})")
            st.dataframe(df, use_container_width=True, hide_index=True)

            avg_score = round(df["Puntaje (0-10)"].mean(), 2) if len(df) else 0
            colA, colB = st.columns(2)
            colA.metric("Promedio del curso", f"{avg_score}/10")
            colB.metric("Total de entregas", len(subs))

            with st.expander("🔍 Ver detalle de respuestas por alumno"):
                names = [s["Nombre"] for s in subs]
                selected = st.selectbox("Selecciona una entrega:", options=range(len(subs)),
                                         format_func=lambda i: f"{names[i]} - {subs[i]['Fecha']}")
                detail_df = pd.DataFrame(subs[selected]["detalle"])
                st.dataframe(detail_df, use_container_width=True, hide_index=True)

            # --- Exportar a CSV ---
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            st.download_button(
                label="⬇️ Exportar resultados a CSV",
                data=csv_buffer.getvalue(),
                file_name=f"resultados_clase_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True,
            )

            # --- Reiniciar registros ---
            st.markdown("---")
            confirm_reset = st.checkbox("Confirmo que deseo borrar todos los registros de esta clase.")
            if st.button("🗑️ Reiniciar / limpiar registros", disabled=not confirm_reset, use_container_width=True):
                with shared_store["lock"]:
                    shared_store["submissions"].clear()
                st.success("Registros reiniciados.")
                st.rerun()
