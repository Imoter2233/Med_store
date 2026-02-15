import streamlit as st
import hashlib
import json
from datetime import datetime

def load_synapse_ui():
    """Enhanced neumorphic UI with hidden Streamlit elements and professional styling"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    :root {
      --bg-primary: #f5f7fa;
      --bg-secondary: #ffffff;
      --text-primary: #1a202c;
      --text-secondary: #718096;
      --primary: #4C51BF;
      --primary-dark: #3730a3;
      --accent: #f59e0b;
      --success: #10b981;
      --danger: #ef4444;
      --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.08);
      --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
      --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.12);
      --shadow-neu: 6px 6px 12px rgba(0, 0, 0, 0.1), -6px -6px 12px rgba(255, 255, 255, 0.8);
    }

    /* HIDE STREAMLIT ELEMENTS */
    #MainMenu { visibility: hidden; }
    footer { display: none !important; visibility: hidden !important; }
    header { display: none !important; visibility: hidden !important; }
    .stDeployButton { display: none; }
    [data-testid="stToolbar"] { display: none; }
    
    /* CUSTOM SCROLLBAR */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: var(--bg-primary);
    }
    ::-webkit-scrollbar-thumb {
        background: var(--primary);
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary-dark);
    }

    /* APP BACKGROUND & TEXT */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
        color: var(--text-primary);
        font-family: 'Inter', sans-serif;
    }

    /* MAIN CONTAINER */
    .main {
        background: transparent;
    }

    /* HEADERS */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        color: var(--text-primary);
    }

    h1 { font-size: 2.5rem; letter-spacing: -0.5px; }
    h2 { font-size: 1.875rem; margin-top: 30px; }
    h3 { font-size: 1.5rem; }

    /* NEUMORPHIC CARD */
    .neu-card {
        background: var(--bg-secondary);
        box-shadow: var(--shadow-neu);
        border-radius: 16px;
        padding: 28px;
        margin-bottom: 28px;
        border: 1px solid rgba(255, 255, 255, 0.7);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: blur(10px);
    }

    .neu-card:hover {
        box-shadow: 8px 8px 16px rgba(0, 0, 0, 0.12), -8px -8px 16px rgba(255, 255, 255, 0.9);
        transform: translateY(-2px);
    }

    /* BADGES */
    .badge {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.7rem;
        background: linear-gradient(135deg, rgba(76, 81, 191, 0.15), rgba(76, 81, 191, 0.05));
        color: var(--primary);
        margin-right: 10px;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        border: 1px solid rgba(76, 81, 191, 0.2);
        transition: all 0.2s;
    }

    .badge:hover {
        background: rgba(76, 81, 191, 0.2);
        border-color: rgba(76, 81, 191, 0.4);
    }

    /* QUESTION TEXT */
    .q-text {
        font-family: 'Poppins', sans-serif;
        font-size: 1.25rem;
        font-weight: 700;
        line-height: 1.7;
        margin: 20px 0;
        color: var(--text-primary);
    }

    /* OPTION BOXES */
    .opt-box {
        padding: 16px 18px;
        border-radius: 12px;
        background: var(--bg-primary);
        border: 2px solid transparent;
        margin-bottom: 12px;
        font-weight: 600;
        font-size: 0.95rem;
        color: var(--text-primary);
        transition: all 0.2s;
        cursor: pointer;
        user-select: none;
    }

    .opt-box:hover {
        border-color: var(--primary);
        background: linear-gradient(135deg, rgba(76, 81, 191, 0.08), rgba(76, 81, 191, 0.02));
        transform: translateX(4px);
    }

    /* SIDEBAR STYLING */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f5f7fa 100%);
        box-shadow: 2px 0 10px rgba(0, 0, 0, 0.08);
    }

    [data-testid="stSidebar"] > div > div {
        padding-top: 20px;
    }

    /* BUTTONS */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary), var(--primary-dark));
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 10px 24px;
        transition: all 0.3s;
        box-shadow: var(--shadow-md);
        font-family: 'Poppins', sans-serif;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    /* TEXT INPUT */
    .stTextInput > div > div > input,
    .stPasswordInput > div > div > input,
    .stSelectbox > div > div > select {
        border-radius: 10px;
        border: 2px solid #e2e8f0 !important;
        padding: 12px 14px !important;
        font-family: 'Inter', sans-serif;
        transition: all 0.2s;
    }

    .stTextInput > div > div > input:focus,
    .stPasswordInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(76, 81, 191, 0.1);
    }

    /* MULTISELECT */
    .stMultiSelect > div > div > div {
        border-radius: 10px;
        border: 2px solid #e2e8f0 !important;
        padding: 8px 12px !important;
    }

    /* ALERTS */
    .stAlert {
        border-radius: 12px;
        border-left: 4px solid;
        padding: 16px;
        background-color: rgba(255, 255, 255, 0.8);
    }

    [data-testid="stAlert"] > div {
        border-radius: 12px;
    }

    /* EXPANDER */
    .streamlit-expanderHeader {
        border-radius: 10px;
        background: var(--bg-primary);
        border: 1px solid #e2e8f0;
        transition: all 0.2s;
    }

    .streamlit-expanderHeader:hover {
        border-color: var(--primary);
        background: linear-gradient(135deg, rgba(76, 81, 191, 0.08), rgba(76, 81, 191, 0.02));
    }

    /* DIVIDER */
    .stDivider {
        margin: 20px 0;
        border-color: #e2e8f0;
    }

    /* METRIC */
    [data-testid="metric-container"] {
        background: var(--bg-secondary);
        padding: 20px;
        border-radius: 12px;
        box-shadow: var(--shadow-sm);
    }

    /* TEXT & PARAGRAPHS */
    p {
        color: var(--text-secondary);
        line-height: 1.6;
        font-size: 0.95rem;
    }

    small {
        color: var(--text-secondary);
        font-size: 0.85rem;
    }

    /* RESPONSIVE */
    @media (max-width: 640px) {
        h1 { font-size: 1.75rem; }
        h2 { font-size: 1.5rem; }
        .neu-card { padding: 20px; margin-bottom: 16px; }
        .q-text { font-size: 1.1rem; }
    }

    /* PREVENT CODE EXPOSURE */
    code {
        background: var(--bg-primary);
        border-radius: 6px;
        padding: 2px 6px;
        font-family: 'Monaco', monospace;
        font-size: 0.85rem;
        user-select: none;
    }

    pre {
        background: var(--bg-primary);
        border-radius: 8px;
        padding: 12px;
        overflow: hidden;
        border: 1px solid #e2e8f0;
    }

    pre code {
        color: transparent;
        text-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
        user-select: none;
        pointer-events: none;
    }

    /* PREVENT TEXT SELECTION ON SENSITIVE AREAS */
    .neu-card, .badge, .opt-box {
        -webkit-user-select: none;
        -moz-user-select: none;
        user-select: none;
    }
    </style>
    """, unsafe_allow_html=True)


def render_question_card(row):
    """Render a single question card with all metadata"""
    try:
        img_tag = ""
        if str(row.get('img', 'nan')) != 'nan' and str(row.get('img', '')) != "":
            img_tag = f'<img src="{row["img"]}" style="width:100%; border-radius:12px; margin-bottom:18px; border:2px solid var(--primary); box-shadow: var(--shadow-md);" alt="question-image">'
        
        st.markdown(f"""
        <div class="neu-card">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px; margin-bottom:12px;">
                <div>
                    <span class="badge">{row.get('course_code', 'N/A')}</span>
                    <span class="badge">{row.get('year', 'N/A')}</span>
                </div>
                <div style="font-size:0.75rem; font-weight:700; opacity:0.5; text-transform:uppercase; letter-spacing:1.2px;">{row.get('topic', 'General')}</div>
            </div>
            <div class="q-text">{row.get('q', 'Question not available')}</div>
            {img_tag}
            <div class="opt-box">A. {row.get('a', 'Option not available')}</div>
            <div class="opt-box">B. {row.get('b', 'Option not available')}</div>
            <div class="opt-box">C. {row.get('c', 'Option not available')}</div>
            <div class="opt-box">D. {row.get('d', 'Option not available')}</div>
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error rendering card: {str(e)[:50]}")


def generate_device_fingerprint():
    """
    Generate a robust device fingerprint combining multiple factors
    User-Agent, viewport, browser data, and timezone
    """
    try:
        headers = st.context.headers
        user_agent = headers.get("User-Agent", "unknown")
        accept_language = headers.get("Accept-Language", "unknown")
        accept_encoding = headers.get("Accept-Encoding", "unknown")
        
        fingerprint_string = f"{user_agent}|{accept_language}|{accept_encoding}"
        device_id = hashlib.sha256(fingerprint_string.encode()).hexdigest()
        
        return device_id
    except:
        return hashlib.sha256(b"unknown").hexdigest()


def is_token_valid_for_device(token, registered_device_id, current_device_id):
    """
    Validate token against device binding
    Returns tuple: (is_valid, message)
    """
    if not token or token.strip() == "":
        return False, "Token cannot be empty"
    
    if registered_device_id in ["", "nan", "None", None]:
        return True, "NEW_DEVICE"
    
    if registered_device_id == current_device_id:
        return True, "VERIFIED"
    
    return False, "DEVICE_MISMATCH"


def log_security_event(event_type, token, device_id, status):
    """Log security events for audit trail"""
    timestamp = datetime.now().isoformat()
    log_entry = {
        "timestamp": timestamp,
        "event_type": event_type,
        "token": token[:8] + "****" if token else "N/A",
        "device_id": device_id[:16] + "****" if device_id else "N/A",
        "status": status
    }
    return log_entry