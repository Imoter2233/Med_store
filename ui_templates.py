import streamlit as st

def load_synapse_ui():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    :root {
      --bg-color: #f4f7f6;
      --card-bg: #ffffff;
      --primary: #4f46e5;
      --text-dark: #1f2937;
      --text-light: #6b7280;
    }

    /* --- GLOBAL RESET --- */
    .stApp {
        background-color: var(--bg-color);
        font-family: 'Inter', sans-serif;
    }
    
    /* --- HIDE STREAMLIT BLOAT (SECURITY) --- */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    .stDeployButton {display:none !important;}
    [data-testid="stToolbar"] {visibility: hidden !important;}
    [data-testid="stDecoration"] {visibility: hidden !important;}
    [data-testid="stStatusWidget"] {visibility: hidden !important;}
    
    /* Remove top padding caused by hidden header */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }

    /* --- LOGIN UI --- */
    .login-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 80vh;
    }
    
    .login-box {
        background: var(--card-bg);
        padding: 40px;
        border-radius: 24px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        width: 100%;
        max-width: 400px;
        text-align: center;
        border: 1px solid #e5e7eb;
    }

    /* --- QUESTION CARDS --- */
    .q-card {
        background: var(--card-bg);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border-left: 6px solid var(--primary);
        transition: transform 0.2s ease-in-out;
    }
    
    .q-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }

    .q-meta {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: var(--primary);
        font-weight: 800;
        margin-bottom: 8px;
    }

    .q-text {
        font-size: 1.125rem;
        font-weight: 700;
        color: var(--text-dark);
        margin-bottom: 16px;
        line-height: 1.5;
    }

    .opt-grid {
        display: grid;
        grid-template-columns: 1fr;
        gap: 8px;
    }

    .opt-item {
        background: #f9fafb;
        padding: 12px 16px;
        border-radius: 8px;
        font-size: 0.95rem;
        color: var(--text-dark);
        border: 1px solid #f3f4f6;
    }

    /* --- INPUT FIELDS & BUTTONS --- */
    div[data-baseweb="input"] {
        background-color: #f9fafb !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 12px !important;
    }

    button[kind="primary"] {
        background-color: var(--primary) !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.2) !important;
    }
    
    button[kind="secondary"] {
        border: 1px solid #e5e7eb !important;
        color: var(--text-light) !important;
    }

    </style>
    """, unsafe_allow_html=True)

def render_question_card(row):
    # Conditional Image Rendering
    img_html = ""
    if str(row.get('img')) != 'nan' and row.get('img', '') != "":
        img_html = f'<div style="margin-bottom:16px;"><img src="{row["img"]}" style="width:100%; border-radius:12px; object-fit:cover;"></div>'

    st.markdown(f"""
    <div class="q-card">
        <div class="q-meta">
            {row['course_code']} &bull; {row['year']} &bull; {row['topic']}
        </div>
        <div class="q-text">
            {row['q']}
        </div>
        {img_html}
        <div class="opt-grid">
            <div class="opt-item"><strong>A.</strong> {row['a']}</div>
            <div class="opt-item"><strong>B.</strong> {row['b']}</div>
            <div class="opt-item"><strong>C.</strong> {row['c']}</div>
            <div class="opt-item"><strong>D.</strong> {row['d']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)