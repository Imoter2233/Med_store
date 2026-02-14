import streamlit as st
from streamlit_gsheets import GSheetsConnection

# 1. Page Config
st.set_page_config(page_title="Synapse Ultimate", layout="centered")

# 2. Combined UI Styles (Centered & Colored)
def load_full_ui():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');
    
    :root {
      --bg: #e0e5ec;
      --text: #4a4a4a;
      --primary: #4C51BF;
      --shadow-light: #ffffff;
      --shadow-dark: #a3b1c6;
    }

    /* Force background color on everything */
    .stApp { 
        background-color: var(--bg) !important; 
        color: var(--text); 
        font-family: 'Nunito', sans-serif; 
    }
    
    /* Centered Login Box */
    .login-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 40px;
        background: var(--bg);
        border-radius: 30px;
        box-shadow: 10px 10px 20px var(--shadow-dark), -10px -10px 20px var(--shadow-light);
        margin-top: 20%;
        border: 2px solid var(--primary);
    }

    /* Neumorphic Card for Questions */
    .neu-card {
        background: var(--bg);
        box-shadow: 7px 7px 14px var(--shadow-dark), -7px -7px 14px var(--shadow-light);
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 25px;
    }

    /* Hide default Streamlit elements */
    header, footer, #MainMenu {visibility: hidden;}
    
    /* Style the input box itself */
    div[data-baseweb="input"] {
        background-color: var(--bg) !important;
        border-radius: 10px !important;
        box-shadow: inset 4px 4px 8px var(--shadow-dark), inset -4px -4px 8px var(--shadow-light) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Question Card Component
def render_question_card(row):
    st.markdown(f"""
    <div class="neu-card">
        <div style="display:flex; justify-content:space-between;">
            <span style="color:var(--primary); font-weight:900;">{row['course_code']}</span>
            <span style="opacity:0.5;">{row['topic']}</span>
        </div>
        <div style="font-size:1.2rem; font-weight:800; margin:20px 0;">{row['q']}</div>
        <div style="padding:10px; border-radius:10px; background:rgba(0,0,0,0.05); margin-bottom:5px;">A. {row['a']}</div>
        <div style="padding:10px; border-radius:10px; background:rgba(0,0,0,0.05); margin-bottom:5px;">B. {row['b']}</div>
    </div>
    """, unsafe_allow_html=True)

# --- EXECUTION ---
load_full_ui()

# Initialize Session State
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    # THE CENTERED LOGIN AREA
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #4C51BF;'>Synapse Ultimate</h2>", unsafe_allow_html=True)
    st.write("👋 Please enter your token to unlock the dashboard.")
    
    token_input = st.text_input("Access Token", type="password", label_visibility="collapsed")
    
    if st.button("Unlock Access", use_container_width=True):
        if token_input == "YOUR_SECRET_TOKEN": # Replace this with your actual logic
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Invalid Token. Please try again.")
    
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # THE ACTUAL CONTENT (Shows after login)
    st.sidebar.button("Log Out", on_click=lambda: st.session_state.update({"authenticated": False}))
    
    st.markdown("### 📚 Your Dashboard")
    
    # Example Row
    test_data = {
        'course_code': 'MTH101', 'topic': 'Algebra', 
        'q': 'Simplify: 2x + 5x', 'a': '7x', 'b': '10x'
    }
    render_question_card(test_data)
