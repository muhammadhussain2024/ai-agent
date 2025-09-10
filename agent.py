# agent.py
import traceback

# Try to import system tools (optional)
try:
    from tools import system_tools
except Exception:
    system_tools = None

def ai_agent(prompt: str, api_key: str = None) -> str:
    """
    Simple, robust agent runner:
    - If no api_key: demo mode (deterministic responses + use available system_tools).
    - If api_key: attempts to call OpenRouter via openai.OpenAI.
    Returns a text response (never raw Python trace by default; but on error returns helpful debug text).
    """
    prompt = (prompt or "").strip()
    if not prompt:
        return "Please enter a command or question."

    # Demo mode
    if not api_key:
        lower = prompt.lower()
        # basic intent handling
        if "open" in lower and ("file" in lower or "folder" in lower or "manager" in lower):
            if system_tools:
                return system_tools.open_file_manager()
            return "(DEMO) Would open File Manager (running locally)."
        if "open" in lower and "chrome" in lower:
            if system_tools:
                return system_tools.open_chrome()
            return "(DEMO) Would open Chrome (running locally)."
        if "open" in lower and "edge" in lower:
            if system_tools:
                return system_tools.open_edge()
            return "(DEMO) Would open Edge (running locally)."
        if "vscode" in lower or "visual studio" in lower:
            if system_tools:
                return system_tools.open_vscode()
            return "(DEMO) Would open VS Code (running locally)."
        if "youtube" in lower:
            if system_tools:
                return system_tools.open_youtube()
            return "(DEMO) Would open YouTube in the browser."
        if "whatsapp" in lower:
            if system_tools:
                return system_tools.open_whatsapp()
            return "(DEMO) Would open WhatsApp Web in the browser."
        if "list files" in lower or ("list" in lower and "files" in lower):
            if system_tools:
                return system_tools.list_files()
            return "(DEMO) File listing: file1.txt, file2.txt"
        # fallback demo reply
        return "(DEMO) I'm running without an LLM key. Provide an OpenRouter API key in the sidebar to enable live AI."

    # LIVE mode: attempt to use OpenRouter via openai.OpenAI
    try:
        from openai import OpenAI
    except Exception as e:
        return f"❌ The Python package 'openai' is not installed. Install with: pip install openai\n\n{e}"

    try:
        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
        messages = [
            {"role": "system", "content": "You are an AI agent. If a user asks you to call a tool, respond exactly with: TOOL:<tool_name> (no extra text). Tools available: open_file_manager, open_chrome, open_edge, open_vscode, open_youtube, open_whatsapp, list_files."},
            {"role": "user", "content": prompt}
        ]
        resp = client.chat.completions.create(model="meta-llama/llama-3-8b-instruct", messages=messages, temperature=0.2, max_tokens=600)
        content = resp.choices[0].message.content.strip()

        # If model indicates a tool
        if content.upper().startswith("TOOL:"):
            tool_request = content.split(":", 1)[1].strip()
            # normalize
            tool_name = tool_request.lower()
            # mapping / whitelist
            mapping = {
                "open_file_manager": "open_file_manager",
                "open_filemanager": "open_file_manager",
                "open file manager": "open_file_manager",
                "open_chrome": "open_chrome",
                "open chrome": "open_chrome",
                "open_edge": "open_edge",
                "open edge": "open_edge",
                "open_vscode": "open_vscode",
                "open vscode": "open_vscode",
                "open_youtube": "open_youtube",
                "open youtube": "open_youtube",
                "open_whatsapp": "open_whatsapp",
                "open whatsapp": "open_whatsapp",
                "list_files": "list_files",
                "list files": "list_files",
            }
            mapped = mapping.get(tool_name, None)
            if mapped and system_tools and hasattr(system_tools, mapped):
                try:
                    return getattr(system_tools, mapped)()
                except Exception as e:
                    return f"❌ The tool '{mapped}' raised an error when executed:\n{e}"
            else:
                return f"⚠️ Model asked for tool '{tool_request}' but it's not available on this host."

        # Otherwise return AI text
        return content

    except Exception as e:
        # Return helpful traceback so you can debug in the UI
        return "❌ API call failed. Full error:\n\n" + traceback.format_exc()
