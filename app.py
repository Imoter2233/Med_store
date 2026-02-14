import streamlit as st
import pandas as pd
import time
from streamlit_javascript import st_javascript
from ui_templates import load_synapse_ui, render_question_card
from streamlit_gsheets import GSheetsConnection 

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Synapse Ultimate",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Load the UI Styles immediately
load_synapse_ui()

# --- 2. JAVASCRIPT SECURITY BRIDGE ---
def get_device_fingerprint():
    # We use a simple key to ensure it runs only once per render cycle
    js = """
    (function() {
        let fps = localStorage.getItem("synapse_device_uuid");
        if (!fps) {
            fps = crypto.randomUUID();
            localStorage.setItem("synapse_device_uuid", fps);
        }
        return fps;
    })();
    """
    return st_javascript(js)

def get_cached_token():
    return st_javascript('localStorage.getItem("synapse_auth_token");')

def cache_token(token):
    st_javascript(f'localStorage.setItem("synapse_auth_token", "{token}");')

def clear_cache():
    st_javascript('localStorage.removeItem("synapse_auth_token");')

# --- 3. AUTHENTICATION LOGIC ---
def auth_flow():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    # --- CRITICAL FIX: HANDLE LOADING STATE ---
    device_id = get_device_fingerprint()
    
    # If JS is still loading (returns 0 or None), show a spinner and wait.
    # This prevents the "Blank Screen" of death.
    if device_id == 0 or device_id is None:
        st.markdown("""
        <div style='text-align:center; margin-top:50px;'>
            <h3 style='color:#4f46e5;'>⚙️ Synapse Security</h3>
            <p>Establishing secure handshake...</p>
        </div>
        """, unsafe_allow_html=True)
        st.stop() # Stops execution here, but shows the message above
    
    # 2. Check for Auto-Login (only if not already logged in)
    if not st.session_state.authenticated:
        cached_token = get_cached_token()
        if cached_token and cached_token != 0 and "auto_login_checked" not in st.session_state:
            st.session_state.auto_login_checked = True
            verify_access(cached_token, device_id, silent=True)

    # 3. Show Login Form
    if not st.session_state.authenticated:
        st.markdown('<div class="login-wrapper"><div class="login-box">', unsafe_allow_html=True)
        st.markdown("<h1 style='color:#4f46e5; margin:0;'>Synapse</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#6b7280; font-size:0.9rem; margin-bottom:25px;'>Secure Assessment Engine</p>", unsafe_allow_html=True)
        
        token_input = st.text_input("Enter Activation Key", type="password", placeholder="Token", label_visibility="collapsed")
        
        if st.button("Authenticate System", use_container_width=True, type="primary"):
            if not token_input:
                st.warning("Token required.")
            else:
                verify_access(token_input, device_id, silent=False)
        
        st.markdown('</div></div>', unsafe_allow_html=True)
        st.stop()

def verify_access(token, device_id, silent=False):
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        tokens_df = conn.read(worksheet="Sheet1", ttl=0)
        
        if token == "ADMIN_MASTER":
            st.session_state.authenticated = True
            st.rerun()
            return

        match = tokens_df[tokens_df['Token'] == token]
        
        if match.empty:
            if not silent: st.error("❌ Invalid Access Token")
            if silent: clear_cache()
            return

        registered_device = str(match.iloc[0]['DeviceID']).strip()
        
        # New Token -> Bind
        if registered_device in ["", "nan", "None", "NaN"]:
            tokens_df.loc[tokens_df['Token'] == token, 'DeviceID'] = device_id
            conn.update(worksheet="Sheet1", data=tokens_df)
            st.session_state.authenticated = True
            cache_token(token)
            if not silent: st.rerun()
            else: st.rerun()

        # Existing Token -> Check Match
        elif registered_device == device_id:
            st.session_state.authenticated = True
            cache_token(token)
            if not silent: st.rerun()
            else: st.rerun()

        # Mismatch -> Block
        else:
            if not silent: st.error(f"⛔ Token bound to another device.")
            if silent: clear_cache()

    except Exception as e:
        if not silent: st.error(f"Server Connection Failed.")

# --- 4. MAIN APP ---
auth_flow()

@st.cache_data(ttl=600)
def get_data():
    URL = "https://raw.githubusercontent.com/Imoter2233/Med_store/main/questions.csv"
    try:
        df = pd.read_csv(URL)
        df['year'] = df['year'].astype(str)
        return df
    except:
        return pd.DataFrame()

df = get_data()

if not df.empty:
    # Header
    c1, c2 = st.columns([1, 4])
    with c2:
        col_h1, col_h2 = st.columns([8, 1])
        with col_h1:
            st.markdown("<h2 style='color:#4f46e5; padding-top:10px;'>Synapse Ultimate</h2>", unsafe_allow_html=True)
        with col_h2:
            if st.button("🔒", help="Logout"):
                clear_cache()
                st.session_state.authenticated = False
                st.rerun()

    # Sidebar
    with st.sidebar:
        st.markdown("### 📚 Knowledge Base")
        sel_course = st.multiselect("Course", sorted(df['course_code'].unique()))
        sel_year = st.multiselect("Year", sorted(df['year'].unique(), reverse=True))
        sel_topic = st.multiselect("Topic", sorted(df['topic'].unique()))
        st.markdown("---")
        st.caption("v3.0 Secure")

    # Filter Logic
    filtered_df = df.copy()
    if sel_course: filtered_df = filtered_df[filtered_df['course_code'].isin(sel_course)]
    if sel_year: filtered_df = filtered_df[filtered_df['year'].isin(sel_year)]
    if sel_topic: filtered_df = filtered_df[filtered_df['topic'].isin(sel_topic)]

    # Search
    search_query = st.text_input("Search", placeholder="🔍 Search...", label_visibility="collapsed")
    if search_query:
        filtered_df = filtered_df[
            filtered_df['q'].str.contains(search_query, case=False, na=False) | 
            filtered_df['topic'].str.contains(search_query, case=False, na=False)
        ]

    # Results & Pagination
    total_results = len(filtered_df)
    st.markdown(f"<p style='color:#6b7280; font-size:0.9rem;'>Found <strong>{total_results}</strong> questions</p>", unsafe_allow_html=True)

    if total_results > 0:
        if 'page_number' not in st.session_state: st.session_state.page_number = 1
        QUESTIONS_PER_PAGE = 5
        max_pages = (total_results // QUESTIONS_PER_PAGE) + (1 if total_results % QUESTIONS_PER_PAGE > 0 else 0)
        
        # Reset page if out of bounds
        if st.session_state.page_number > max_pages: st.session_state.page_number = 1
        
        start = (st.session_state.page_number - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        
        for index, row in filtered_df.iloc[start:end].iterrows():
            render_question_card(row)
            with st.expander("👁️ View Answer"):
                st.info(f"**Answer:** {row['ans']}")
                st.markdown(f"_{row['exp']}_")

        # Pagination Buttons
        st.markdown("---")
        c_prev, c_disp, c_next = st.columns([1, 2, 1])
        with c_prev:
            if st.button("⬅️", disabled=(st.session_state.page_number == 1), use_container_width=True):
                st.session_state.page_number -= 1
                st.rerun()
        with c_disp:
            st.markdown(f"<div style='text-align:center; padding-top:7px;'>Page {st.session_state.page_number} / {max_pages}</div>", unsafe_allow_html=True)
        with c_next:
            if st.button("➡️", disabled=(st.session_state.page_number >= max_pages), use_container_width=True):
                st.session_state.page_number += 1
                st.rerun()
    else:
        st.warning("No matches found.")

else:
    st.error("Database connection failed.")