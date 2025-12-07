import streamlit as st
import re

# Initialize
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.info = {}
    st.session_state.tech_q = []
    st.session_state.current_q = 0

# Steps
steps = [
    ("name", "Full name?", lambda x: bool(re.match(r"^[a-zA-Z\s]+$", x))),
    ("email", "Email?", lambda x: "@" in x and "." in x),
    ("phone", "Phone?", lambda x: bool(re.match(r"^\d{10}$", re.sub(r'\D', '', x)))),
    ("exp", "Years experience?", lambda x: x.isdigit() and 0 < int(x) < 50),
    ("job", "Desired position?", lambda x: len(x) > 1),
    ("city", "Location?", lambda x: len(x) > 1),
    ("tech", "Tech stack?", lambda x: len(x) > 2)
]

# Chat
for msg in st.session_state.get("messages", []):
    role, content = msg["role"], msg["content"]
    st.chat_message(role).markdown(content)

# Ask question
if st.session_state.step < len(steps):
    key, question, validator = steps[st.session_state.step]
    
    if "messages" not in st.session_state or not st.session_state.messages:
        st.session_state.messages = [{"role": "assistant", "content": question}]
        st.rerun()

# Get answer
if answer := st.chat_input("Type here..."):
    # Exit check
    if answer.lower().strip() in ["exit", "quit", "bye"]:
        st.chat_message("assistant").markdown("👋 Screening ended!")
        st.stop()
    
    st.chat_message("user").markdown(answer)
    
    # Validate & store
    key, _, validator = steps[st.session_state.step]
    if validator(answer):
        st.session_state.info[key] = answer
        st.session_state.step += 1
        
        if st.session_state.step >= len(steps):
            # Generate tech questions
            techs = [t.strip() for t in answer.split(",") if t.strip()]
            st.session_state.tech_q = [f"Explain {tech}?" for tech in techs[:3]]
            msg = f"✅ Info saved! {len(st.session_state.tech_q)} tech questions next."
        else:
            next_q = steps[st.session_state.step][1]
            msg = f"✅ {next_q}"
    else:
        msg = f"❌ Invalid {key}. Try again."
    
    st.chat_message("assistant").markdown(msg)
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.rerun()

# Report
if st.session_state.info.get("tech") and st.sidebar.button("Show Report"):
    st.success("📋 Screening Report")
    st.write(st.session_state.info)
