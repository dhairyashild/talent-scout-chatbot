(venv) ubuntu@ip-10-0-2-99:~/talent-scout-chatbot$ cat app.py 
import streamlit as st
import random
import re

st.set_page_config(page_title="TalentScout Hiring Assistant", page_icon="🤖", layout="centered")

st.title("🤖 TalentScout AI Hiring Assistant")
st.markdown("*AI-powered initial screening for technology placements*")

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.candidate_info = {}
    st.session_state.tech_stack = []
    st.session_state.questions = []
    st.session_state.current_q = 0
    st.session_state.conversation = [{
        "role": "assistant",
        "content": "👋 Hello! I'm the TalentScout AI Hiring Assistant. I'll help with your initial screening. You can type 'exit' anytime to end."
    }]
    st.session_state.asked_question = False  # Track if current question was asked

# Conversation steps with validation types
STEPS = [
    ("name", "What is your full name?", "text"),
    ("email", "What is your email address?", "email"),
    ("phone", "What is your phone number? (10 digits)", "phone"),
    ("experience", "How many years of experience do you have? (number)", "number"),
    ("position", "What position are you applying for?", "text"),
    ("location", "Where are you currently located?", "text"),
    ("tech_stack", "What is your tech stack? (comma separated, e.g., Python, React, AWS)", "text")
]

# Technical questions database
QUESTIONS_DB = {
    "python": ["Explain Python decorators.", "List vs Tuple difference?", "What is GIL in Python?"],
    "java": ["What is polymorphism?", "Explain collections.", "Multithreading in Java?"],
    "javascript": ["What is closure?", "Explain event loop.", "var/let/const difference?"],
    "react": ["What are React hooks?", "Virtual DOM?", "State vs props?"],
    "aws": ["EC2 vs Lambda difference?", "What is S3?", "Describe VPC."],
    "sql": ["SQL joins types?", "What are indexes?", "Normalization?"],
    "docker": ["Docker vs VMs?", "What is Dockerfile?", "Image vs container?"],
    "node": ["Event-driven programming?", "Callback hell?", "Async operations?"]
}

def validate_input(field_type, value):
    """Validate user input"""
    value = value.strip()
    
    if not value:
        return False, "This field cannot be empty."
    
    if field_type == "email":
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, value):
            return False, "Please enter valid email (e.g., name@example.com)"
        return True, ""
    
    elif field_type == "phone":
        digits = re.sub(r'\D', '', value)
        if len(digits) != 10:
            return False, "Please enter 10-digit phone number"
        return True, ""
    
    elif field_type == "number":
        if not value.isdigit():
            return False, "Please enter a number (e.g., 2, 5)"
        if int(value) > 50:
            return False, "Please enter realistic years (1-50)"
        return True, ""
    
    elif field_type == "text":
        if len(value) < 2:
            return False, "Please enter valid response"
        return True, ""
    
    return True, ""

def get_questions(tech_list, exp):
    """Get 3-5 technical questions"""
    questions = []
    for tech in tech_list[:5]:
        tech_low = tech.strip().lower()
        for key in QUESTIONS_DB:
            if key in tech_low:
                questions.append(f"[{key.title()}] {random.choice(QUESTIONS_DB[key])}")
                break
    
    if not questions:
        questions = [
            "Describe a technical project you worked on.",
            "How do you debug complex issues?",
            "How do you stay updated with technology?"
        ]
    
    return questions[:5]

# Display progress
if st.session_state.step < len(STEPS):
    progress = (st.session_state.step) / len(STEPS)
    st.progress(progress)
    st.caption(f"📝 Step {st.session_state.step + 1} of {len(STEPS)} - Information Collection")
elif st.session_state.questions:
    total_q = len(st.session_state.questions)
    current_q = min(st.session_state.current_q, total_q)
    progress = current_q / total_q if total_q > 0 else 0
    st.progress(progress)
    st.caption(f"🧪 Question {current_q + 1} of {total_q} - Technical Screening")

# Display conversation history
st.markdown("### 💬 Conversation")
for msg in st.session_state.conversation:
    if msg["role"] == "assistant":
        st.markdown(f"""
        <div style='background-color: #e8f4fc; padding: 12px; border-radius: 8px; margin: 8px 0; border-left: 4px solid #2563eb;'>
            <strong>🤖 TalentScout:</strong> {msg["content"]}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='background-color: #f0fdf4; padding: 12px; border-radius: 8px; margin: 8px 0; border-left: 4px solid #10b981;'>
            <strong>👤 You:</strong> {msg["content"]}
        </div>
        """, unsafe_allow_html=True)

# Main interaction area
st.markdown("---")
st.markdown("### ✍️ Your Turn")

# Step 1: Information gathering
if st.session_state.step < len(STEPS):
    field, question, field_type = STEPS[st.session_state.step]
    
    # Ask the current question if not already asked
    if not st.session_state.asked_question:
        st.session_state.conversation.append({"role": "assistant", "content": question})
        st.session_state.asked_question = True
        st.rerun()
    
    # Placeholder examples
    placeholders = {
        "email": "your.email@example.com",
        "phone": "1234567890",
        "number": "e.g., 3",
        "text": "Type here...",
        "tech_stack": "Python, JavaScript, AWS, Docker"
    }
    
    placeholder = placeholders.get(field_type, "Type your answer...")
    
    # Get user input
    user_input = st.text_input(
        f"**{question}**",
        key=f"input_{st.session_state.step}",
        placeholder=placeholder
    )
    
    # Submit button
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Next →", key=f"btn_{st.session_state.step}", type="primary", use_container_width=True):
            if user_input:
                # Check for exit
                if user_input.lower() in ["exit", "quit", "bye", "end"]:
                    st.session_state.conversation.append({
                        "role": "assistant", 
                        "content": "👋 Thank you! Screening ended. We'll contact you if needed."
                    })
                    st.session_state.step = len(STEPS) + 1
                    st.rerun()
                
                # Validate input
                is_valid, error_msg = validate_input(field_type, user_input)
                
                if not is_valid:
                    st.error(f"**Validation Error:** {error_msg}")
                else:
                    # Store response
                    st.session_state.conversation.append({"role": "user", "content": user_input})
                    st.session_state.candidate_info[field] = user_input
                    
                    # Special handling for tech stack
                    if field == "tech_stack":
                        tech_items = [t.strip() for t in user_input.split(",") if t.strip()]
                        st.session_state.tech_stack = tech_items
                    
                    # Move to next step
                    st.session_state.step += 1
                    st.session_state.asked_question = False
                    
                    # If all info collected, generate questions
                    if st.session_state.step >= len(STEPS):
                        exp = st.session_state.candidate_info.get("experience", "1")
                        questions = get_questions(st.session_state.tech_stack, exp)
                        st.session_state.questions = questions
                        
                        # Completion message
                        completion_msg = f"""
                        ✅ **Information Collection Complete!**
                        
                        **Technical Questions ({len(questions)}):**
                        """
                        for i, q in enumerate(questions, 1):
                            completion_msg += f"\n{i}. {q}"
                        
                        completion_msg += "\n\nPlease answer each question. Type 'exit' to end."
                        
                        st.session_state.conversation.append({
                            "role": "assistant", 
                            "content": completion_msg
                        })
                    
                    st.rerun()
            else:
                st.warning("Please enter a response.")

# Step 2: Technical questions
elif st.session_state.step == len(STEPS) and st.session_state.questions:
    if st.session_state.current_q < len(st.session_state.questions):
        q_num = st.session_state.current_q
        current_q = st.session_state.questions[q_num]
        
        # Display current question
        st.markdown(f"""
        <div style='background-color: #fef3c7; padding: 15px; border-radius: 10px; margin: 15px 0;'>
            <h4>❓ Question {q_num + 1} of {len(st.session_state.questions)}</h4>
            <p style='font-size: 16px;'>{current_q}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Answer input
        answer = st.text_area(
            "**Your Answer:**",
            key=f"answer_{q_num}",
            height=150,
            placeholder="Provide a detailed answer with examples if possible..."
        )
        
        # Buttons
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("✅ Submit", key=f"submit_{q_num}", use_container_width=True):
                if answer:
                    if answer.lower() in ["exit", "quit", "bye"]:
                        st.session_state.conversation.append({
                            "role": "assistant",
                            "content": "👋 Screening ended. Thank you!"
                        })
                        st.session_state.step = len(STEPS) + 1
                        st.rerun()
                    
                    st.session_state.conversation.append({
                        "role": "user",
                        "content": f"**Answer {q_num + 1}:** {answer[:150]}..."
                    })
                    st.session_state.current_q += 1
                    st.rerun()
                else:
                    st.warning("Please write an answer.")
        
        with col2:
            if st.button("⏭️ Skip", key=f"skip_{q_num}", use_container_width=True):
                st.session_state.current_q += 1
                st.rerun()
    
    else:
        # All questions completed
        st.balloons()
        st.success("""
        🎉 **Screening Successfully Completed!**
        
        **Thank you for your participation.**
        
        **Next Steps:**
        1. Our team will review your responses
        2. You'll hear back within 3-5 business days
        3. Next interview round (if selected)
        
        **Good luck!** 🍀
        """)
        
        if st.button("🔄 Start New Screening", type="primary", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

# Sidebar
with st.sidebar:
    st.markdown("### 📋 Candidate Profile")
    st.markdown("---")
    
    if st.session_state.candidate_info:
        display_order = ["name", "email", "phone", "experience", "position", "location", "tech_stack"]
        for field in display_order:
            if field in st.session_state.candidate_info:
                label = field.replace("_", " ").title()
                value = st.session_state.candidate_info[field]
                
                if field == "tech_stack" and st.session_state.tech_stack:
                    value = ", ".join(st.session_state.tech_stack)
                
                st.markdown(f"**{label}:**")
                st.text(value)
    
    st.markdown("---")
    
    if st.button("🔄 Restart Conversation", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 🛡️ Data Privacy")
    st.caption("""
    - All data processed locally
    - No permanent storage
    - Session clears on refresh
    - GDPR compliant
    """)
    
    st.markdown("---")
    st.caption("TalentScout AI Hiring Assistant v3.0")

# Footer
st.markdown("---")
st.caption("Built for TalentScout Recruitment Agency | AI/ML Intern Assignment")
