# tools/system_tools.py
import os
import subprocess
import webbrowser

def open_file_manager():
    """Open the OS file manager in the current directory."""
    try:
        if os.name == "nt":
            subprocess.Popen("explorer", shell=True)
        elif os.name == "posix":
            # Try xdg-open (Linux) or open (macOS)
            if subprocess.call(["which", "xdg-open"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
                subprocess.Popen(["xdg-open", "."])
            else:
                subprocess.Popen(["open", "."])
        return "📂 File manager opened (on local machine)."
    except Exception as e:
        return f"❌ Could not open file manager: {e}"

def open_chrome():
    """Open Google Chrome (if available on PATH)."""
    try:
        if os.name == "nt":
            subprocess.Popen("start chrome", shell=True)
        else:
            subprocess.Popen(["google-chrome"])
        return "🌐 Chrome opened."
    except Exception as e:
        return f"❌ Could not open Chrome: {e}"

def open_edge():
    """Open Microsoft Edge (if available)."""
    try:
        if os.name == "nt":
            subprocess.Popen("start msedge", shell=True)
        else:
            subprocess.Popen(["microsoft-edge"])
        return "🌐 Edge opened."
    except Exception as e:
        return f"❌ Could not open Edge: {e}"

def open_vscode():
    """Open Visual Studio Code (must be on PATH as 'code')."""
    try:
        subprocess.Popen("code", shell=True)
        return "💻 VS Code opened."
    except Exception as e:
        return f"❌ Could not open VS Code: {e}"

def open_youtube():
    """Open YouTube in the default browser."""
    try:
        webbrowser.open("https://www.youtube.com")
        return "▶️ YouTube opened in your browser."
    except Exception as e:
        return f"❌ Could not open YouTube: {e}"

def open_whatsapp():
    """Open WhatsApp Web in the default browser."""
    try:
        webbrowser.open("https://web.whatsapp.com")
        return "💬 WhatsApp Web opened."
    except Exception as e:
        return f"❌ Could not open WhatsApp: {e}"

def list_files():
    """List files in current working directory."""
    try:
        files = os.listdir(".")
        if not files:
            return "📂 No files found in this directory."
        return "📂 Files:\n" + "\n".join(files)
    except Exception as e:
        return f"❌ Could not list files: {e}"
