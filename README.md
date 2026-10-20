# CodeClarity Studio

A polished, learning-first coding companion: explain code in plain English, generate code from everyday-language requests, and execute snippets locally or through an online runner.

## Features

- Explain snippets in beginner, intermediate, or advanced language.
- Generate commented code for Python, R, JavaScript, TypeScript, Java, C, C++, C#, Go, SQL, HTML/CSS, and Bash.
- Offline AI option through a locally installed Ollama model.
- Local Python execution with a short timeout.
- Online execution through a Piston-compatible API for configured languages.
- Responsive Streamlit interface with clear privacy notes.

## Quick start

Requires Python 3.10 or newer.

### 1. Create an environment

**Windows PowerShell**
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### 2. Configure AI

Open `.env`.

- **OpenAI online:** set `OPENAI_API_KEY` to your own API key.
- **Ollama offline:** install Ollama, download a code model such as `qwen2.5-coder:7b`, and keep `OLLAMA_BASE_URL` and `OLLAMA_MODEL` aligned with your local setup.

The app's `Auto` mode uses OpenAI when an API key is configured; otherwise it tries Ollama.

### 3. Launch

```bash
streamlit run app.py
```

Streamlit will show a local URL, usually `http://localhost:8501`.

## Project structure

```text
codeclarity_studio/
├── app.py
├── services/
│   ├── __init__.py
│   ├── explainer.py
│   └── runner.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Execution and safety

- Local execution currently supports Python only.
- The local Python runner uses a child process and a timeout, but **this is not a secure sandbox**. Do not run untrusted code on a personal computer or expose this runner to the public internet.
- Online execution sends code to the configured third-party runner. Do not send secrets, credentials, private datasets, or proprietary code.
- Before public deployment, move execution into an isolated container/VM or a dedicated sandbox service with CPU, memory, filesystem, network, and wall-clock limits. Add authentication, rate limits, audit logging, and abuse prevention.
- Online runner availability, supported versions, and rate limits depend on the configured service.

## Suggested next steps

1. Add unit tests and sample lessons for each supported language.
2. Add a syntax-highlighted editor (for example, Monaco) and downloadable generated files.
3. Add saved workspaces and side-by-side code/explanation views.
4. Add safer isolated execution with per-run containers.
5. Add export to Markdown/PDF and multilingual explanations.
6. Add accessibility testing, error telemetry with consent, and deployment configuration.

## License

Choose a license before publishing this project (for example, MIT if that fits your intended use).
