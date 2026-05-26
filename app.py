import streamlit as st
from ai import generate_replies, parse_replies
from tone import analyze_tone

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Unseen", page_icon="👻", layout="centered")

# ── Header ────────────────────────────────────────────────────────────────────
st.title("👻 Unseen")
st.caption("Paste a message you don't know how to reply to. Get 3 replies instantly.")
st.markdown("---")

# ── Inputs ────────────────────────────────────────────────────────────────────
message = st.text_area(
    "Message you received",
    placeholder='e.g.  "k."   or   "we need to talk"   or   "why didn\'t you come yesterday"',
    height=120,
)

col1, col2 = st.columns(2)
with col1:
    sender = st.selectbox(
        "Who sent it?",
        ["Friend", "Crush", "Parent", "Teacher", "Colleague", "Stranger", "Ex"],
    )
with col2:
    goal = st.selectbox(
        "What's your goal?",
        ["Keep the peace", "Be firm", "Play it cool", "Be funny", "Be honest", "End the conversation"],
    )

st.markdown("---")

# ── Generate ──────────────────────────────────────────────────────────────────
if st.button("✨ Generate Replies", type="primary", use_container_width=True):
    if not message.strip():
        st.warning("Paste a message first.")
    else:
        with st.spinner("Reading the vibes..."):
            tone = analyze_tone(message)
            raw = generate_replies(message, sender, goal, tone["label"])
            replies = parse_replies(raw)

        # Tone badge
        tone_colors = {"Positive": "🟢", "Negative": "🔴", "Neutral": "🟡"}
        icon = tone_colors.get(tone["label"], "⚪")
        st.caption(
            f"Detected tone: {icon} **{tone['label']}** "
            f"({round(tone['score'] * 100)}% confidence)"
        )

        st.markdown("### Your replies")

        # Reply cards
        for item in replies:
            with st.container(border=True):
                st.markdown(f"**{item['label']}**")
                st.write(item["reply"])
                st.code(item["reply"], language=None)

        st.markdown("---")
        st.caption("💡 Tip: the code block above each reply is easy to copy on mobile.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(
    "<br><center><sub>Set <code>GROQ_API_KEY</code> in your environment or a <code>.env</code> file to enable real replies.</sub></center>",
    unsafe_allow_html=True,
)
