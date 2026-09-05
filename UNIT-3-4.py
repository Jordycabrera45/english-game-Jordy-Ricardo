import streamlit as st
import streamlit.components.v1 as components
import re

st.set_page_config(page_title="Units 3-4: How We Feel / Talking about People", page_icon="👪", layout="wide")

# =============================================================================
# CONTENT DATA — VERSION A AND VERSION B
# =============================================================================

CONTENT = {
    "A": {
        "audio_text": (
            "Every summer, the Ramirez family has a huge reunion at their grandparents' house. "
            "This year, over thirty relatives came, including aunts, uncles, cousins, nieces, and nephews. "
            "Grandma Rosa, who is eighty-two, is the oldest person in the family, and everyone says she's much more outgoing than her husband, Grandpa Hugo, who is very quiet. "
            "Rosa's daughter, Elena, just got engaged to her boyfriend, Peter, and the whole family is excited about the wedding next spring. "
            "Elena's brother, Carlos, is divorced, but he's still close friends with his ex-wife, Marta, and they often get together with their kids. "
            "During the party, Elena's niece, Sofia, arrived with a terrible cold. "
            "She had a sore throat and a headache, and she looked worse than she felt. "
            "Her aunt, Elena, told her she should rest and drink hot tea, and that she shouldn't play soccer with her cousins that afternoon. "
            "Sofia said she felt sad because she couldn't join the game, but she also felt happy watching everyone have fun. "
            "Later, the family played games in the yard. "
            "Carlos's son, Diego, is more athletic than his cousins, and he can run faster than almost everyone at the party. "
            "His sister, Amy, can't play soccer very well, but she's much funnier than Diego and always makes everyone laugh. "
            "By the end of the day, everyone agreed that Grandma Rosa's reunions are always the best part of the summer."
        ),
        "mc": [
            {"q": "How old is Grandma Rosa?", "options": ["72", "80", "82", "90"],
             "answer": 2, "explanation": "The text states Grandma Rosa is eighty-two."},
            {"q": "Who just got engaged?", "options": ["Carlos", "Elena", "Sofia", "Marta"],
             "answer": 1, "explanation": "Elena just got engaged to her boyfriend, Peter."},
            {"q": "What is Carlos's relationship with his ex-wife, Marta?",
             "options": ["They never speak", "They are still close friends", "They live together", "They are getting married again"],
             "answer": 1, "explanation": "The text says they are still close friends and often get together."},
            {"q": "What ailments did Sofia have?",
             "options": ["A backache and fever", "A sore throat and a headache", "A stomachache and cough", "An earache and toothache"],
             "answer": 1, "explanation": "Sofia had a sore throat and a headache."},
            {"q": "According to the story, who is more athletic among Carlos's children?",
             "options": ["Amy", "Diego", "Both equally", "Neither"],
             "answer": 1, "explanation": "Diego is described as more athletic than his cousins."},
        ],
        "tf": [
            {"q": "Grandma Rosa is more outgoing than Grandpa Hugo.", "answer": True},
            {"q": "Elena told Sofia she should play soccer that afternoon.", "answer": False},
            {"q": "Carlos is divorced from Marta.", "answer": True},
            {"q": "Amy can play soccer very well.", "answer": False},
            {"q": "More than thirty relatives attended the reunion.", "answer": True},
        ],
        "order_events": {
            "events": {
                "A": "Sofia arrived with a cold.",
                "B": "Elena got engaged to Peter.",
                "C": "Elena told Sofia to rest and drink tea.",
                "D": "The family played games in the yard.",
                "E": "Diego ran faster than his cousins.",
                "F": "Everyone agreed Grandma Rosa's reunions are the best.",
            },
            "correct_order": ["B", "A", "C", "D", "E", "F"],
        },
        "reading": {
            "title": "What Makes Families Different (and Alike)",
            "paragraphs": [
                "Families around the world come in many shapes and sizes. Some people grow up in a small immediate family with just their parents and siblings, while others are surrounded by a large extended family that includes grandparents, aunts, uncles, and dozens of cousins. In recent years, more households have become multi-generational, meaning grandparents, parents, and children all live under the same roof. Researchers say these different family structures can shape how people communicate, celebrate, and even resolve conflicts.",
                "Take the Torres sisters as an example. Camila is the older sister, and she is far more outgoing than her younger sister, Valeria, who tends to be quieter in social situations. Camila got married last year, while Valeria is still single and says she isn't in a hurry to change that. When Valeria had a bad cold last month, Camila told her she should stay home and rest instead of going to work, and Valeria, for once, actually followed her sister's advice.",
                "Cousins Mia and Elena are often mistaken for sisters because they look so alike, with the same curly hair and the same smile. However, their abilities are completely different. Mia can play the violin beautifully, but she can't cook at all, while Elena can't play any instrument but is easily the best cook in the family. Neither of them can swim, which always surprises people, since they grew up near the beach.",
                "According to family therapists, comparing siblings or cousins isn't necessarily negative. In fact, understanding that your cousin is the funniest person at every gathering, or that your brother-in-law is the most patient with children, can help families appreciate each person's unique role. The key, experts say, is to celebrate differences rather than turn them into competition.",
            ],
            "mc": [
                {"q": "What happened when Valeria had a bad cold?",
                 "options": ["She went to work anyway", "Camila told her to stay home and rest", "She saw a doctor immediately", "She ignored her sister's advice"],
                 "answer": 1, "explanation": "Paragraph 2 states Camila told her to stay home and rest."},
                {"q": "Why are Mia and Elena often mistaken for sisters?",
                 "options": ["They have the same personality", "They look very alike", "They live in the same house", "They are actually twins"],
                 "answer": 1, "explanation": "Paragraph 3 says they look alike, with the same curly hair and smile."},
                {"q": "What can Elena do well, according to the text?",
                 "options": ["Play the violin", "Swim", "Cook", "Draw"],
                 "answer": 2, "explanation": "Paragraph 3 states Elena is easily the best cook in the family."},
            ],
            "tfnm": [
                {"q": "Camila is the younger sister.", "answer": "False"},
                {"q": "Mia and Elena both know how to swim.", "answer": "False"},
                {"q": "Mia and Elena grew up near the beach.", "answer": "True"},
            ],
            "vocab": [
                {"q": "In paragraph 1, the phrase 'under the same roof' is closest in meaning to...",
                 "options": ["in the same house", "on the same street", "with the same personality", "at the same job"],
                 "answer": 0, "explanation": "'Under the same roof' means living together in the same house."},
                {"q": "In paragraph 4, the word 'unique' is closest in meaning to...",
                 "options": ["common", "one of a kind", "confusing", "unimportant"],
                 "answer": 1, "explanation": "'Unique' means being the only one of its kind, special."},
            ],
            "inference": [
                {"q": "What can we infer about Valeria's personality from paragraph 2?",
                 "options": ["She rarely listens to advice", "She is somewhat stubborn but can be convinced by people close to her", "She always follows every piece of advice she receives", "She dislikes her sister"],
                 "answer": 1, "explanation": "The text notes she 'for once' followed the advice, suggesting she doesn't always."},
                {"q": "Why does the text suggest that comparing family members isn't always negative?",
                 "options": ["Because it always leads to competition", "Because recognizing each person's strengths can help families appreciate their differences", "Because most families argue about comparisons", "Because comparisons are usually inaccurate"],
                 "answer": 1, "explanation": "Paragraph 4 explains that recognizing unique roles helps families appreciate each other."},
            ],
        },
        "word_bank": ["keep in touch", "get together", "drop by", "tons of",
                      "an only child", "feel awful", "I'm sorry to hear that", "enough about me"],
        "vocab_sentences": [
            {"q": "Even though my cousins live abroad, we always try to ______ by calling every month.",
             "answer": "keep in touch"},
            {"q": "Every summer, the whole family likes to ______ at our grandmother's house.",
             "answer": "get together"},
            {"q": "If you're ever in the neighborhood, feel free to ______ and say hello.",
             "answer": "drop by"},
            {"q": "My sister has ______ friends from university who still visit her every year.",
             "answer": "tons of"},
            {"q": "Since my brother has no siblings, he's ______.",
             "answer": "an only child"},
            {"q": "After the long flight, David says he ______ and needs to rest.",
             "answer": "feels awful", "accept": ["feels awful", "feel awful"]},
            {"q": "When Maria heard that her uncle was in the hospital, she said, \"______.\"",
             "answer": "I'm sorry to hear that"},
            {"q": "\"Anyway, ______ — how's your new job going?\" Peter asked his friend, changing the subject.",
             "answer": "enough about me"},
        ],
        "grammar_mc": [
            {"q": "My brother is ____ than me.", "options": ["tall", "taller", "more tall", "the tallest"],
             "answer": 1, "explanation": "Short adjectives form the comparative with -er: tall → taller."},
            {"q": "She is ____ person I know.", "options": ["the most funny", "funnier", "the funniest", "more funny"],
             "answer": 2, "explanation": "Short adjectives ending in -y form the superlative with -iest: funny → the funniest."},
            {"q": "This exercise is ____ than the last one.", "options": ["more easy", "easier", "easiest", "the easier"],
             "answer": 1, "explanation": "'Easy' becomes 'easier' in the comparative (y → i + er)."},
            {"q": "He's a good cook, but his sister is even ____.", "options": ["gooder", "better", "best", "more good"],
             "answer": 1, "explanation": "'Good' is irregular: good → better → the best."},
            {"q": "Choose the correct superlative.", "options": ["the most expensivest", "the expensivest", "the most expensive", "more expensivest"],
             "answer": 2, "explanation": "Long adjectives use 'the most' + adjective: the most expensive."},
            {"q": "My grandmother is ____ than my grandfather.", "options": ["more talkativer", "more talkative", "talkativer", "the more talkative"],
             "answer": 1, "explanation": "Long adjectives use 'more' + adjective in the comparative: more talkative."},
            {"q": "Of all my cousins, Diego is ____.", "options": ["the athleticest", "more athletic", "the most athletic", "athleticer"],
             "answer": 2, "explanation": "'Athletic' is a long adjective, so the superlative is 'the most athletic'."},
            {"q": "This is ____ movie I've ever seen.", "options": ["the worse", "worse", "the worst", "more worse"],
             "answer": 2, "explanation": "'Bad' is irregular: bad → worse → the worst."},
        ],
        "grammar_fill": [
            {"q": "My aunt is ______________ (funny - comparative) than my uncle.", "answer": "funnier"},
            {"q": "This is ______________ (interesting - superlative) book in the library.", "answer": "the most interesting"},
            {"q": "Diego is ______________ (athletic - comparative) than his sister.", "answer": "more athletic"},
            {"q": "Of all the cousins, Amy is ______________ (funny - superlative) one at parties.", "answer": "the funniest"},
            {"q": "My grandfather is ______________ (quiet - comparative) than my grandmother.", "answer": "quieter"},
        ],
        "writing_topics": [
            "Describe your immediate and extended family. Who are you closest to, and why?",
            "Compare two people in your family using comparative adjectives.",
            "Write about a time you felt sick and someone gave you advice. What did they say?",
            "Describe an ability you have or would like to develop, and explain how you plan to improve it.",
        ],
    },

    "B": {
        "audio_text": (
            "Last weekend, Linda organized a family dinner to celebrate her father-in-law's birthday. "
            "Linda's husband, Mark, has three sisters, and all of them came with their families. "
            "Mark's mother, Grace, has been widowed for five years, but she says she feels happier now than she has in a long time. "
            "Linda's sister-in-law, Karen, is separated from her husband, but she still comes to every family event with her children. "
            "During dinner, Linda's nephew, Tyler, said he felt scared because he had a stomachache, so his aunt told him he shouldn't eat any more cake and that he should drink some water instead. "
            "Meanwhile, Mark's youngest sister, Beth, brought her new boyfriend to meet the family for the first time. "
            "Everyone agreed that Beth's boyfriend is much more talkative than her last one, and definitely funnier, too. "
            "After dinner, the cousins played games in the living room. "
            "Tyler's older cousin, Max, can play the piano really well, and he can also draw better than anyone else in the family. "
            "His sister, Zoe, can't draw at all, but she's more athletic than Max and can run much faster. "
            "Grace watched everyone from her chair, feeling excited about seeing her grandchildren together again. "
            "By the end of the night, Linda felt tired but happy, and she said this was one of the best family dinners they'd had in years."
        ),
        "mc": [
            {"q": "Whose birthday were they celebrating?", "options": ["Linda's", "Mark's", "Mark's father's", "Grace's"],
             "answer": 2, "explanation": "The dinner celebrated Linda's father-in-law's birthday."},
            {"q": "How long has Grace been widowed?", "options": ["Two years", "Five years", "Ten years", "She isn't widowed"],
             "answer": 1, "explanation": "The text states Grace has been widowed for five years."},
            {"q": "What is Karen's marital status?", "options": ["Married", "Divorced", "Separated", "Engaged"],
             "answer": 2, "explanation": "Karen is described as separated from her husband."},
            {"q": "What was wrong with Tyler?", "options": ["He had a headache", "He had a stomachache", "He had a sore throat", "He had a fever"],
             "answer": 1, "explanation": "Tyler had a stomachache after eating cake."},
            {"q": "According to the story, who can play the piano well?", "options": ["Zoe", "Beth", "Max", "Tyler"],
             "answer": 2, "explanation": "Max can play the piano really well."},
        ],
        "tf": [
            {"q": "Grace has been widowed for five years.", "answer": True},
            {"q": "Karen is divorced from her husband.", "answer": False},
            {"q": "Beth's new boyfriend is quieter than her last one.", "answer": False},
            {"q": "Zoe is more athletic than Max.", "answer": True},
            {"q": "Tyler's aunt told him he should eat more cake.", "answer": False},
        ],
        "order_events": {
            "events": {
                "A": "Beth brought her new boyfriend to meet the family.",
                "B": "Tyler said he felt scared because of his stomachache.",
                "C": "Linda organized the family dinner.",
                "D": "The cousins played games in the living room.",
                "E": "Grace watched her grandchildren, feeling excited.",
                "F": "Linda said it was one of the best family dinners.",
            },
            "correct_order": ["C", "A", "B", "D", "E", "F"],
        },
        "reading": {
            "title": "Learning New Things at Any Age",
            "paragraphs": [
                "There's an old saying that you can't teach an old dog new tricks, meaning that it's supposedly difficult for older people to learn new skills. But is that really true? Psychologists who study how people develop abilities point to three main factors: motivation, practice, and natural ability. According to most experts, motivation and practice usually matter more than natural talent, no matter how old the learner is.",
                "Mr. Alvarez decided to learn the guitar at the age of sixty-eight, right after he retired. At first, practicing scales felt boring, and he sometimes wanted to give up. However, his daughter-in-law, who teaches music, says he is actually more disciplined than most of her younger students. She should know, she has seen dozens of students over the years, and few of them practice every single day the way Mr. Alvarez does.",
                "Grandma Wu never learned to drive when she was young because, in her family, it wasn't common for women to drive. At seventy years old, she finally decided it was time. Her son was scared at first and told her she probably shouldn't attempt it at her age, but her granddaughter disagreed, saying Grandma Wu is braver than most young people she knows. After several months of lessons, Grandma Wu passed her driving test on her first try.",
                "Stories like these show that developing a new ability has less to do with age and more to do with motivation and family support. When people feel excited instead of discouraged, and when family members encourage instead of discourage them, almost anyone can learn something new at any point in life.",
            ],
            "mc": [
                {"q": "At what age did Mr. Alvarez start learning the guitar?", "options": ["58", "62", "68", "70"],
                 "answer": 2, "explanation": "The text states he started at sixty-eight, right after retiring."},
                {"q": "According to his daughter-in-law, how does Mr. Alvarez compare to her younger students?",
                 "options": ["He is less disciplined", "He is more disciplined", "He is exactly the same", "He never practices"],
                 "answer": 1, "explanation": "Paragraph 2 says he is more disciplined than most of her younger students."},
                {"q": "What did Grandma Wu's son think about her decision to learn to drive?",
                 "options": ["He was excited for her", "He was scared and doubtful", "He didn't care", "He decided to teach her himself"],
                 "answer": 1, "explanation": "Her son was scared and told her she probably shouldn't attempt it."},
            ],
            "tfnm": [
                {"q": "Grandma Wu passed her driving test on her first try.", "answer": "True"},
                {"q": "Mr. Alvarez's daughter-in-law is a driving instructor.", "answer": "False"},
                {"q": "Grandma Wu's granddaughter also doesn't know how to drive.", "answer": "Not Mentioned"},
            ],
            "vocab": [
                {"q": "In paragraph 2, the phrase 'give up' is closest in meaning to...",
                 "options": ["continue trying", "stop trying", "start again", "improve quickly"],
                 "answer": 1, "explanation": "'Give up' means to stop trying to do something."},
                {"q": "In paragraph 4, the word 'discouraged' is closest in meaning to...",
                 "options": ["feeling confident and motivated", "feeling like giving up or losing hope", "feeling proud of an achievement", "feeling relaxed"],
                 "answer": 1, "explanation": "'Discouraged' describes losing confidence or hope about doing something."},
            ],
            "inference": [
                {"q": "What can we infer about the role of family in developing new abilities, based on the text?",
                 "options": ["Family members have no real effect on learning", "Family encouragement can play an important role in someone's success", "Only teachers can help someone learn a skill", "Family members usually discourage older relatives from trying new things"],
                 "answer": 1, "explanation": "The examples show family encouragement (or doubt) affecting the outcome."},
                {"q": "Why does the text mention the saying 'you can't teach an old dog new tricks' in paragraph 1?",
                 "options": ["To prove that the saying is completely true", "To introduce an idea the rest of the text will challenge", "To give advice about training pets", "To explain a scientific law"],
                 "answer": 1, "explanation": "The rest of the text uses examples to challenge this common belief."},
            ],
        },
        "word_bank": ["bless you", "what are you up to", "will do", "feel better",
                      "take a nap", "no way", "good advice", "so busy"],
        "vocab_sentences": [
            {"q": "When Andrew sneezed loudly, Coral said, \"______, Andrew!\"",
             "answer": "bless you", "accept": ["bless you"]},
            {"q": "\"So, ______ these days? Are you still working at the bank?\" Coral asked her old friend.",
             "answer": "what are you up to"},
            {"q": "\"Please call me when you arrive,\" said Mom. \"______,\" replied her son.",
             "answer": "will do"},
            {"q": "After hearing that her friend was sick, Sofia said, \"I hope you ______ soon.\"",
             "answer": "feel better"},
            {"q": "Grandpa was so tired after the long trip that he decided to ______ before dinner.",
             "answer": "take a nap"},
            {"q": "\"My cousin can speak four languages fluently.\" \"______! That's amazing.\"",
             "answer": "no way"},
            {"q": "The doctor gave Mr. Alvarez some ______ about how to protect his back while gardening.",
             "answer": "good advice"},
            {"q": "Linda has been ______ this week that she hasn't had time to call anyone.",
             "answer": "so busy"},
        ],
        "grammar_mc": [
            {"q": "Karen's new apartment is ____ than her old one.", "options": ["more big", "bigger", "biggest", "the bigger"],
             "answer": 1, "explanation": "Short adjectives form the comparative with -er: big → bigger."},
            {"q": "Max is ____ student in his class.", "options": ["more smart", "smarter", "the smartest", "smartest"],
             "answer": 2, "explanation": "The superlative needs 'the': the smartest."},
            {"q": "This soup tastes ____ than the one from yesterday.", "options": ["more good", "gooder", "better", "best"],
             "answer": 2, "explanation": "'Good' is irregular: good → better → the best."},
            {"q": "Choose the correct superlative.", "options": ["the most beautifulest", "more beautifuler", "the most beautiful", "beautifulest"],
             "answer": 2, "explanation": "Long adjectives use 'the most' + adjective: the most beautiful."},
            {"q": "Zoe runs ____ than Max.", "options": ["fast", "faster", "fastest", "more fast"],
             "answer": 1, "explanation": "Short adjectives form the comparative with -er: fast → faster."},
            {"q": "Grace is ____ person in the whole family.", "options": ["happyest", "the happiest", "more happy", "happier"],
             "answer": 1, "explanation": "'Happy' becomes 'the happiest' in the superlative (y → i + est)."},
            {"q": "Choose the correct comparative.", "options": ["more relaxinger", "relaxinger", "more relaxing", "the relaxing"],
             "answer": 2, "explanation": "Long adjectives use 'more' + adjective in the comparative: more relaxing."},
            {"q": "This was ____ day of my life.", "options": ["the worse", "worst", "the worst", "more worst"],
             "answer": 2, "explanation": "'Bad' is irregular: bad → worse → the worst."},
        ],
        "grammar_fill": [
            {"q": "Beth's boyfriend is ______________ (talkative - comparative) than her last one.", "answer": "more talkative"},
            {"q": "Grandma Wu is ______________ (brave - superlative) person in the family.", "answer": "the bravest"},
            {"q": "Tyler's stomachache is ______________ (bad - comparative) today than yesterday.", "answer": "worse"},
            {"q": "Of all the cousins, Max is ______________ (good - superlative) piano player.", "answer": "the best"},
            {"q": "Mark's mother is ______________ (happy - comparative) now than she was last year.", "answer": "happier"},
        ],
        "writing_topics": [
            "Describe the person in your family who is the most similar to you. In what ways?",
            "Write about a family celebration or reunion you remember well.",
            "Give advice to someone who doesn't feel well, using should/shouldn't.",
            "Describe someone you admire and explain what makes them special, using comparatives.",
        ],
    },
}

CONNECTORS = ["first", "then", "however", "because", "in addition", "finally", "for example",
              "also", "moreover", "on the other hand", "as a result", "after that", "next", "in conclusion"]

# =============================================================================
# HELPERS
# =============================================================================

def normalize(text):
    text = text.lower().strip()
    text = re.sub(r"[^\w\s']", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


def check_text_answer(user_input, item):
    accepted = item.get("accept", [item["answer"]])
    user_norm = normalize(user_input)
    return any(user_norm == normalize(a) for a in accepted) and user_norm != ""


def init_keys():
    if "version" not in st.session_state:
        st.session_state.version = "A"
    if "printable" not in st.session_state:
        st.session_state.printable = False


def reset_version_answers(version):
    prefix = f"{version}_"
    for key in list(st.session_state.keys()):
        if key.startswith(prefix):
            del st.session_state[key]
    st.rerun()


# =============================================================================
# AUDIO PLAYER COMPONENT
# =============================================================================

def render_audio_player(text, key_suffix):
    safe_text = text.replace("\\", "\\\\").replace("`", "'")
    html_code = f"""
    <div style="font-family: sans-serif;">
      <p id="audioText-{key_suffix}" style="display:none;">{safe_text}</p>
      <button id="playBtn-{key_suffix}" style="padding:8px 16px; margin-right:8px; background-color:#2563eb; color:white; border:none; border-radius:6px; cursor:pointer; font-size:14px;">▶ Play Audio</button>
      <button id="stopBtn-{key_suffix}" style="padding:8px 16px; background-color:#dc2626; color:white; border:none; border-radius:6px; cursor:pointer; font-size:14px;">⏹ Stop</button>
      <span id="status-{key_suffix}" style="margin-left:12px; font-weight:bold; color:#374151;"></span>
    </div>
    <script>
      (function() {{
        const playBtn = document.getElementById("playBtn-{key_suffix}");
        const stopBtn = document.getElementById("stopBtn-{key_suffix}");
        const statusEl = document.getElementById("status-{key_suffix}");
        const textEl = document.getElementById("audioText-{key_suffix}");

        function pickVoice() {{
          const voices = window.speechSynthesis.getVoices();
          let v = voices.find(v => v.lang === "en-US");
          if (!v) v = voices.find(v => v.lang && v.lang.startsWith("en"));
          return v;
        }}

        playBtn.addEventListener("click", function() {{
          window.speechSynthesis.cancel();
          const utterance = new SpeechSynthesisUtterance(textEl.textContent);
          const voice = pickVoice();
          if (voice) {{ utterance.voice = voice; utterance.lang = voice.lang; }}
          else {{ utterance.lang = "en-US"; }}
          utterance.rate = 0.95;
          utterance.onstart = function() {{ statusEl.textContent = "Playing..."; }};
          utterance.onend = function() {{ statusEl.textContent = "Finished."; }};
          utterance.onerror = function() {{ statusEl.textContent = "Error playing audio."; }};
          window.speechSynthesis.speak(utterance);
        }});

        stopBtn.addEventListener("click", function() {{
          window.speechSynthesis.cancel();
          statusEl.textContent = "Stopped.";
        }});
      }})();
    </script>
    """
    components.html(html_code, height=70)


# =============================================================================
# MODULE RENDERERS (interactive mode)
# =============================================================================

def render_listening(version, data):
    st.subheader("🎧 Module 1: Listening Comprehension")
    st.caption("Click Play to listen to the story. You can play it as many times as you need.")
    render_audio_player(data["audio_text"], f"listen_{version}")

    st.markdown("**Audio script:**")
    st.markdown(f"> {data['audio_text']}")

    st.markdown("#### A. Multiple Choice")
    mc_prefix = f"{version}_listen_mc_"
    for i, item in enumerate(data["mc"]):
        st.radio(f"{i+1}. {item['q']}", item["options"], key=mc_prefix + str(i), index=None)

    st.markdown("#### B. True / False")
    tf_prefix = f"{version}_listen_tf_"
    for i, item in enumerate(data["tf"]):
        st.radio(f"{i+1}. {item['q']}", ["True", "False"], key=tf_prefix + str(i), index=None)

    st.markdown("#### C. Put the events in chronological order")
    st.caption("Assign a letter (A–F) to each position, from first (1) to last (6).")
    events = data["order_events"]["events"]
    st.markdown("\n".join([f"- **{letter}.** {desc}" for letter, desc in events.items()]))
    order_prefix = f"{version}_listen_order_"
    cols = st.columns(6)
    for i in range(6):
        with cols[i]:
            st.selectbox(f"Position {i+1}", ["-", "A", "B", "C", "D", "E", "F"], key=order_prefix + str(i))

    checked_key = f"{version}_listen_checked"
    if st.button("✅ Check Answers", key=f"{version}_listen_check_btn"):
        st.session_state[checked_key] = True

    if st.session_state.get(checked_key):
        st.markdown("---")
        st.markdown("**Results — Multiple Choice**")
        for i, item in enumerate(data["mc"]):
            user = st.session_state.get(mc_prefix + str(i))
            correct = item["options"][item["answer"]]
            if user == correct:
                st.success(f"{i+1}. Correct! {item['explanation']}")
            else:
                st.error(f"{i+1}. Incorrect (you chose: {user or 'no answer'}). Correct answer: {correct}. {item['explanation']}")

        st.markdown("**Results — True / False**")
        for i, item in enumerate(data["tf"]):
            user = st.session_state.get(tf_prefix + str(i))
            correct = "True" if item["answer"] else "False"
            if user == correct:
                st.success(f"{i+1}. Correct!")
            else:
                st.error(f"{i+1}. Incorrect (you chose: {user or 'no answer'}). Correct answer: {correct}")

        st.markdown("**Results — Chronological Order**")
        user_order = [st.session_state.get(order_prefix + str(i), "-") for i in range(6)]
        correct_order = data["order_events"]["correct_order"]
        if user_order == correct_order:
            st.success(f"All correct! Order: {' → '.join(correct_order)}")
        else:
            st.error(f"Your order: {' → '.join(user_order)}. Correct order: {' → '.join(correct_order)}")


def render_reading(version, data):
    st.subheader("📖 Module 2: Reading Comprehension")
    st.markdown(f"#### {data['reading']['title']}")
    for i, p in enumerate(data["reading"]["paragraphs"]):
        st.markdown(f"**Paragraph {i+1}.** {p}")

    st.markdown("#### A. Multiple Choice")
    mc_prefix = f"{version}_read_mc_"
    for i, item in enumerate(data["reading"]["mc"]):
        st.radio(f"{i+1}. {item['q']}", item["options"], key=mc_prefix + str(i), index=None)

    st.markdown("#### B. True / False / Not Mentioned")
    tfnm_prefix = f"{version}_read_tfnm_"
    for i, item in enumerate(data["reading"]["tfnm"]):
        st.radio(f"{i+1}. {item['q']}", ["True", "False", "Not Mentioned"], key=tfnm_prefix + str(i), index=None)

    st.markdown("#### C. Vocabulary in Context")
    vocab_prefix = f"{version}_read_vocab_"
    for i, item in enumerate(data["reading"]["vocab"]):
        st.radio(f"{i+1}. {item['q']}", item["options"], key=vocab_prefix + str(i), index=None)

    st.markdown("#### D. Inference")
    inf_prefix = f"{version}_read_inf_"
    for i, item in enumerate(data["reading"]["inference"]):
        st.radio(f"{i+1}. {item['q']}", item["options"], key=inf_prefix + str(i), index=None)

    checked_key = f"{version}_read_checked"
    if st.button("✅ Check Answers", key=f"{version}_read_check_btn"):
        st.session_state[checked_key] = True

    if st.session_state.get(checked_key):
        st.markdown("---")
        for label, prefix, items in [
            ("Multiple Choice", mc_prefix, data["reading"]["mc"]),
            ("Vocabulary in Context", vocab_prefix, data["reading"]["vocab"]),
            ("Inference", inf_prefix, data["reading"]["inference"]),
        ]:
            st.markdown(f"**Results — {label}**")
            for i, item in enumerate(items):
                user = st.session_state.get(prefix + str(i))
                correct = item["options"][item["answer"]]
                if user == correct:
                    st.success(f"{i+1}. Correct! {item['explanation']}")
                else:
                    st.error(f"{i+1}. Incorrect (you chose: {user or 'no answer'}). Correct answer: {correct}. {item['explanation']}")

        st.markdown("**Results — True / False / Not Mentioned**")
        for i, item in enumerate(data["reading"]["tfnm"]):
            user = st.session_state.get(tfnm_prefix + str(i))
            correct = item["answer"]
            if user == correct:
                st.success(f"{i+1}. Correct!")
            else:
                st.error(f"{i+1}. Incorrect (you chose: {user or 'no answer'}). Correct answer: {correct}")


def render_vocabulary(version, data):
    st.subheader("📝 Module 3: Vocabulary & Idioms")
    st.markdown("#### Word Bank")
    st.info(" • ".join(data["word_bank"]))
    st.caption("Complete each sentence using an exact phrase from the Word Bank above.")

    prefix = f"{version}_vocab_"
    for i, item in enumerate(data["vocab_sentences"]):
        st.text_input(f"{i+1}. {item['q']}", key=prefix + str(i))

    checked_key = f"{version}_vocab_checked"
    if st.button("✅ Check Answers", key=f"{version}_vocab_check_btn"):
        st.session_state[checked_key] = True

    if st.session_state.get(checked_key):
        st.markdown("---")
        for i, item in enumerate(data["vocab_sentences"]):
            user = st.session_state.get(prefix + str(i), "")
            if check_text_answer(user, item):
                st.success(f"{i+1}. Correct!")
            else:
                st.error(f"{i+1}. Incorrect (you wrote: \"{user}\"). Expected: \"{item['answer']}\"")


def render_grammar(version, data):
    st.subheader("📐 Module 4: Grammar — Comparatives & Superlatives")
    st.markdown("#### A. Multiple Choice")
    mc_prefix = f"{version}_gram_mc_"
    for i, item in enumerate(data["grammar_mc"]):
        st.radio(f"{i+1}. {item['q']}", item["options"], key=mc_prefix + str(i), index=None)

    st.markdown("#### B. Complete the Sentences")
    fill_prefix = f"{version}_gram_fill_"
    for i, item in enumerate(data["grammar_fill"]):
        st.text_input(f"{i+1}. {item['q']}", key=fill_prefix + str(i))

    checked_key = f"{version}_gram_checked"
    if st.button("✅ Check Answers", key=f"{version}_gram_check_btn"):
        st.session_state[checked_key] = True

    if st.session_state.get(checked_key):
        st.markdown("---")
        st.markdown("**Results — Multiple Choice**")
        for i, item in enumerate(data["grammar_mc"]):
            user = st.session_state.get(mc_prefix + str(i))
            correct = item["options"][item["answer"]]
            if user == correct:
                st.success(f"{i+1}. Correct! {item['explanation']}")
            else:
                st.error(f"{i+1}. Incorrect (you chose: {user or 'no answer'}). Correct answer: {correct}. {item['explanation']}")

        st.markdown("**Results — Complete the Sentences**")
        for i, item in enumerate(data["grammar_fill"]):
            user = st.session_state.get(fill_prefix + str(i), "")
            if check_text_answer(user, item):
                st.success(f"{i+1}. Correct!")
            else:
                st.error(f"{i+1}. Incorrect (you wrote: \"{user}\"). Expected: \"{item['answer']}\"")


def render_writing(version, data):
    st.subheader("✍️ Module 5: Writing (150 words)")
    topic_key = f"{version}_write_topic"
    text_key = f"{version}_write_text"
    st.radio("Choose one topic:", data["writing_topics"], key=topic_key, index=None)
    text = st.text_area("Write your composition here:", key=text_key, height=250)

    words = re.findall(r"\b[\w']+\b", text or "")
    word_count = len(words)
    progress = min(word_count / 150, 1.0)
    st.progress(progress, text=f"{word_count} / 150 words")

    if st.button("✅ Check My Writing", key=f"{version}_write_check_btn"):
        st.session_state[f"{version}_write_submitted"] = True

    if st.session_state.get(f"{version}_write_submitted"):
        st.markdown("---")
        if word_count < 100:
            st.error(f"Your composition has {word_count} words. Try to write closer to 150 words to fully develop your ideas.")
        elif word_count < 140:
            st.warning(f"Your composition has {word_count} words. You're close to the goal — try to add a bit more detail.")
        else:
            st.success(f"Great! Your composition has {word_count} words, close to the 150-word goal.")

        text_lower = (text or "").lower()
        found_connectors = [c for c in CONNECTORS if c in text_lower]
        if found_connectors:
            st.success(f"Good use of connectors: {', '.join(found_connectors)}. This helps your ideas flow logically.")
        else:
            st.warning("No connectors detected (e.g., first, then, however, because, in addition, finally). Try adding some to link your ideas.")

        if not st.session_state.get(topic_key):
            st.info("Remember to select a topic above before submitting your final version.")


# =============================================================================
# PRINTABLE VIEW
# =============================================================================

def render_printable(version, data):
    st.markdown("""
    <style>
    @media print {
        [data-testid="stSidebar"], header, [data-testid="stToolbar"] { display: none !important; }
    }
    </style>
    """, unsafe_allow_html=True)

    st.title(f"UNITS 3-4: HOW WE FEEL / TALKING ABOUT PEOPLE — Exam (Version {version})")
    st.caption("Printable worksheet — press Ctrl+P (or Cmd+P) to print or save as PDF.")
    st.markdown("**Name:** _______________________________  **Date:** _______________  **Score:** _______ / 100")
    st.markdown("---")

    st.header("Module 1: Listening Comprehension")
    st.caption("(Listen to the audio in the app, or use this script if listening offline is not possible.)")
    with st.expander("Audio script (for teacher/offline use)"):
        st.write(data["audio_text"])

    st.markdown("**A. Multiple Choice — Circle the correct answer.**")
    for i, item in enumerate(data["mc"]):
        st.markdown(f"{i+1}. {item['q']}")
        opts = "    ".join([f"{chr(65+j)}) {opt}" for j, opt in enumerate(item["options"])])
        st.markdown(opts)

    st.markdown("**B. True / False — Write T or F.**")
    for i, item in enumerate(data["tf"]):
        st.markdown(f"____ {i+1}. {item['q']}")

    st.markdown("**C. Put the events in chronological order (write letters 1–6).**")
    for letter, desc in data["order_events"]["events"].items():
        st.markdown(f"**{letter}.** {desc}")
    st.markdown("Order: 1.___ 2.___ 3.___ 4.___ 5.___ 6.___")

    st.markdown("---")
    st.header("Module 2: Reading Comprehension")
    st.subheader(data["reading"]["title"])
    for i, p in enumerate(data["reading"]["paragraphs"]):
        st.markdown(f"**Paragraph {i+1}.** {p}")

    st.markdown("**A. Multiple Choice**")
    for i, item in enumerate(data["reading"]["mc"]):
        st.markdown(f"{i+1}. {item['q']}")
        opts = "    ".join([f"{chr(65+j)}) {opt}" for j, opt in enumerate(item["options"])])
        st.markdown(opts)

    st.markdown("**B. True / False / Not Mentioned**")
    for i, item in enumerate(data["reading"]["tfnm"]):
        st.markdown(f"____ {i+1}. {item['q']}")

    st.markdown("**C. Vocabulary in Context**")
    for i, item in enumerate(data["reading"]["vocab"]):
        st.markdown(f"{i+1}. {item['q']}")
        opts = "    ".join([f"{chr(65+j)}) {opt}" for j, opt in enumerate(item["options"])])
        st.markdown(opts)

    st.markdown("**D. Inference**")
    for i, item in enumerate(data["reading"]["inference"]):
        st.markdown(f"{i+1}. {item['q']}")
        opts = "    ".join([f"{chr(65+j)}) {opt}" for j, opt in enumerate(item["options"])])
        st.markdown(opts)

    st.markdown("---")
    st.header("Module 3: Vocabulary & Idioms")
    st.markdown("**Word Bank:** " + " • ".join(data["word_bank"]))
    for i, item in enumerate(data["vocab_sentences"]):
        st.markdown(f"{i+1}. {item['q']}")

    st.markdown("---")
    st.header("Module 4: Grammar — Comparatives & Superlatives")
    st.markdown("**A. Multiple Choice**")
    for i, item in enumerate(data["grammar_mc"]):
        st.markdown(f"{i+1}. {item['q']}")
        opts = "    ".join([f"{chr(65+j)}) {opt}" for j, opt in enumerate(item["options"])])
        st.markdown(opts)
    st.markdown("**B. Complete the Sentences**")
    for i, item in enumerate(data["grammar_fill"]):
        st.markdown(f"{i+1}. {item['q']}")

    st.markdown("---")
    st.header("Module 5: Writing (150 words)")
    st.markdown("Choose ONE topic and write your composition below.")
    for i, t in enumerate(data["writing_topics"]):
        st.markdown(f"{chr(65+i)}) {t}")
    st.markdown("\n".join(["_" * 90 for _ in range(14)]))


# =============================================================================
# MAIN APP
# =============================================================================

def main():
    init_keys()

    st.sidebar.title("👪 Units 3-4: How We Feel / Talking about People")
    st.sidebar.markdown("### Exam Version")
    version = st.sidebar.radio("Choose a version:", ["Version A", "Version B"],
                                index=0 if st.session_state.version == "A" else 1)
    st.session_state.version = "A" if version == "Version A" else "B"
    v = st.session_state.version

    st.sidebar.markdown("---")
    st.session_state.printable = st.sidebar.checkbox("🖨️ Printable View / Export to PDF", value=st.session_state.printable)

    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 Reset answers (current version)"):
        reset_version_answers(v)

    data = CONTENT[v]

    if st.session_state.printable:
        render_printable(v, data)
        return

    st.title("👪 Units 3-4: How We Feel / Talking about People")
    st.caption(f"Interactive Study & Assessment App — Version {v}")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "1. Listening", "2. Reading", "3. Vocabulary", "4. Grammar", "5. Writing"
    ])

    with tab1:
        render_listening(v, data)
    with tab2:
        render_reading(v, data)
    with tab3:
        render_vocabulary(v, data)
    with tab4:
        render_grammar(v, data)
    with tab5:
        render_writing(v, data)


if __name__ == "__main__":
    main()
