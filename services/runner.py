import os
import subprocess
import sys
import tempfile
from pathlib import Path
import requests

LANGUAGE_MAP = {
    "Python": "python",
    "JavaScript": "javascript",
    "R": "r",
    "C++": "cpp",
    "Java": "java",
    "Go": "go",
    "SQL": "sqlite3",
}

def run_python_locally(code: str) -> str:
    """Run Python in a child process with a timeout. This is not a secure sandbox."""
    with tempfile.TemporaryDirectory(prefix="codeclarity_") as temp_dir:
        script = Path(temp_dir) / "snippet.py"
        script.write_text(code, encoding="utf-8")
        try:
            completed = subprocess.run(
                [sys.executable, "-I", str(script)],
                cwd=temp_dir,
                capture_output=True,
                text=True,
                timeout=5,
                env={"PATH": os.environ.get("PATH", ""), "PYTHONIOENCODING": "utf-8"}
            )
            output = completed.stdout
            if completed.stderr:
                output += ("\n" if output else "") + completed.stderr
            if completed.returncode != 0:
                output += f"\nProcess exited with code {completed.returncode}."
            return output or "(No output)"
        except subprocess.TimeoutExpired:
            return "Execution stopped: time limit of 5 seconds exceeded."
        except Exception as exc:
            return f"Could not run code: {exc}"

def run_online(code: str, language: str) -> str:
    """Use the Piston public API. For production, configure a trusted execution service."""
    runtime = LANGUAGE_MAP.get(language)
    if not runtime:
        return f"Online execution is not configured for {language}."
    endpoint = os.getenv("PISTON_API_URL", "https://emkc.org/api/v2/piston/execute")
    payload = {
        "language": runtime,
        "version": "*",
        "files": [{"name": "main", "content": code}],
        "stdin": "",
        "args": [],
        "compile_timeout": 10000,
        "run_timeout": 5000
    }
    try:
        response = requests.post(endpoint, json=payload, timeout=20)
        response.raise_for_status()
        data = response.json()
        run = data.get("run", {})
        compile_info = data.get("compile", {}) or {}
        output = ""
        if compile_info.get("output"):
            output += "Compile output:\n" + compile_info["output"] + "\n"
        if run.get("stdout"):
            output += run["stdout"]
        if run.get("stderr"):
            output += ("\n" if output else "") + run["stderr"]
        return output.strip() or f"Execution completed (code {run.get('code', 'unknown')}) with no output."
    except Exception as exc:
        return f"Online execution failed: {exc}\nCheck internet access or configure PISTON_API_URL."
