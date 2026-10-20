import streamlit as st
from dotenv import load_dotenv
from services.explainer import explain_code, generate_code
from services.runner import run_python_locally, run_online

load_dotenv()
st.set_page_config(page_title="CodeClarity Studio", page_icon="✦", layout="wide")

st.markdown("""
<style>
:root { --ink:#172033; --muted:#64748b; --line:#e7ebf2; --accent:#5b5ce2; }
.block-container {padding-top: 1.5rem; max-width: 1440px;}
.hero {padding: 1.5rem 1.7rem; border: 1px solid var(--line); border-radius: 22px;
background: linear-gradient(120deg, rgba(91,92,226,.10), rgba(15,183,166,.07));}
.hero h1 {letter-spacing:-.04em; margin:0; font-size:2.2rem;}
.hero p {color:var(--muted); margin:.45rem 0 0 0;}
div[data-testid="stTabs"] button {font-weight:600;}
.small-note {color:var(--muted); font-size:.9rem;}
</style>
<div class="hero">
  <h1>✦ CodeClarity Studio</h1>
  <p>Understand code. Turn ideas into code. Run experiments with clear, practical feedback.</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## Workspace")
    st.caption("A learning-first coding companion")
    mode = st.radio("Execution mode", ["Offline · local Python", "Online · Piston runner"], index=0)
    st.divider()
    st.markdown("### AI provider")
    st.caption("Online AI uses an OpenAI API key. Offline AI can use a local Ollama model.")
    provider = st.selectbox("Provider", ["Auto", "OpenAI", "Ollama"])
    st.caption("Configure keys and models in `.env`.")
    st.divider()
    st.markdown("**Privacy note**")
    st.caption("Code sent to online AI or an online runner leaves your computer. Do not submit secrets or private code.")

tab_explain, tab_generate, tab_run, tab_about = st.tabs(
    ["🧠 Explain code", "✨ English → code", "▶ Run code", "ⓘ About"]
)

LANGUAGES = ["Python", "R", "JavaScript", "TypeScript", "Java", "C", "C++", "C#", "Go", "SQL", "HTML/CSS", "Bash"]

with tab_explain:
    st.subheader("Turn unfamiliar code into plain English")
    st.write("Paste a snippet, choose its language, and get a structured explanation with the purpose, line-by-line meaning, and important caveats.")
    c1, c2 = st.columns([3, 1])
    with c1:
        explain_lang = st.selectbox("Code language", LANGUAGES, key="explain_lang")
    with c2:
        level = st.selectbox("Explanation level", ["Beginner", "Intermediate", "Advanced"], index=0)
    code_input = st.text_area("Paste code", height=260, placeholder="Paste a function, script, query, or code snippet here…", key="code_input")
    explain_col, clear_col = st.columns([1, 5])
    with explain_col:
        explain_clicked = st.button("Explain code", type="primary", use_container_width=True)
    with clear_col:
        st.caption("Tip: include the error message and expected result if you want debugging help.")
    if explain_clicked:
        if not code_input.strip():
            st.warning("Paste some code first.")
        else:
            with st.spinner("Reading your code…"):
                result = explain_code(code_input, explain_lang, level, provider)
            st.markdown(result)

with tab_generate:
    st.subheader("Describe the task in everyday English")
    st.write("Choose a target language and ask for readable, commented code—not just a code dump.")
    target_lang = st.selectbox("Generate code in", LANGUAGES, key="target_lang")
    task = st.text_area("What should the code do?", height=180, placeholder="Example: Read a CSV of survey responses, calculate the weighted mean by region, and explain each step.")
    requirements = st.text_input("Optional requirements", placeholder="e.g. use pandas, include validation, beginner-friendly comments")
    if st.button("Generate code", type="primary"):
        if not task.strip():
            st.warning("Describe what you want the code to do.")
        else:
            with st.spinner("Designing a solution…"):
                result = generate_code(task, target_lang, requirements, provider)
            st.markdown(result)

with tab_run:
    st.subheader("Run a code snippet")
    st.warning("Only run code you trust. A local subprocess is not a complete security sandbox. Online execution sends code to a third-party runner.")
    run_lang = st.selectbox("Language to run", ["Python", "JavaScript", "R", "C++", "Java", "Go", "SQL"], key="run_lang")
    run_code = st.text_area("Code to execute", height=240, placeholder="print('Hello, world!')", key="run_code")
    run_mode = st.radio("Where to run", ["Offline on this computer", "Online runner"], horizontal=True,
                        index=0 if mode.startswith("Offline") else 1)
    if st.button("Run code", type="primary"):
        if not run_code.strip():
            st.warning("Enter code first.")
        elif run_mode.startswith("Offline"):
            if run_lang != "Python":
                st.info("The starter project supports offline execution for Python only. Use the online runner for other supported languages.")
            else:
                with st.spinner("Running locally…"):
                    result = run_python_locally(run_code)
                st.markdown("**Result**")
                st.code(result, language="text")
        else:
            with st.spinner("Submitting to online runner…"):
                result = run_online(run_code, run_lang)
            st.markdown("**Result**")
            st.code(result, language="text")

with tab_about:
    st.subheader("Built for understanding, not just producing code")
    st.markdown("""
    - **Explain:** plain-English purpose, line-by-line breakdown, inputs/outputs, assumptions, and likely errors.
    - **Generate:** convert a task description into readable, commented code in the selected language.
    - **Execute:** run Python locally, or use the configurable online runner for supported languages.
    - **Offline AI:** optionally connect Ollama running on your computer.
    - **Extensible:** add more language runtimes, tests, saved projects, and user accounts as needed.
    """)
    st.info("This is a starter project. For public deployment, isolate execution in a hardened container or dedicated sandbox service before allowing untrusted users to run code.")
