# app.py
import streamlit as st
import streamlit.components.v1 as components
import html as html_lib
from agent import ai_agent
import traceback

st.set_page_config(page_title="AI Agent", page_icon="🤖", layout="wide")

# ----------------- Sidebar -----------------
st.sidebar.title("⚙️ Settings")
st.sidebar.text_input(
    "🔑 Enter your OpenRouter API Key",
    key="api_key",
    type="password",
    placeholder="Paste your key here (sk-or-v1-...)"
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "📢 **Notice:**\n\n"
    "- If you run this app **locally on your PC**, the agent can run certain whitelisted system commands (open Chrome, YouTube, File Manager, VS Code).\n\n"
    "- If you run this app on **Streamlit Cloud** or other hosted environments, the agent **cannot control your computer**. It will only show the command or response.\n\n"
    "- **Do not hardcode** your API key into source code if you plan to share or publish this app."
)

# ----------------- Session state init -----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # list of {"role":"user"|"agent","content":...}

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# Helper: sanitize text
def _escape(text: str) -> str:
    return html_lib.escape(text)

# Send message handler
def send_message():
    text = st.session_state.get("input_text", "").strip()
    if not text:
        return

    # append user message
    st.session_state.chat_history.append({"role": "user", "content": text})
    st.session_state.input_text = ""  # clear input

    # call agent and append reply
    api_key = st.session_state.get("api_key", None)
    with st.spinner("🤖 Agent is thinking..."):
        try:
            reply = ai_agent(text, api_key)
        except Exception:
            reply = "❌ Internal error when calling agent:\n\n" + traceback.format_exc()

    st.session_state.chat_history.append({"role": "agent", "content": reply})

# ----------------- Page header -----------------
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<h1 style='font-size:38px;'>🤖 AI Agent with Tools</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='font-size:20px; color:#444;'>Ask me to do things like open Chrome, YouTube, File Manager, or VS Code</h3>", unsafe_allow_html=True)
st.markdown("---")

# ----------------- Input area -----------------
st.text_input(
    "💬 Your command or question:",
    key="input_text",
    on_change=send_message,
    placeholder="Type and press Enter (or click Send)..."
)

col1, col2 = st.columns([1, 6])
with col1:
    if st.button("Send"):
        send_message()
with col2:
    if st.button("Clear chat"):
        st.session_state.chat_history = []
        st.success("Chat cleared.")

st.markdown("")  # spacing

# ----------------- Build chat HTML -----------------
# We'll render inside an iframe with a fixed height and allow internal scrolling.
# This prevents the page from cutting off and ensures a consistent scroll area.
chat_html = """
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { font-family: Arial, Helvetica, sans-serif; margin:0; padding:0; }
  #chat-container {
      box-sizing: border-box;
      padding: 12px;
      height: 100%;
      overflow-y: auto;
  }
  .bubble-user {
      display:flex; justify-content:flex-end; margin-bottom:12px;
  }
  .bubble-user .bubble {
      background-color:#1E90FF; color:white; padding:20px 26px; border-radius:16px;
      max-width:90%; font-size:20px; line-height:1.4;
  }
  .bubble-agent {
      display:flex; justify-content:flex-start; margin-bottom:12px;
  }
  .bubble-agent .bubble {
      background-color:#228B22; color:white; padding:20px 26px; border-radius:16px;
      max-width:90%; font-size:20px; line-height:1.4;
  }
  .label { font-weight:700; margin-bottom:6px; }
  .label-agent { color:#90EE90; }
  .content { white-space: pre-wrap; }
</style>
</head>
<body>
<div id="chat-container">
"""

# append messages
for msg in st.session_state.chat_history:
    role = msg.get("role")
    content = _escape(msg.get("content", ""))
    if role == "user":
        chat_html += f"""
        <div class="bubble-user">
          <div class="bubble">
            <div class="label">You</div>
            <div class="content">{content}</div>
          </div>
        </div>
        """
    else:
        chat_html += f"""
        <div class="bubble-agent">
          <div class="bubble">
            <div class="label label-agent">🤖 Agent</div>
            <div class="content">{content}</div>
          </div>
        </div>
        """

chat_html += """
</div>
<script>
  // auto-scroll to bottom on load
  const chat = document.getElementById('chat-container');
  if (chat) { chat.scrollTop = chat.scrollHeight; }
</script>
</body>
</html>
"""

# ----------------- Render HTML in an iframe with scrolling enabled -----------------
# Use a reasonably tall iframe so there's space to see content and the iframe itself will be scrollable.
components.html(chat_html, height=650, scrolling=True)
