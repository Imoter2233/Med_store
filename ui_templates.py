import streamlit as st
from streamlit_gsheets import GSheetsConnection

# --- 1. UI TEMPLATE CONFIGURATION ---
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

    /* Set Background */
    .stApp { background: var(--bg); color: var(--text); font-family: 'Nunito', sans-serif; }
    
    /* Neumorphic Card */
    .neu-card {
        background: var(--bg);
        box-shadow: 7px 7px 14px var(--shadow-dark), -7px -7px 14px var(--shadow-light);
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 25px;
        border: none;
        transition: 0.3s;
    }

    /* Badges */
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

    /* Question Text */
    .q-text {
        font-size: 1.15rem;
        font-weight: 800;
        line-height: 1.6;
        margin: 20px 0;
        color: var(--text);
    }

    /* Option Box */
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
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: var(--bg);
        box-shadow: 4px 0 10px var(--shadow-dark);
    }

    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

def render_question_card(row):
    # Image logic
    img_tag = f'<img src="{row["img"]}" style="width:100%; border-radius:15px; margin-bottom:15px; border:2px solid var(--primary);">' if str(row['img']) != 'nan' and row['img'] != "" else ""
    
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

# --- 2. MAIN APP LOGIC ---

# Initialize UI
load_synapse_ui()

# Create the Sidebar Token Input
with st.sidebar:
    st.markdown("### 🔑 Authentication")
    user_token = st.text_input("Enter your Access Token", type="password", placeholder="Paste token here...")
    st.info("The token grants you access to Synapse Ultimate features.")

# Main Screen Behavior
if not user_token:
    # This matches the message in your screenshot
    st.info("👋 Welcome to Synapse Ultimate. Please enter your token in the sidebar.")
else:
    # Everything inside this 'else' block only shows once the token is typed
    st.success("Access Granted!")
    
    # Example connection to GSheets
    # conn = st.connection("gsheets", type=GSheetsConnection)
    # df = conn.read()
    
    # For demonstration, here is how a card would look:
    sample_data = {
        'course_code': 'MTH101',
        'year': '2024',
        'topic': 'Calculus',
        'q': 'What is the derivative of sin(x)?',
        'img': '',
        'a': 'cos(x)',
        'b': '-cos(x)',
        'c': 'tan(x)',
        'd': 'sec(x)'
    }
    render_question_card(sample_data)
