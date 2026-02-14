import streamlit as st
from streamlit_gsheets import GSheetsConnection

# --- 1. UI TEMPLATES (Exactly as you provided) ---
def load_synapse_ui():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');
    
    :root {
      --bg: #e0e5ec;
      --text: #4a4a4a;
      --primary: #4C51BF;
      --shadow-light: #ffffff;
      --shadow-dark: #a3b1c6;
      --accent: #d97706;
      --correct: #38A169;
    }

    .stApp { background: var(--bg); color: var(--text); font-family: 'Nunito', sans-serif; }
    
    .neu-card {
        background: var(--bg);
        box-shadow: 7px 7px 14px var(--shadow-dark), -7px -7px 14px var(--shadow-light);
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 25px;
        border: none;
    }

    .badge {
        padding: 5px 12px;
        border-radius: 8px;
        font-weight: 800;
        font-size: 0.7rem;
        background: rgba(76, 81, 191, 0.1);
        color: var(--primary);
        margin-right: 8px;
        text-transform: uppercase;
    }

    .q-text {
        font-size: 1.15rem;
        font-weight: 800;
        line-height: 1.6;
        margin: 20px 0;
        color: var(--text);
    }

    .opt-box {
        padding: 14px 18px;
        border-radius: 12px;
        background: var(--bg);
        box-shadow: inset 3px 3px 6px var(--shadow-dark), inset -3px -3px 6px var(--shadow-light);
        margin-bottom: 12px;
        font-weight: 700;
        font-size: 0.95rem;
        color: var(--text);
    }
    
    [data-testid="stSidebar"] {
        background: var(--bg);
        box-shadow: 4px 0 10px var(--shadow-dark);
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

def render_question_card(row):
    img_tag = f'<img src="{row["img"]}" style="width:100%; border-radius:15px; margin-bottom:15px; border:2px solid var(--primary);">' if str(row.get('img')) != 'nan' and row.get('img') != "" else ""
    
    st.markdown(f"""
    <div class="neu-card">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div><span class="badge">{row['course_code']}</span><span class="badge">{row['year']}</span></div>
            <div style="font-size:0.7rem; font-weight:900; opacity:0.5; text-transform:uppercase; letter-spacing:1px;">{row['topic']}</div>
        </div>
        <div class="q-text">{row['q']}</div>
        {img_tag}
        <div class="opt-box">A. {row['a']}</div>
        <div class="opt-box">B. {row['b']}</div>
        <div class="opt-box">C. {row['c']}</div>
        <div class="opt-box">D. {row['d']}</div>
    </div>
    """, unsafe_allow_html=True)

# --- 2. EXECUTION LOGIC ---

load_synapse_ui()

# Use Session State to keep the token active
if "token" not in st.session_state:
    st.session_state.token = ""

# Sidebar setup
with st.sidebar:
    st.title("Settings")
    # This updates the session state when typed in the sidebar
    input_token = st.text_input("Enter Token", type="password", key="sidebar_token")
    if input_token:
        st.session_state.token = input_token

# Main Page Logic
if not st.session_state.token:
    # If no token, show a nice input box right in the middle of the screen
    st.info("👋 Welcome to Synapse Ultimate.")
    main_token = st.text_input("Please enter your access token to continue:", type="password")
    if main_token:
        st.session_state.token = main_token
        st.rerun()
else:
    # TOKEN IS PRESENT - Show your actual app content here
    st.write(f"✅ Authenticated")
    
    # Placeholder data to test the UI
    test_row = {
        'course_code': 'BIO101', 'year': '2023', 'topic': 'Cell Biology',
        'q': 'Which organelle is known as the powerhouse of the cell?',
        'img': '', 'a': 'Nucleus', 'b': 'Mitochondria', 'c': 'Ribosome', 'd': 'Golgi'
    }
    render_question_card(test_row)

    if st.button("Log Out"):
        st.session_state.token = ""
        st.rerun()
