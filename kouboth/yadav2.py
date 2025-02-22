import streamlit as st
import google.generativeai as genai
import base64

# Configure Gemini API Key
genai.configure(api_key="AIzaSyBEWOC1UVl5nv5YfHbdEYztXn0UW_VM-4w")  # Replace with your actual API key

# Streamlit Page Config
st.set_page_config(page_title="Mental Health Chatbot", layout="wide")

# Background Image Function
def get_base64(background):
    with open(background, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

bin_str = get_base64("E:/pythoncode/calmconnect/background.png")

# Custom CSS for the page
st.markdown(f"""
    <style>
        .main {{
            background-image: url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            height: 100vh;
            padding: 20px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}
        .chat-container {{
            flex-grow: 1;
            overflow-y: auto;
            margin-bottom: 20px;
        }}
        .search-panel {{
            display: flex;
            align-items: center;
            gap: 10px;
            background: rgba(255, 255, 255, 0.9);
            padding: 10px;
            border-radius: 10px;
            box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
            position: sticky;
            bottom: 0;
        }}
        .search-input {{
            flex-grow: 1;
            font-size: 16px;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #ccc;
        }}
        .search-button {{
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 5px;
        }}
        .search-button:hover {{
            background-color: #45a049;
        }}
        .action-buttons {{
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }}
        .action-buttons button {{
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            flex: 1;
        }}
        .action-buttons button:hover {{
            background-color: #45a049;
        }}
        .message {{
            margin-bottom: 10px;
            padding: 10px;
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.9);
            box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
        }}
        .message.user {{
            background: rgba(240, 240, 240, 0.9);
        }}
        .message.assistant {{
            background: rgba(220, 240, 255, 0.9);
        }}
    </style>
""", unsafe_allow_html=True)

# Initialize Chat History
if 'conversation_history' not in st.session_state:
    st.session_state['conversation_history'] = []

# Generate Response from Gemini
def generate_response(user_input):
    st.session_state['conversation_history'].append({"role": "user", "content": user_input})
    model = genai.GenerativeModel("gemini-pro")  
    response = model.generate_content(user_input)  
    ai_response = response.text
    st.session_state['conversation_history'].append({"role": "assistant", "content": ai_response})
    return ai_response

# Generate Positive Affirmations
def generate_affirmation():
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content("Provide a positive affirmation for someone feeling stressed.")
    return response.text

# Generate Meditation Guide
def generate_meditation_guide():
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content("Provide a 5-minute guided meditation script to help someone relax.")
    return response.text

# Callback to clear the input box
def clear_input():
    st.session_state["user_message"] = ""

# Streamlit UI
st.title("Mental Health Support Agent")

# Display Chat History
chat_container = st.container()
with chat_container:
    for msg in st.session_state['conversation_history']:
        role = msg['role']
        content = msg['content']
        st.markdown(f"""
            <div class="message {'user' if role == 'user' else 'assistant'}">
                <strong>{'You' if role == 'user' else 'AI'}:</strong> {content}
            </div>
        """, unsafe_allow_html=True)

# Search Panel (Input and Enter Button)
st.markdown('<div class="search-panel">', unsafe_allow_html=True)
user_message = st.text_input("How can I help you today?", key="user_message", label_visibility="collapsed", on_change=lambda: st.session_state.update({"user_message_submitted": True}))
if st.button("🚀 Enter", key="enter_button", on_click=clear_input):
    st.session_state["user_message_submitted"] = True
st.markdown('</div>', unsafe_allow_html=True)

# Handle User Input
if st.session_state.get("user_message_submitted", False):
    if user_message:
        with st.spinner("Thinking..."):
            ai_response = generate_response(user_message)
            st.session_state["user_message_submitted"] = False
            st.rerun()  # Refresh the page to display the new message

# Action Buttons (Positive Affirmation and Guided Meditation)
st.markdown('<div class="action-buttons">', unsafe_allow_html=True)
if st.button("💖 Positive Affirmation"):
    affirmation = generate_affirmation()
    st.session_state['conversation_history'].append({"role": "assistant", "content": f"**Affirmation:** {affirmation}"})
    st.rerun()

if st.button("🧘‍♂️ Guided Meditation"):
    meditation_guide = generate_meditation_guide()
    st.session_state['conversation_history'].append({"role": "assistant", "content": f"**Guided Meditation:** {meditation_guide}"})
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)