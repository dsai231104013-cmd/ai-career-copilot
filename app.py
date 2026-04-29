from reportlab.pdfgen import canvas
import json
import os
from reportlab.lib.pagesizes import A4
import matplotlib.pyplot as plt
import streamlit as st 
from PyPDF2 import PdfReader
import speech_recognition as sr
import tempfile
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import re
import pyttsx3
from reportlab.lib import colors

from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.graphics.shapes import Drawing, Circle
import pdfkit
import os
from jinja2 import Template
import base64
import streamlit as st

st.set_page_config(
    page_title="AI Career Copilot",
    page_icon="💼",
    layout="wide"
)
st.markdown("""
<style>

/* GLOBAL BACKGROUND */
.stApp {
    background: radial-gradient(circle at top left, #0f172a, #020617);
    color: white;
    font-family: 'Arial';
}

/* FLOATING GLASS EFFECT */
.block-container {
    padding: 2rem 3rem;
}

/* GLASS CARDS */
.card, div[data-testid="stVerticalBlock"] {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 18px;
    padding: 20px;
    box-shadow: 0px 8px 30px rgba(0,0,0,0.4);
}

/* BUTTONS (MODERN) */
.stButton > button {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    color: white;
    border-radius: 12px;
    padding: 10px 22px;
    border: none;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0px 0px 20px rgba(37,99,235,0.5);
}

/* INPUT FIELDS */
.stTextInput input, .stTextArea textarea {
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.2);
    background: rgba(255,255,255,0.05);
    color: white;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: rgba(2,6,23,0.95);
    border-right: 1px solid rgba(255,255,255,0.1);
}

/* ANIMATED TITLE */
@keyframes glow {
    0% {text-shadow: 0 0 5px #2563eb;}
    50% {text-shadow: 0 0 20px #3b82f6;}
    100% {text-shadow: 0 0 5px #2563eb;}
}

h1 {
    animation: glow 3s infinite;
}

/* METRICS STYLE */
[data-testid="stMetricValue"] {
    color: #60a5fa;
    font-size: 22px;
}

</style>
""", unsafe_allow_html=True)
st.markdown("""
<div style="
text-align:center;
padding:40px;
border-radius:20px;
background: linear-gradient(135deg, #1e3a8a, #0f172a);
box-shadow: 0px 10px 40px rgba(0,0,0,0.6);
margin-bottom:25px;
">

<h1 style="font-size:40px;">🚀 AI Career Copilot</h1>
<p style="font-size:16px; opacity:0.8;">
Build • Improve • Train • Get Hired — Powered by AI
</p>

</div>
""", unsafe_allow_html=True)
def image_to_base64(image_file):
    if image_file is None:
        return ""
    return base64.b64encode(image_file.read()).decode()


def improve_data(resume_text, skills, image_path=None):

    lines = resume_text.split("\n") if resume_text else []
    # ---- ATS KEYWORD BOOST (simple AI upgrade) ----
    ats_keywords = [
        "problem solving", "teamwork", "communication",
        "leadership", "python", "data analysis", "AI"
    ]

    return {
        "name": "Candidate",
        "email": "email@example.com",
        "phone": "0300-0000000",
        "location": "Pakistan",

        "profile": resume_text[:500] if resume_text else "Professional candidate...",

        "skills": [s.title() for s in skills if s],

        "experience": lines[:5],
        "education": lines[5:10],

        "projects": [
            "AI Resume Builder Project",
            "Career Copilot System",
            "Job Matching Tool"
        ],

        # ⭐ NEW: image path pass
        "image": image_path
    }
def create_cv_pdf(data, image_base64=None):

    template_path = "europass.html"

    if not os.path.exists(template_path):
        raise FileNotFoundError("europass.html not found")

    # inject image
    data["image_base64"] = image_base64

    with open(template_path, "r", encoding="utf-8") as f:
        template = Template(f.read())

    html = template.render(**data)

    with open("output.html", "w", encoding="utf-8") as f:
        f.write(html)

    config = pdfkit.configuration(
        wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    )

    options = {
        "enable-local-file-access": None,   # ⭐ MOST IMPORTANT FIX
        "encoding": "UTF-8",
        "no-stop-slow-scripts": None,
        "load-error-handling": "ignore"
    }

    pdf_file = "canva_style_cv.pdf"

    pdfkit.from_file(
        "output.html",
        pdf_file,
        configuration=config,
        options=options
    )

    return pdf_file# ---------- VOICE FUNCTION ----------
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)
    engine.setProperty('volume', 1.0)
    engine.say(text)
    engine.runAndWait()
# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="AI Career Copilot 🚀",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)
# ---------- CSS ----------
# ---------- SIDEBAR ----------
# ---------- SIDEBAR ----------
st.sidebar.markdown('<h1 style="color:white;">🚀 AI Career Copilot</h1>', unsafe_allow_html=True)
section = st.sidebar.radio("Navigate", ["AI Chatbot 🤖", "Resume Upload", "Skills & Jobs", "Interview", "Results","Feedback","resume improvement","Dashboard"])
if st.sidebar.button("💾 Save Progress"):
    save_data()
    st.sidebar.success("Progress Saved Successfully!")
st.sidebar.markdown("""
<div style="
margin-top:20px;
padding:12px;
border-radius:12px;
background:rgba(255,255,255,0.1);
color:white;
font-size:13px;
text-align:center;
box-shadow:0px 2px 10px rgba(0,0,0,0.2);
">
⚡ AI Powered Career System<br>
Build • Learn • Get Hired
</div>
""", unsafe_allow_html=True)

# ---------- SESSION ----------
if "resume_text" not in st.session_state: st.session_state.resume_text = ""
if "skills" not in st.session_state: st.session_state.skills = []
if "jobs" not in st.session_state: st.session_state.jobs = []
if "answers" not in st.session_state: st.session_state.answers = []
if "scores" not in st.session_state: st.session_state.scores = []
# ---------- SAVE / LOAD SYSTEM ----------

DATA_FILE = "career_data.json"

def save_data():
    data = {
        "resume_text": st.session_state.get("resume_text", ""),
        "skills": st.session_state.get("skills", []),
        "jobs": st.session_state.get("jobs", []),
        "answers": st.session_state.get("answers", []),
        "scores": st.session_state.get("scores", [])
    }

    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)

        st.session_state.resume_text = data.get("resume_text", "")
        st.session_state.skills = data.get("skills", [])
        st.session_state.jobs = data.get("jobs", [])
        st.session_state.answers = data.get("answers", [])
        st.session_state.scores = data.get("scores", [])

load_data()

# ---------- CHATBOT ----------
# ---------- CHATBOT ----------
if section == "AI Chatbot 🤖":

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("🤖 AI Chatbot")

    # ---------- INIT ----------
    if "chat_started" not in st.session_state:
        st.session_state.chat_started = True
        st.session_state.chat_history = []

    if "user_name" not in st.session_state:
        st.session_state.user_name = ""

    if "ask_name" not in st.session_state:
        st.session_state.ask_name = False

    # ---------- INTRO ----------
    if len(st.session_state.chat_history) == 0:
        intro = "Hello! I am Kriss 🤖, your AI Career Copilot. Ask me anything about careers, skills, resume or interviews."
        st.session_state.chat_history.append("🤖 Bot: " + intro)
        speak(intro)

    # ---------- CHAT DISPLAY ----------
    for chat in st.session_state.chat_history:

        if "You:" in chat:
            st.markdown(f"""
            <div style="
                background:#25D366;
                color:white;
                padding:10px;
                border-radius:15px;
                margin:5px;
                width:70%;
                margin-left:auto;
                text-align:right;
                box-shadow:2px 2px 10px rgba(0,0,0,0.3);
            ">
            {chat}
            </div>
            """, unsafe_allow_html=True)

        else:
            st.markdown(f"""
            <div style="
                background:#2c3e50;
                color:white;
                padding:10px;
                border-radius:15px;
                margin:5px;
                width:70%;
                box-shadow:2px 2px 10px rgba(0,0,0,0.3);
            ">
            {chat}
            </div>
            """, unsafe_allow_html=True)

    # ---------- INPUT ----------
    user_input = st.text_input("💬 Ask me anything...")

    # ---------- AI FUNCTION ----------
    def chatbot_reply(text):

        text = text.lower()

        # ---------- NAME FLOW ----------
        if st.session_state.ask_name:
            st.session_state.user_name = text.title()
            st.session_state.ask_name = False

            reply = f"Nice to meet you {st.session_state.user_name}  How can I help you today?"
            speak(reply)
            return reply

        # ---------- HELLO FLOW ----------
        if "hello" in text:
            st.session_state.ask_name = True
            return "Hello What is your name?"

        # ---------- PERSONAL ----------
        elif "your name" in text:
            return "My name is Kriss 🤖, your AI Career Copilot."

        elif "your age" in text:
            return "I don't have age, I am an AI assistant built to help your career."

        elif "who are you" in text:
            return "I am Kriss 🤖, your AI Career Copilot."

        # ---------- CAREER ----------
        elif "python" in text:
            return "Python is used in AI, data science and web development."

        elif "resume" in text:
            return "A strong resume should show skills, projects and experience clearly."

        elif "interview" in text:
            return "Focus on confidence, communication and structured answers."

        elif "job" in text:
            return "Improve skills like Python, AI and communication for better jobs."

        elif "ai" in text:
            return "AI means Artificial Intelligence. It simulates human intelligence."

        else:
            return "Ask me about resume, jobs, skills or interviews "

    # ---------- SEND BUTTON ----------
    if st.button("Send"):

        if user_input:

            user_msg = f" You: {user_input}"
            bot_reply = chatbot_reply(user_input)
            bot_msg = f"🤖 Bot: {bot_reply}"

            st.session_state.chat_history.append(user_msg)
            st.session_state.chat_history.append(bot_msg)

            speak(bot_reply)

            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)# ---------- RESUME UPLOAD ----------
elif section == "Resume Upload":

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("📄 Upload Resume")

    # ---------- VOICE INTRO ----------
    if "resume_voice" not in st.session_state:
        msg = """Please upload your resume to continue.
        I will analyze your skills, experience and suggest best job roles for you."""
        st.write(msg)
        speak(msg)
        st.session_state.resume_voice = True

    # ---------- FILE UPLOAD ----------
    uploaded_file = st.file_uploader("Upload PDF Resume", type=["pdf"])

    if uploaded_file:

        with st.spinner("🤖 AI is analyzing your resume..."):
            pdf = PdfReader(uploaded_file)
            text = ""

            for page in pdf.pages:
                if page.extract_text():
                    text += page.extract_text()

        st.session_state.resume_text = text

        # ---------- SUCCESS ----------
        st.success("✅ Resume uploaded successfully!")

        # ---------- RESUME STATS ----------
        word_count = len(text.split())

        st.subheader("📊 Resume Analysis")

        st.write("📄 Word Count:", word_count)

        # Simple quality score
        if word_count < 100:
            score = "⚠ Weak Resume"
        elif word_count < 300:
            score = "👍 Medium Resume"
        else:
            score = "🌟 Strong Resume"

        st.write("📌 Resume Strength:", score)

        # ---------- PREVIEW ----------
        st.subheader("📄 Resume Preview")
        st.text_area("Extracted Text", text[:1500], height=250)

        # ---------- AI MESSAGE ----------
        success_msg = f"""
Great! Your resume has been analyzed.

I detected {word_count} words.

Now I will extract your skills and recommend the best jobs for you.
"""
        st.write(success_msg)
        speak(success_msg)

    st.markdown('</div>', unsafe_allow_html=True)
# ---------- SKILLS ----------
elif section == "Skills & Jobs":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("🛠 Skills & 💼 Job Recommendations")

    text = st.session_state.resume_text

    if not text.strip():
        st.warning("⚠️ Please upload your resume first.")

    else:

        # -------- SKILL KEYWORDS --------
        skill_keywords = [
            "Python","Machine Learning","Artificial Intelligence","Deep Learning","Data Analysis",
            "Java","C++","SQL","Excel","Power BI","Tableau",
            "Web Development","HTML","CSS","JavaScript",
            "React","Node","Django","Flask",
            "Fitness","Training","Nutrition","Personal Training","Group Training",
            "Communication","Leadership","Teamwork","Problem Solving"
        ]

        # -------- JOB MAP --------
        job_map = {
            "Python": ["Data Scientist","AI Engineer","Backend Developer"],
            "Machine Learning": ["ML Engineer","AI Researcher"],
            "Artificial Intelligence": ["AI Developer","AI Specialist"],
            "Deep Learning": ["DL Engineer"],
            "Data Analysis": ["Data Analyst","Business Analyst"],
            "SQL": ["Database Analyst","Data Engineer"],
            "Excel": ["Financial Analyst","Business Analyst"],
            "Power BI": ["BI Developer"],
            "Tableau": ["Data Visualization Expert"],
            "Java": ["Software Engineer"],
            "C++": ["Game Developer","System Engineer"],
            "Web Development": ["Full Stack Developer"],
            "HTML": ["Frontend Developer"],
            "CSS": ["UI Developer"],
            "JavaScript": ["Frontend Developer"],
            "React": ["React Developer"],
            "Node": ["Backend Developer"],
            "Django": ["Python Web Developer"],
            "Flask": ["API Developer"],
            "Fitness": ["Personal Trainer","Fitness Coach"],
            "Training": ["Personal Trainer","Fitness Instructor"],
            "Nutrition": ["Nutritionist","Wellness Coach"],
            "Communication": ["HR","Manager"],
            "Leadership": ["Team Lead","Manager"],
            "Teamwork": ["Project Coordinator"],
            "Problem Solving": ["Consultant"],
            "General": ["Intern","Entry Level Job"]
        }

        # -------- SKILL DETECTION + CONFIDENCE --------
        skills = []
        skill_confidence = {}

        for s in skill_keywords:
            pattern = r'\b' + re.escape(s.lower()) + r'\b'
            matches = len(re.findall(pattern, text.lower()))

            if matches > 0:
                skills.append(s)
                skill_confidence[s] = min(100, matches * 40)

        if not skills:
            skills = ["General"]
            skill_confidence["General"] = 50

        # -------- JOB RECOMMENDATION --------
        jobs = []
        for s in skills:
            jobs.extend(job_map.get(s, []))

        jobs = list(set(jobs))

        # -------- SCORES --------
        skill_accuracy = min(100, len(skills) * 10)
        job_strength = min(100, len(jobs) * 5)

        # -------- SAVE STATE --------
        st.session_state.skills = skills
        st.session_state.jobs = jobs

        # -------- UI --------
        st.subheader("🧠 AI Intelligence Report")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Skill Detection Accuracy", f"{skill_accuracy}%")

        with col2:
            st.metric("Job Recommendation Strength", f"{job_strength}%")

        # -------- GRAPHS --------
        st.subheader("📊 Skill Confidence Graph")

        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()
        ax.bar(skill_confidence.keys(), skill_confidence.values())
        ax.set_ylabel("Confidence %")
        ax.set_xlabel("Skills")
        ax.set_xticklabels(skill_confidence.keys(), rotation=45)
        st.pyplot(fig)

        st.subheader("💼 Job Mapping Strength")

        job_scores = {}
        for j in jobs:
            job_scores[j] = 90  # simple strong weight (you can improve later)

        fig2, ax2 = plt.subplots()
        ax2.bar(job_scores.keys(), job_scores.values())
        ax2.set_ylabel("Relevance %")
        ax2.set_xlabel("Jobs")
        ax2.set_xticklabels(job_scores.keys(), rotation=45)
        st.pyplot(fig2)

        # -------- DISPLAY --------
        st.subheader("✅ Detected Skills")

        for k, v in skill_confidence.items():
            st.write(f"🔹 {k} — {v}% confidence")

        st.subheader("💼 Recommended Jobs")
        st.write(", ".join(jobs))

        # -------- AI EXPLANATION --------
        st.subheader("🤖 AI Insight")

        for s in skills:
            st.write(f"✔ Because you have **{s}**, you can explore roles like {job_map.get(s, [])}")
# ---------- INTERVIEW ----------
elif section == "Interview":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("🎤 AI Interview Practice")

    recognizer = sr.Recognizer()
# ---------- AI FEEDBACK FUNCTION ----------
    def ai_feedback(answer):
        answer = answer.lower()
        feedback = []

        if len(answer.split()) < 20:
            feedback.append("❌ Too short answer – explain more")

        if "because" not in answer:
            feedback.append("⚠ Add reasoning (because...)")

        if "example" not in answer:
            feedback.append("⚠ Add real-life example")

        if len(answer.split()) > 80:
            feedback.append("👍 Good detailed answer")

        if not feedback:
            feedback.append("🌟 Excellent structured answer")

        return feedback

    # ---------- QUESTIONS ----------
    if "questions" not in st.session_state:
        st.session_state.questions = [
            "Tell me about yourself",
            "What are your strengths and weaknesses?",
            "Why should we hire you?",
            "Describe a challenging situation"
        ]

    if "keyword_map" not in st.session_state:
        st.session_state.keyword_map = {
            st.session_state.questions[0]: ["experience", "skills", "projects", "background"],
            st.session_state.questions[1]: ["strength", "weakness", "improve", "learning"],
            st.session_state.questions[2]: ["skills", "value", "company", "contribute"],
            st.session_state.questions[3]: ["challenge", "problem", "solution", "team", "result"]
        }

    # ---------- SAFE INIT ----------
    if "q_index" not in st.session_state:
        st.session_state.q_index = 0

    if "answers" not in st.session_state:
        st.session_state.answers = [""] * len(st.session_state.questions)

    if "mode_selected" not in st.session_state:
        st.session_state.mode_selected = False

    if "mode" not in st.session_state:
        st.session_state.mode = None

    if "spoken_q" not in st.session_state:
        st.session_state.spoken_q = -1

    # ---------- EVALUATION ----------
    def evaluate_answer(answer, question):
        if not answer:
            return 0, "❌ No Answer"

        answer = answer.lower()
        words = answer.split()

        length_score = min(len(words) / 10, 1) * 25

        keywords = st.session_state.keyword_map.get(question, [])
        keyword_score = sum(1 for k in keywords if k in answer) / len(keywords) * 25

        repetition_penalty = 10 if len(set(words)) < len(words) * 0.6 else 0

        structure_bonus = 10 if any(w in answer for w in ["because", "for example", "my experience", "i think"]) else 0

        score = length_score + keyword_score + structure_bonus - repetition_penalty
        score = max(0, min(score, 100))

        if score >= 80:
            rank = "🌟 Excellent"
        elif score >= 60:
            rank = "👍 Good"
        elif score >= 40:
            rank = "⚠ Average"
        else:
            rank = "❌ Weak"

        return round(score, 1), rank

    # ---------- MODE SELECTION ----------
    if not st.session_state.mode_selected:
        mode = st.radio("Choose Interview Mode:", ["Text ✍️", "Voice 🎤"])

        if st.button("Start Interview"):
            st.session_state.mode = mode
            st.session_state.mode_selected = True
            st.session_state.q_index = 0
            st.session_state.answers = [""] * len(st.session_state.questions)
            speak(f"You selected {mode} mode. Let's begin.")

    else:
        mode = st.session_state.mode

        # ---------- TEXT MODE ----------
        if mode == "Text ✍️":
            st.subheader("📝 Answer All Questions Below")

            responses = []

            for i, q in enumerate(st.session_state.questions):
                st.write(f"Q{i+1}: {q}")
                ans = st.text_area(f"Answer {i+1}", key=f"text_{i}")
                responses.append(ans)

            if st.button("Submit Interview"):
                st.session_state.answers = responses
                st.success("✅ Interview Submitted Successfully!")
                st.info("👉 Go to Results section to see your AI evaluation")

        # ---------- VOICE MODE ----------
        else:
            if st.session_state.q_index < len(st.session_state.questions):

                q = st.session_state.questions[st.session_state.q_index]
                st.subheader(f"Now Answer: {q}")

                if st.session_state.spoken_q != st.session_state.q_index:
                    speak(q)
                    st.session_state.spoken_q = st.session_state.q_index

                # ---------- RECORD ----------
                def record_audio():
                    fs = 16000
                    duration = 6

                    st.info("🎤 Recording... Speak now")

                    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
                    sd.wait()

                    audio = np.int16(audio * 32767)

                    file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
                    write(file.name, fs, audio)

                    st.success("Recording complete")
                    return file.name

                def speech_to_text(file):
                    try:
                        with sr.AudioFile(file) as source:
                            audio = recognizer.record(source)
                        return recognizer.recognize_google(audio)
                    except:
                        return ""

                # ---------- RECORD BUTTON ----------
                if st.button("🎤 Record Answer"):
                    file = record_audio()
                    answer = speech_to_text(file)

                    # SAFE SAVE (FIXED ERROR)
                    st.session_state.answers[st.session_state.q_index] = answer

                    score, rank = evaluate_answer(answer, q)

                    st.success(f"Your Answer: {answer}")
                    st.info(f"Score: {score}/100 | {rank}")

                # ---------- NEXT QUESTION ----------
                if st.button("➡️ Next Question"):
                    st.session_state.q_index += 1
                    st.session_state.spoken_q = -1

            else:
                st.success("🎉 Interview Completed!")
                speak("Interview completed. Good job!Now you may leave the interview section and saw your results in next section thank you")

    st.markdown('</div>', unsafe_allow_html=True)
elif section == "Results":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("📊 AI Interview Results Dashboard")

    def ai_feedback(answer):
        if not answer or not answer.strip():
            return ["No answer provided"]

        feedback = []

        if len(answer.split()) < 10:
            feedback.append("Too short answer")

        if "because" not in answer.lower():
            feedback.append("Add reasoning")

        if not feedback:
            feedback.append("Good answer")

        return feedback

    def evaluate_answer(answer, question):
        if not answer:
            return 0, "❌ No Answer"

        words = answer.split()

        length_score = min(len(words) / 10, 1) * 25

        keywords = st.session_state.keyword_map.get(question, [])
        keyword_score = (
            sum(1 for k in keywords if k in answer.lower()) / len(keywords) * 25
            if keywords else 0
        )

        structure_bonus = 10 if any(
            w in answer.lower() for w in ["because", "for example", "i think"]
        ) else 0

        score = length_score + keyword_score + structure_bonus
        score = max(0, min(score, 100))

        rank = "🌟 Excellent" if score >= 80 else "👍 Good" if score >= 60 else "⚠ Average"

        return round(score, 1), rank

    if st.session_state.answers:

        total = 0
        count = 0

        for i, ans in enumerate(st.session_state.answers):
            if i < len(st.session_state.questions):
                q = st.session_state.questions[i]

                score, rank = evaluate_answer(ans, q)

                st.write(f"Q{i+1}: {q}")
                st.write(f"Answer: {ans}")
                st.write(f"Score: {score}/100 | {rank}")

                st.write("AI Feedback:")
                for f in ai_feedback(ans):
                    st.write("•", f)

                st.markdown("---")

                total += score
                count += 1

        if count > 0:
            st.metric("Final Score", f"{total/count:.1f}/100")

    else:
        st.info("No interview data found")

    st.markdown('</div>', unsafe_allow_html=True)
# ---------- FEEDBACK ----------
elif section == "Feedback":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("📝 We Value Your Feedback")

    st.write("Help us improve your AI Career Copilot experience 🚀")

    # Rating
    st.subheader("⭐ Rate Your Experience")
    rating = st.radio(
        "How would you rate this app?",
        ["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"],
        horizontal=True
    )

    # Feedback text
    st.subheader("💬 Your Feedback")
    feedback_text = st.text_area("Write your suggestions or issues here...")

    # Optional name/email
    name = st.text_input("👤 Your Name (optional)")
    email = st.text_input("📧 Email (optional)")

    # Submit button
    if st.button("🚀 Submit Feedback"):
        if feedback_text.strip() == "":
            st.warning("Please write some feedback before submitting!")
        else:
            st.success("✅ Thank you for your feedback! We appreciate your input 💙")
            st.info(f"Rating: {rating}")
            st.info(f"Feedback: {feedback_text}")

    st.markdown('</div>', unsafe_allow_html=True)
# ================= RESUME IMPROVEMENT =================
elif section == "resume improvement":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("📄 AI Resume Improvement Engine")

    # ---------- GET DATA FIRST ----------
    resume_text = st.session_state.get("resume_text", "")
    skill_keywords = st.session_state.get("skills", [])

    if not resume_text.strip():
        st.warning("⚠️ Please upload your resume first in Resume Upload section.")
        st.stop()

    if not skill_keywords:
        skill_keywords = ["Python", "Communication", "Problem Solving"]

    # ---------- ATS SCORE FUNCTION ----------
    def calculate_ats_score(resume_text, skills):
        resume_text = resume_text.lower()

        if not skills:
            return 0, [], []

        matched = []
        missing = []

        for skill in skills:
            if skill.lower() in resume_text:
                matched.append(skill)
            else:
                missing.append(skill)

        score = (len(matched) / len(skills)) * 100
        return round(score, 1), matched, missing

    # ---------- CALCULATE ATS ----------
    ats_score, matched, missing = calculate_ats_score(resume_text, skill_keywords)

    st.subheader("📊 ATS Score")
    st.metric("ATS Compatibility", f"{ats_score}/100")

    st.write("✅ Matched:", matched)
    st.write("❌ Missing:", missing)

    # ---------- IMPROVED RESUME ----------
    improved = f"""
========================
🚀 AI OPTIMIZED RESUME
========================

📌 SKILLS IDENTIFIED:
{', '.join(skill_keywords)}

📌 SUMMARY:
Dedicated and motivated professional with strong expertise in {skill_keywords[0]} 
and hands-on experience in real-world problem solving.

📌 TECHNICAL SKILLS:
{chr(10).join(['- ' + s for s in skill_keywords])}

📌 PROJECT HIGHLIGHT:
- AI Career Copilot (Streamlit + Python)
- Resume Analyzer using NLP techniques
- Voice-based Interview System

📌 STRENGTHS:
- Quick Learner
- Strong Communication
- Problem Solving Ability
- Analytical Thinking

📌 RECOMMENDATION:
Add real projects, GitHub links, and internship experience to strengthen profile.
"""

    st.text_area("📄 Improved Resume Preview", improved, height=400)
# ================= STREAMLIT UI =================
uploaded_file = st.file_uploader("Upload Profile Image", type=["png", "jpg", "jpeg","jfif"])

image_path = None

if uploaded_file is not None:
    image_path = "profile.jpg"
    with open(image_path, "wb") as f:
        f.write(uploaded_file.read())
if st.button("Generate CV"):

    # ✅ SAFE GLOBAL DATA
    resume_text = st.session_state.get("resume_text", "")
    skills = st.session_state.get("skills", [])

    # 👇 NEW: image support
    uploaded_image = st.session_state.get("uploaded_image", None)

    if not resume_text.strip():
        st.warning("⚠ Please upload resume first")
        st.stop()

    if not skills:
        st.warning("⚠ No skills detected yet")
        skills = ["Communication", "Problem Solving"]

    # ✅ CREATE DATA
    data = improve_data(resume_text, skills, image_path)

    # 👇 convert image to base64 (IMPORTANT)
    image_base64 = image_to_base64(uploaded_image)

    # ✅ GENERATE PDF (WITH IMAGE NOW)
    pdf = create_cv_pdf(data, image_base64)

    # ✅ DOWNLOAD BUTTON (FIXED)
    with open(pdf, "rb") as f:
        st.download_button(
            "⬇ Download CV",
            data=f,
            file_name="canva_cv.pdf",
            mime="application/pdf")
# ---------- DASHBOARD (FIXED) ----------
elif section == "Dashboard":
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.header("📊 AI Performance Dashboard")

    skills = st.session_state.get("skills", [])
    jobs = st.session_state.get("jobs", [])
    answers = st.session_state.get("answers", [])
    questions = st.session_state.get("questions", [])

    # ---------- SAFE SCORE CALCULATION ----------
    def quick_score(ans):
        if not ans:
            return 0
        words = len(ans.split())
        return min(100, words * 8)  # simple but stable scoring

    scores = [quick_score(a) for a in answers if a]
    st.session_state.scores = scores

    # ---------- SKILLS CHART ----------
    st.subheader("🛠 Skills Strength Overview")

    if skills:
        fig, ax = plt.subplots()
        ax.barh(skills, [1]*len(skills))
        ax.set_xlabel("Detected Skills")
        st.pyplot(fig)
    else:
        st.info("No skills detected yet.")

    # ---------- INTERVIEW PERFORMANCE ----------
    st.subheader("🎤 Interview Performance Trend")

    if scores:
        fig2, ax2 = plt.subplots()
        ax2.plot(range(1, len(scores)+1), scores, marker="o")
        ax2.set_xlabel("Question Number")
        ax2.set_ylabel("Score")
        ax2.set_ylim(0, 100)
        st.pyplot(fig2)
    else:
        st.warning("No interview scores available yet. Complete interview first.")

    # ---------- SUMMARY ----------
    st.subheader("📌 Summary Report")

    st.write("**Skills Found:**", skills if skills else "None")
    st.write("**Recommended Jobs:**", jobs if jobs else "None")
    st.write("**Total Interview Questions Answered:**", len(scores))

    if scores:
        avg_score = sum(scores) / len(scores)
        st.metric("Average Interview Score", f"{avg_score:.1f}/100")

        if avg_score >= 80:
            st.success("🌟 Excellent Performance")
        elif avg_score >= 60:
            st.info("👍 Good Performance")
        else:
            st.warning("⚠ Needs Improvement")

    st.markdown('</div>', unsafe_allow_html=True)
def generate_full_report():
    file = "career_report.pdf"
    c = canvas.Canvas(file, pagesize=A4)

    y = 800

    data = [
        "AI CAREER REPORT",
        "================",
        "",
        "SKILLS:",
        ", ".join(st.session_state.get("skills", [])),
        "",
        "JOBS:",
        ", ".join(st.session_state.get("jobs", [])),
        "",
        "ANSWERS:"
    ]

    for a in st.session_state.get("answers", []):
        data.append(str(a))

    for line in data:
        c.drawString(40, y, line[:100])
        y -= 20
        if y < 40:
            c.showPage()
            y = 800

    c.save()
    return file
if st.button("📄 Download Full Report"):
    pdf = generate_full_report()

    with open(pdf, "rb") as f:
        st.download_button("Download PDF", f, file_name="career_report.pdf")
