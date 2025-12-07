# TalentScout AI Hiring Assistant

AI chatbot for initial candidate screening with Hugging Face LLM integration.

## Setup
1. `pip install -r requirements.txt`
2. Get Hugging Face token from https://huggingface.co/settings/tokens
3. Create `.streamlit/secrets.toml` with your token
4. `streamlit run app.py`

## Features
- Collects candidate information
- Generates technical questions using Hugging Face LLM
- Shows questions one by one
- Stores answers
- Professional UI with sidebar

## Files
- `app.py` - Main application
- `requirements.txt` - Dependencies
- `.streamlit/secrets.toml` - API key (create this)
