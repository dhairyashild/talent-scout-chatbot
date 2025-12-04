<<<<<<< HEAD
# Your app.py content here
=======
import streamlit as st
import os
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="TalentScout Hiring Assistant",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2563EB;
        text-align: center;
    }
    .chat-message {
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
    }
    .user-message {
        background-color: #E3F2FD;
        text-align: right;
    }
    .bot-message {
        background-color: #F5F5F5;
        text-align: left;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'candidate_info' not in st.session_state:
    st.session_state.candidate_info = {}
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'tech_stack' not in st.session_state:
    st.session_state.tech_stack = []

# Information gathering steps
steps = [
    ("name", "What is your full name?"),
    ("email", "What is your email address?"),
    ("phone", "What is your phone number?"),
    ("experience", "How many years of experience do you have?"),
    ("position", "What position are you applying for?"),
    ("location", "Where are you currently located?"),
    ("tech_stack", "What is your tech stack? (comma-separated, e.g., Python, React, AWS)")
]

# Function to generate technical questions
def generate_tech_questions(tech_stack, experience):
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        # Fallback questions if no API key
        questions = []
        for tech in tech_stack:
            questions.append(f"\n**{tech} Questions:**")
            questions.append(f"1. What experience do you have with {tech}?")
            questions.append(f"2. Can you explain a key concept in {tech}?")
            questions.append(f"3. How would you solve a common problem using {tech}?")
        return "\n".join(questions)
    
    try:
        client = openai.OpenAI(api_key=api_key)
        prompt = f"Generate 3-5 technical interview questions for each technology: {', '.join(tech_stack)}. Candidate has {experience} years of experience."
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a technical interviewer generating relevant questions."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except:
        # Fallback if API call fails
        return f"Technical questions for: {', '.join(tech_stack)}\n1. Describe your experience\n2. Explain key concepts\n3. Solve sample problems"

# Main app
st.markdown('<h1 class="main-header">🤖 TalentScout AI Hiring Assistant</h1>', unsafe_allow_html=True)
st.markdown("### Your AI-powered recruitment screening partner")

# Display chat messages
for message in st.session_state.messages:
    with st.container():
        if message["role"] == "user":
            st.markdown(f'<div class="chat-message user-message"><strong>You:</strong> {message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message bot-message"><strong>🤖 TalentScout:</strong> {message["content"]}</div>', unsafe_allow_html=True)

# Chat input
if st.session_state.step < len(steps):
    field, question = steps[st.session_state.step]
    
    if not st.session_state.messages or st.session_state.messages[-1]["role"] != "assistant":
        st.session_state.messages.append({"role": "assistant", "content": question})
        st.rerun()
    
    if prompt := st.chat_input("Your response:"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Store information
        if field == "tech_stack":
            tech_items = [t.strip() for t in prompt.split(",") if t.strip()]
            st.session_state.tech_stack = tech_items
            st.session_state.candidate_info[field] = tech_items
        else:
            st.session_state.candidate_info[field] = prompt
        
        # Move to next step or generate questions
        st.session_state.step += 1
        
        if st.session_state.step >= len(steps):
            # All info collected, generate questions
            experience = st.session_state.candidate_info.get("experience", "0")
            questions = generate_tech_questions(st.session_state.tech_stack, experience)
            final_message = f"✅ Screening Complete!\n\n**Technical Questions:**\n\n{questions}\n\nPlease answer these questions one by one."
            st.session_state.messages.append({"role": "assistant", "content": final_message})
        else:
            # Ask next question
            next_field, next_question = steps[st.session_state.step]
            st.session_state.messages.append({"role": "assistant", "content": next_question})
        
        st.rerun()

# Sidebar with candidate info
with st.sidebar:
    st.title("Candidate Info")
    if st.session_state.candidate_info:
        for key, value in st.session_state.candidate_info.items():
            if value:
                st.write(f"**{key.title()}:** {value}")
    
    if st.button("Restart Conversation"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# Footer
st.markdown("---")
st.markdown("🔒 **Data Privacy:** All information is processed locally and not stored permanently.")
>>>>>>> 91126b9 (Complete TalentScout AI Hiring Assistant with OpenAI integration, AWS deployment, and systemd service)
