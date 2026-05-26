import streamlit as st
from ai import generate_replies, parse_replies
from tone import analyze_tone

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Unseen", page_icon="👻", layout="centered")

# ── Session state init ────────────────────────────────────────────────────────
if "thread" not in st.session_state:
    st.session_state.thread = []  # list of {speaker, text}
if "replies" not in st.session_state:
    st.session_state.replies = []
if "tone" not in st.session_state:
    st.session_state.tone = None

# ── Header ────────────────────────────────────────────────────────────────────
st.title("👻 Unseen")
st.caption("Build the conversation, set your vibe, get 3 replies instantly.")
st.markdown("---")

# ── SECTION 1: Conversation Thread Builder ────────────────────────────────────
st.markdown("### 💬 Conversation Thread")
st.caption("Add messages in order. Label each as **Me** or **Them**.")

col_speaker, col_text, col_add = st.columns([1, 4, 1])
with col_speaker:
    speaker = st.selectbox("Who?", ["Them", "Me"], label_visibility="collapsed")
with col_text:
    new_msg = st.text_input("Message", placeholder="Type a message...", label_visibility="collapsed")
with col_add:
    if st.button("Add", use_container_width=True):
        if new_msg.strip():
            st.session_state.thread.append({"speaker": speaker.lower(), "text": new_msg.strip()})

# Display thread
if st.session_state.thread:
    for i, msg in enumerate(st.session_state.thread):
        col_msg, col_del = st.columns([10, 1])
        with col_msg:
            align = "**Me:**" if msg["speaker"] == "me" else "Them:"
            st.markdown(f"{align} {msg['text']}")
        with col_del:
            if st.button("✕", key=f"del_{i}"):
                st.session_state.thread.pop(i)
                st.rerun()

    if st.button("🗑 Clear thread", use_container_width=False):
        st.session_state.thread = []
        st.rerun()
else:
    st.info("No messages yet. Add the conversation above.")

st.markdown("---")

# ── SECTION 2: Context ────────────────────────────────────────────────────────
st.markdown("### 🎯 Context")

col1, col2, col3 = st.columns(3)
with col1:
    sender = st.selectbox(
        "Who sent it?",
        ["Friend", "Crush", "Parent", "Teacher", "Colleague", "Stranger", "Ex"],
    )
with col2:
    relationship = st.selectbox(
        "How close?",
        ["Acquaintance", "Casual friend", "Good friend", "Close friend", "Best friend"],
    )
with col3:
    goal = st.selectbox(
        "Your goal?",
        ["Keep the peace", "Be firm", "Play it cool", "Be funny", "Be honest", "End the conversation"],
    )

st.markdown("---")

# ── SECTION 3: Style Fingerprinting ──────────────────────────────────────────
st.markdown("### ✍️ Your Writing Style *(optional)*")
st.caption("Paste 2–3 of your past messages so replies sound like *you*.")

style_sample = st.text_area(
    "Style sample",
    placeholder='e.g.  "lmaooo ok but hear me out"  /  "yeah no that\'s fair tbh"  /  "bro what 💀"',
    height=80,
    label_visibility="collapsed",
)

col_casual, col_length = st.columns(2)
with col_casual:
    casual_formal = st.slider("Casual ←→ Formal", 1, 5, 2)
with col_length:
    short_long = st.slider("Short ←→ Long replies", 1, 5, 2)

st.markdown("---")

# ── SECTION 4: Generate ───────────────────────────────────────────────────────
if st.button("✨ Generate Replies", type="primary", use_container_width=True):
    if not st.session_state.thread:
        st.warning("Add at least one message to the thread first.")
    else:
        last_them = next(
            (m["text"] for m in reversed(st.session_state.thread) if m["speaker"] == "them"),
            " ".join(m["text"] for m in st.session_state.thread)
        )

        with st.spinner("Reading the vibes..."):
            tone = analyze_tone(last_them)
            raw = generate_replies(
                thread=st.session_state.thread,
                sender=sender,
                relationship=relationship,
                goal=goal,
                tone=tone["label"],
                style_sample=style_sample,
                casual_formal=casual_formal,
                short_long=short_long,
            )
            st.session_state.replies = parse_replies(raw)
            st.session_state.tone = tone

# ── Results ───────────────────────────────────────────────────────────────────
if st.session_state.replies:
    tone = st.session_state.tone
    tone_colors = {"Positive": "🟢", "Negative": "🔴", "Neutral": "🟡"}
    icon = tone_colors.get(tone["label"], "⚪")
    st.caption(
        f"Detected tone: {icon} **{tone['label']}** "
        f"({round(tone['score'] * 100)}% confidence)"
    )

    st.markdown("### Your replies")

    for item in st.session_state.replies:
        with st.container(border=True):
            st.markdown(f"**{item['label']}**")
            st.code(item["reply"], language=None)

    st.markdown("---")
    st.caption("💡 Click the copy icon on any reply block to copy it.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(
    "<br><center><sub>Set <code>GROQ_API_KEY</code> in your <code>.env</code> file to enable real replies.</sub></center>",
    unsafe_allow_html=True,
)
