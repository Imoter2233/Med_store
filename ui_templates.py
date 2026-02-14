import streamlit as st

def load_synapse_ui():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    :root {
      --bg-color: #f4f7f6;
      --card-bg: #ffffff;
      --primary: #4f46e5;
    }

    /* BACKGROUND */
    .stApp {
        background-color: var(--bg-color);
        font-family: 'Inter', sans-serif;
    }
    
    /* HIDE STREAMLIT UI ELEMENTS */
    #MainMenu, header, footer {visibility: hidden !important;}
    .stDeployButton {display:none !important;}
    [data-testid="stToolbar"] {visibility: hidden !important;}
    [data-testid="stDecoration"] {visibility: hidden !important;}
    
    /* LOGIN WRAPPER */
    .login-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        padding-top: 50px;
    }
    
    .login-box {
        background: var(--card-bg);
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        width: 100%;
        max-width: 380px;
        text-align: center;
        border: 1px solid #e5e7eb;
    }

    /* CARD STYLES */
    .q-card {
        background: var(--card-bg);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        border-left: 5px solid var(--primary);
    }
    
    .q-meta {
        font-size: 0.7rem;
        text-transform: uppercase;
        color: var(--primary);
        font-weight: 800;
        margin-bottom: 5px;
    }

    .q-text {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 15px;
    }

    .opt-grid div {
        background: #f9fafb;
        padding: 10px;
        border-radius: 8px;
        font-size: 0.9rem;
        margin-bottom: 5px;
        border: 1px solid #eee;
    }
    
    /* CUSTOM INPUTS */
    div[data-baseweb="input"] {
        background-color: #fff !important;
        border-radius: 10px !important;
    }
    
    /* CUSTOM BUTTONS */
    button[kind="primary"] {
        background-color: var(--primary) !important;
        color: white !important;
        border: none !important;
        padding: 0.5rem 1rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

def render_question_card(row):
    img_html = ""
    if str(row.get('img')) != 'nan' and row.get('img', '') != "":
        img_html = f'<div style="margin-bottom:10px;"><img src="{row["img"]}" style="width:100%; border-radius:10px;"></div>'

    st.markdown(f"""
    <div class="q-card">
        <div class="q-meta">{row['course_code']} &bull; {row['year']}</div>
        <div class="q-text">{row['q']}</div>
        {img_html}
        <div class="opt-grid">
            <div>A. {row['a']}</div>
            <div>B. {row['b']}</div>
            <div>C. {row['c']}</div>
            <div>D. {row['d']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)