import os
import requests

def _openai_response(prompt: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return "### AI provider is not configured\nSet `OPENAI_API_KEY` in your `.env` file, or select Ollama and configure a local model. The UI and execution features can still be explored without AI."
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
            input=prompt
        )
        return response.output_text
    except Exception as exc:
        return f"**AI request failed:** {exc}\n\nCheck your API key, model name, internet connection, and account access."

def _ollama_response(prompt: str) -> str:
    base = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
    model = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:7b")
    try:
        response = requests.post(
            f"{base}/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=180
        )
        response.raise_for_status()
        return response.json().get("response", "No response returned by Ollama.")
    except Exception as exc:
        return f"**Ollama is unavailable:** {exc}\n\nStart Ollama locally and pull the model configured in `.env`."

def _ask(prompt: str, provider: str) -> str:
    if provider == "OpenAI":
        return _openai_response(prompt)
    if provider == "Ollama":
        return _ollama_response(prompt)
    if os.getenv("OPENAI_API_KEY", "").strip():
        return _openai_response(prompt)
    return _ollama_response(prompt)

def explain_code(code: str, language: str, level: str, provider: str) -> str:
    prompt = f"""You are CodeClarity Studio, a careful programming tutor.
Explain the following {language} code for a {level.lower()} learner.
Use this structure:
1. **Purpose in one sentence**
2. **How it works**, in small ordered steps
3. **Important syntax and variables**
4. **Inputs and outputs**
5. **Potential errors or assumptions** (only if relevant)
6. **A tiny example** when it helps.
Be accurate. Do not invent execution results. Preserve the original code's meaning and flag uncertainty.
Code:
```{language.lower()}
{code}
```"""
    return _ask(prompt, provider)

def generate_code(task: str, language: str, requirements: str, provider: str) -> str:
    prompt = f"""You are CodeClarity Studio, a senior developer and patient tutor.
Convert this task into working, readable {language} code.
Task: {task}
Additional requirements: {requirements or "None specified"}
Return:
1. A brief approach
2. A single complete code block with useful comments
3. How to run it
4. A short explanation of the main parts
5. Any assumptions or limitations.
Prefer simple, maintainable code. Do not claim the code was tested unless it actually was."""
    return _ask(prompt, provider)
