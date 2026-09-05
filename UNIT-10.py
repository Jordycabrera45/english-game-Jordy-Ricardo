import streamlit as st
import streamlit.components.v1 as components
import re

st.set_page_config(page_title="Unit 10: Life Goals and Plans - Practice & Test", page_icon="🎯", layout="wide")

# =============================================================================
# CONTENT DATA — VERSION A AND VERSION B
# =============================================================================

CONTENT = {
    "A": {
        "audio_text": (
            "Last month, my cousin Elena finally decided to make some big changes in her life. "
            "She had been working at the same company for eight years, but she felt she needed a new challenge. "
            "First, she told her manager that she wanted to change careers and move into marketing. "
            "Her manager was surprised, but he agreed to help her find a position in a different department. "
            "A few weeks later, Elena's boyfriend Tomas proposed to her, and she was thrilled. "
            "They had fallen in love three years earlier, right after Elena graduated from university with a degree in business. "
            "Now they were planning a small wedding for next summer. "
            "Elena's grandmother, who is eighty years old, always says her only wish is to live a long, healthy life and to see her grandchildren get married. "
            "When Elena told her the news, she cried with happiness. "
            "After the engagement, Elena and Tomas began to talk about their future together. "
            "Tomas has always dreamed of living abroad, maybe in Spain or Italy, so they decided that after the wedding, they would move to Madrid for two years while Tomas works for an international company. "
            "Elena isn't sure if she wants to become famous or get rich, but she does hope to get a promotion once she settles into her new job. "
            "Her final goal is simple: she wants to retire early, travel the world, and spend more time with her family. "
            "Everyone who knows Elena believes she deserves all the happiness in the world, because she has worked so hard to reach her goals."
        ),
        "mc": [
            {"q": "What did Elena do last month?",
             "options": ["She got married", "She told her manager she wanted a career change", "She moved to Spain", "She retired"],
             "answer": 1, "explanation": "The story says Elena told her manager she wanted to change careers last month."},
            {"q": "How long had Elena worked at the same company before deciding to change?",
             "options": ["Three years", "Five years", "Eight years", "Ten years"],
             "answer": 2, "explanation": "The text states she had worked there for eight years."},
            {"q": "Who proposed to Elena?",
             "options": ["Her manager", "Her grandmother", "Tomas", "Her cousin"],
             "answer": 2, "explanation": "Tomas, her boyfriend, proposed to her."},
            {"q": "What is Elena's grandmother's biggest wish?",
             "options": ["To become famous", "To live a long, healthy life and see her grandchildren married", "To get rich", "To live abroad"],
             "answer": 1, "explanation": "The grandmother's wish is explicitly stated in the story."},
            {"q": "Where do Elena and Tomas plan to move after the wedding?",
             "options": ["Italy", "Madrid, Spain", "London", "They are not planning to move"],
             "answer": 1, "explanation": "They decided to move to Madrid for two years."},
        ],
        "tf": [
            {"q": "Elena worked at the same company for eight years.", "answer": True},
            {"q": "Elena and Tomas got married last month.", "answer": False},
            {"q": "Tomas has always dreamed of living abroad.", "answer": True},
            {"q": "Elena's main goal is to become famous.", "answer": False},
            {"q": "Elena's grandmother is eighty years old.", "answer": True},
        ],
        "order_events": {
            "events": {
                "A": "Tomas proposed to Elena.",
                "B": "Elena graduated from university.",
                "C": "Elena told her manager she wanted to change careers.",
                "D": "Elena and Tomas decided to move to Madrid.",
                "E": "Elena and Tomas fell in love.",
                "F": "Elena hopes to retire early and travel the world.",
            },
            "correct_order": ["B", "E", "C", "A", "D", "F"],
        },
        "reading": {
            "title": "Making Big Changes: How People Reach Their Life Goals",
            "paragraphs": [
                "Every person imagines a different future. Some people would like to fall in love, get married, and have children; others dream about traveling the world, living abroad, or building a career that makes them proud. Researchers who study happiness say that people who write down clear goals are more likely to reach them, even when the path is not easy.",
                "Camila is a good example. For six years, she worked at a bank, but she never felt satisfied. She had always loved baking, so last year she decided to open her own small bakery. The process involved plenty of hassle, from getting permits to hiring her first employee, and she often had a lot on her plate. Still, she was going to make it work no matter what. Camila is going to open a second location next spring, something she never imagined when she was still counting money behind a bank counter.",
                "Marco and Sofia met while studying abroad in Canada. They fell in love almost immediately, and after graduation, they realized neither of them wanted to settle down in their home country right away. Instead, they would like to spend a few more years working overseas before deciding where to build a permanent home. Their families were surprised by the decision, but Marco and Sofia believe that going the extra mile now will give them more choices later in life.",
                "Not every goal is reached exactly as planned, and that is perfectly normal. Some people change careers more than once before finding the right fit; others discover that what they truly wanted was different from what they expected. What matters most, according to psychologists, is not only the destination but the journey itself. People who keep trying, learn from failure, and adjust their plans usually feel more successful in the end, even if they never become rich or famous.",
            ],
            "mc": [
                {"q": "According to the text, what did Camila do before opening her bakery?",
                 "options": ["She studied abroad", "She worked at a bank", "She was a professional baker", "She traveled the world"],
                 "answer": 1, "explanation": "Paragraph 2 states Camila worked at a bank for six years."},
                {"q": "Where did Marco and Sofia meet?",
                 "options": ["At a bakery", "At a bank", "While studying abroad in Canada", "At a wedding"],
                 "answer": 2, "explanation": "Paragraph 3 states they met while studying abroad in Canada."},
                {"q": "What does Camila plan to do next spring?",
                 "options": ["Retire", "Open a second bakery location", "Move abroad", "Return to the bank"],
                 "answer": 1, "explanation": "Paragraph 2 mentions she is going to open a second location next spring."},
            ],
            "tfnm": [
                {"q": "Camila's family helped her open the bakery.", "answer": "Not Mentioned"},
                {"q": "Marco and Sofia want to settle down in their home country immediately.", "answer": "False"},
                {"q": "Researchers say writing down goals can help people achieve them.", "answer": "True"},
            ],
            "vocab": [
                {"q": "In paragraph 2, the word 'hassle' is closest in meaning to...",
                 "options": ["an easy task", "an annoyance or difficulty", "a type of bread", "a business plan"],
                 "answer": 1, "explanation": "'Hassle' describes something that causes trouble or difficulty."},
                {"q": "In paragraph 3, the phrase 'settle down' is closest in meaning to...",
                 "options": ["to travel constantly", "to establish a stable home", "to become famous", "to change jobs frequently"],
                 "answer": 1, "explanation": "'Settle down' means to start living a stable, permanent life somewhere."},
            ],
            "inference": [
                {"q": "What can we infer about Camila's personality based on paragraph 2?",
                 "options": ["She is afraid of taking risks", "She is determined and hard-working", "She dislikes her old job intensely", "She prefers stability over change"],
                 "answer": 1, "explanation": "Despite the hassle, she kept working toward her goal, which shows determination."},
                {"q": "Why does the text suggest that reaching a goal exactly as planned isn't the only thing that matters?",
                 "options": ["Because most people never reach their goals", "Because the journey and effort also matter, according to psychologists", "Because money is more important than goals", "Because plans always fail"],
                 "answer": 1, "explanation": "Paragraph 4 explains that the journey itself matters, not only the final destination."},
            ],
        },
        "word_bank": ["grab a bite", "call it a day", "have a lot on your plate", "go the extra mile",
                      "get a promotion", "change careers", "fall in love", "flexible hours"],
        "vocab_sentences": [
            {"q": "After the meeting, my colleague and I decided to ______ at the café near the office.",
             "answer": "grab a bite"},
            {"q": "It's already 7 p.m.; let's ______ and finish the report tomorrow.",
             "answer": "call it a day"},
            {"q": "My manager has ______ this month, so she started coming home very late.",
             "answer": "have a lot on her plate", "accept": ["a lot on her plate", "have a lot on her plate"]},
            {"q": "If you want that promotion, you need to ______ and offer to help with extra projects.",
             "answer": "go the extra mile"},
            {"q": "After ten years at the company, Mr. Lopez finally received ______.",
             "answer": "a promotion", "accept": ["a promotion", "get a promotion"]},
            {"q": "Instead of staying in the same job forever, some people decide to ______ in their thirties or forties.",
             "answer": "change careers"},
            {"q": "Sofia and Daniel ______ during their first year of university and got married two years later.",
             "answer": "fell in love"},
            {"q": "Many young professionals prefer companies that offer ______ so they can choose their own work schedule.",
             "answer": "flexible hours"},
        ],
        "grammar_mc": [
            {"q": "She ____ like to live abroad someday.", "options": ["would", "is", "does", "has"],
             "answer": 0, "explanation": "'Would like' is the correct structure to express a wish for the future."},
            {"q": "____ they like to get married next year?", "options": ["Would", "Are", "Do", "Will"],
             "answer": 0, "explanation": "Yes/no questions with 'would like' begin with 'Would'."},
            {"q": "Choose the correct question.",
             "options": ["Who would like to retire early?", "Who would like retire early?", "Who does like to retire early?", "Who liking to retire early?"],
             "answer": 0, "explanation": "When 'who' is the subject, there is no inversion, but 'to' is still required before the infinitive."},
            {"q": "We ____ going to move to another city next month.", "options": ["are", "would", "do", "have"],
             "answer": 0, "explanation": "'Be going to' uses am/is/are + going to + base form."},
            {"q": "Choose the correct negative form.",
             "options": ["She isn't going to change careers.", "She not going to change careers.", "She doesn't going to change careers.", "She isn't go to change careers."],
             "answer": 0, "explanation": "The negative of 'be going to' is formed with isn't/aren't/am not + going to + base form."},
            {"q": "____ he going to send out the invitations?", "options": ["Is", "Does", "Would", "Has"],
             "answer": 0, "explanation": "Questions with 'be going to' begin with the verb 'be' (is/are/am)."},
            {"q": "I'd like ____ a new car this year.", "options": ["to buy", "buying", "buy", "bought"],
             "answer": 0, "explanation": "'Would like' is followed by an infinitive (to + base form)."},
            {"q": "Which sentence correctly expresses a future plan?",
             "options": ["He's going to retire next year.", "He's retire next year.", "He going to retire next year.", "He retires going next year."],
             "answer": 0, "explanation": "The correct structure is subject + be + going to + base form."},
        ],
        "grammar_fill": [
            {"q": "I ______________ (would like) to graduate next year.", "answer": "would like to graduate"},
            {"q": "They ______________ (be going to) organize a party for the promotion.", "answer": "are going to organize"},
            {"q": "______________ your sister ______________ (would like) to live abroad?", "answer": "would your sister like",
             "accept": ["would your sister like", "would she like"]},
            {"q": "He ______________ (be going to - negative) attend the wedding.", "answer": "isn't going to",
             "accept": ["isn't going to", "is not going to"]},
            {"q": "Who ______________ (would like) to change careers this year?", "answer": "would like"},
        ],
        "writing_topics": [
            "Describe your life goals for the next ten years.",
            "Write about someone you know who changed careers. What happened?",
            "Would you like to live abroad someday? Why or why not?",
            "Describe your idea of a perfect job and explain why it's attractive to you.",
        ],
    },

    "B": {
        "audio_text": (
            "Daniel has always had one big dream: to become a famous musician. "
            "Two years ago, he graduated from music school, and since then, he has been trying to find his place in the industry. "
            "His parents wanted him to get a stable job, but Daniel decided to follow his passion instead. "
            "Last spring, he moved to a bigger city because he thought it would give him better opportunities to perform. "
            "At first, life was difficult. He had a lot on his plate: he had to work in a restaurant during the day and practice music at night. "
            "He often had no time to grab a bite before rushing to a rehearsal. "
            "Then, a few months ago, everything changed. A music producer heard Daniel play at a small café and offered him a recording contract. "
            "Daniel couldn't believe it, his dream was finally coming true. "
            "He decided to go the extra mile and recorded an entire album in just two months. "
            "When the album was released, it became very popular, and Daniel started to get rich from ticket sales and streaming. "
            "However, becoming famous also changed his life in unexpected ways. Fans recognized him everywhere, and he had less privacy. "
            "Despite the fame and the money, Daniel says his real goals are simpler: he would like to fall in love, get married one day, and have children. "
            "He also hopes to live a long, healthy life so he can enjoy his success with the people he loves. "
            "His grandfather always told him, you deserve everything you've worked for, and Daniel finally believes it's true."
        ),
        "mc": [
            {"q": "What was Daniel's biggest dream?",
             "options": ["To become a doctor", "To become a famous musician", "To get rich quickly", "To move abroad"],
             "answer": 1, "explanation": "The story opens by stating his dream was to become a famous musician."},
            {"q": "What did Daniel do before he became successful?",
             "options": ["He worked in a restaurant and practiced music at night", "He worked as a teacher", "He studied medicine", "He lived with his grandfather"],
             "answer": 0, "explanation": "The text says he worked in a restaurant during the day and practiced at night."},
            {"q": "Who offered Daniel a recording contract?",
             "options": ["His parents", "A music producer", "His grandfather", "A restaurant owner"],
             "answer": 1, "explanation": "A music producer heard him play and offered the contract."},
            {"q": "How long did it take Daniel to record his album?",
             "options": ["Two weeks", "Two months", "Two years", "One year"],
             "answer": 1, "explanation": "The text says he recorded the entire album in two months."},
            {"q": "What are Daniel's simpler goals, according to the story?",
             "options": ["To become more famous", "To fall in love, get married, and have children", "To move to another country", "To retire early"],
             "answer": 1, "explanation": "The story states his real goals are to fall in love, get married, and have children."},
        ],
        "tf": [
            {"q": "Daniel graduated from music school two years ago.", "answer": True},
            {"q": "Daniel's parents wanted him to become a musician.", "answer": False},
            {"q": "Daniel moved to a bigger city to find more opportunities.", "answer": True},
            {"q": "Daniel became famous and rich immediately after graduating.", "answer": False},
            {"q": "Daniel's grandfather told him he deserves what he worked for.", "answer": True},
        ],
        "order_events": {
            "events": {
                "A": "A music producer offered Daniel a recording contract.",
                "B": "Daniel graduated from music school.",
                "C": "Daniel moved to a bigger city.",
                "D": "Daniel recorded his album in two months.",
                "E": "Daniel's album became popular and he started to get rich.",
                "F": "Daniel decided he wants to fall in love, get married, and have children.",
            },
            "correct_order": ["B", "C", "A", "D", "E", "F"],
        },
        "reading": {
            "title": "The Road to a Dream Job",
            "paragraphs": [
                "Not everyone defines success the same way. Some people would like to get rich or become famous, while others simply hope to retire early and travel, or to enjoy a peaceful life with their family. Career counselors often say that understanding your own definition of success is the first step toward reaching your goals, even if that definition changes over time.",
                "Diego spent twelve years working in finance, earning a stable salary and good perks, but he always felt something was missing. He wanted more of a challenge and more flexible hours, so two years ago he quit his job to become a freelance photographer. The income is irregular, and finding new clients can be a hassle, but Diego says he wouldn't trade this atmosphere of freedom for anything. He is going to open his own small studio next year, something he never imagined while sitting in an office all day.",
                "Ana has dreamed of becoming a famous singer since she was a child. She fell in love with music the first time she sang in front of an audience, and she never stopped practicing. Ana is going to release her first album next month, and she would like to live abroad in Los Angeles for a while to record with well-known producers. Her family worries about the risks of the music industry, but Ana believes that if she doesn't try, she will always wonder what could have happened.",
                "These two stories show that success has many different faces. For Diego, it means having control over his schedule and a positive atmosphere, even without a large salary. For Ana, it means chasing a childhood dream, whatever feedback or criticism she receives along the way. Experts agree that people who spend time thinking about what truly matters to them, rather than copying someone else's plan, usually end up happier in the long run.",
            ],
            "mc": [
                {"q": "What was missing from Diego's life when he worked in finance?",
                 "options": ["Money", "A challenge and flexible hours", "Friends", "Education"],
                 "answer": 1, "explanation": "Paragraph 2 states he wanted more of a challenge and more flexible hours."},
                {"q": "What does Ana plan to do next month?",
                 "options": ["Retire", "Release her first album", "Move back home", "Change careers"],
                 "answer": 1, "explanation": "Paragraph 3 states Ana is going to release her first album next month."},
                {"q": "According to paragraph 4, what does success mean for Diego?",
                 "options": ["Having a large salary", "Having control over his schedule and a positive atmosphere", "Becoming famous", "Living abroad"],
                 "answer": 1, "explanation": "Paragraph 4 explicitly describes what success means for Diego."},
            ],
            "tfnm": [
                {"q": "Diego worked in finance for twelve years.", "answer": "True"},
                {"q": "Ana's family fully supports her decision without any worries.", "answer": "False"},
                {"q": "Ana practiced singing every day as a child.", "answer": "Not Mentioned"},
            ],
            "vocab": [
                {"q": "In paragraph 2, the word 'irregular' is closest in meaning to...",
                 "options": ["predictable", "not consistent", "very high", "illegal"],
                 "answer": 1, "explanation": "'Irregular' describes something that does not happen at a fixed, predictable rate."},
                {"q": "In paragraph 2, the phrase 'wouldn't trade' is closest in meaning to...",
                 "options": ["wouldn't exchange", "would sell", "would buy", "would ignore"],
                 "answer": 0, "explanation": "'Wouldn't trade something for anything' means he would not exchange it for anything else."},
            ],
            "inference": [
                {"q": "What can we infer about Diego's priorities based on paragraph 2?",
                 "options": ["He values financial security above everything", "He values freedom and personal satisfaction more than a stable salary", "He regrets leaving his finance job", "He wants to return to an office job"],
                 "answer": 1, "explanation": "He gave up a stable salary for more freedom and challenge, showing his priorities."},
                {"q": "Why does the text mention that Ana's family worries about the music industry?",
                 "options": ["To show that Ana made the wrong choice", "To show that pursuing a dream can involve risk and require courage", "To criticize Ana's parents", "To suggest Ana should quit music"],
                 "answer": 1, "explanation": "It highlights the risk involved in following a dream, and Ana's courage to take it anyway."},
            ],
        },
        "word_bank": ["have a lot on your plate", "I wish", "you deserve", "get rich",
                      "live abroad", "a challenge", "retire", "become famous"],
        "vocab_sentences": [
            {"q": "Working two jobs and studying at night gave Marta ______ that year.",
             "answer": "a lot on her plate", "accept": ["a lot on her plate", "have a lot on her plate"]},
            {"q": "\"______ I could speak five languages fluently,\" said Carlos, looking at his study notes.",
             "answer": "I wish"},
            {"q": "After the concert, the singer's fans shouted that ______ all the success in the world.",
             "answer": "she deserves", "accept": ["she deserves", "you deserve"]},
            {"q": "Some people dream about winning the lottery and becoming ______ overnight.",
             "answer": "rich", "accept": ["rich", "get rich"]},
            {"q": "Many young engineers move to Germany because they would like to ______ for a few years.",
             "answer": "live abroad"},
            {"q": "The new employee asked for more responsibilities because she wanted ______ in her position.",
             "answer": "a challenge"},
            {"q": "After forty years of teaching, Mr. Alvarez plans to ______ next June.",
             "answer": "retire"},
            {"q": "Winning an international award helped the young author ______ almost overnight.",
             "answer": "become famous"},
        ],
        "grammar_mc": [
            {"q": "My parents ____ like to see me graduate this year.", "options": ["would", "is", "does", "has"],
             "answer": 0, "explanation": "'Would like' is the correct structure to express a wish for the future."},
            {"q": "____ you like to change careers someday?", "options": ["Would", "Are", "Do", "Will"],
             "answer": 0, "explanation": "Yes/no questions with 'would like' begin with 'Would'."},
            {"q": "Choose the correct question.",
             "options": ["Who would like to become famous?", "Who would liking become famous?", "Who does would like become famous?", "Who would like becoming famous?"],
             "answer": 0, "explanation": "'Would like' is followed by the infinitive 'to become', with no auxiliary inversion when 'who' is the subject."},
            {"q": "She ____ going to retire next year.", "options": ["is", "would", "do", "has"],
             "answer": 0, "explanation": "'Be going to' uses am/is/are + going to + base form."},
            {"q": "Choose the correct negative form.",
             "options": ["They aren't going to move abroad.", "They not going to move abroad.", "They doesn't going to move abroad.", "They aren't go to move abroad."],
             "answer": 0, "explanation": "The negative of 'be going to' is formed with isn't/aren't/am not + going to + base form."},
            {"q": "____ we going to get a promotion this year?", "options": ["Are", "Does", "Would", "Has"],
             "answer": 0, "explanation": "Questions with 'be going to' begin with the verb 'be' (are/is/am)."},
            {"q": "He'd like ____ his own business.", "options": ["to start", "starting", "start", "started"],
             "answer": 0, "explanation": "'Would like' is followed by an infinitive (to + base form)."},
            {"q": "Which sentence correctly expresses a future plan?",
             "options": ["They're going to travel next summer.", "They're travel going next summer.", "They going to travel next summer.", "They travels going to next summer."],
             "answer": 0, "explanation": "The correct structure is subject + be + going to + base form."},
        ],
        "grammar_fill": [
            {"q": "She ______________ (would like) to become a famous singer.", "answer": "would like to become"},
            {"q": "We ______________ (be going to) buy a house next year.", "answer": "are going to buy"},
            {"q": "______________ he ______________ (would like) to retire early?", "answer": "would he like",
             "accept": ["would he like"]},
            {"q": "I ______________ (be going to - negative) change careers this year.", "answer": "am not going to",
             "accept": ["am not going to", "'m not going to"]},
            {"q": "Who ______________ (would like) to live abroad next year?", "answer": "would like"},
        ],
        "writing_topics": [
            "What does \"success\" mean to you? Describe your own definition.",
            "Write about a dream you would like to make come true and how you plan to do it.",
            "Do you think money and fame are necessary to be happy? Explain your opinion.",
            "Describe a person who inspires you to reach your goals.",
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
    st.subheader("📐 Module 4: Grammar — Would like / Be going to")
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

    st.title(f"UNIT 10: LIFE GOALS AND PLANS — Exam (Version {version})")
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
    st.header("Module 4: Grammar — Would like / Be going to")
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

    st.sidebar.title("🎯 Unit 10: Life Goals and Plans")
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

    st.title("🎯 Unit 10: Life Goals and Plans")
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
