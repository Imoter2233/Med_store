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

# Load the Stealth UI
load_synapse_ui()

# --- 2. JAVASCRIPT SECURITY BRIDGE ---
def get_device_fingerprint():
    # JS Code to create a persistent UUID for the specific browser
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
    # We use a unique key based on time to force re-execution if needed, 
    # but the JS logic ensures the ID stays the same.
    return st_javascript(js)

def get_cached_token():
    return st_javascript('localStorage.getItem("synapse_auth_token");')

def cache_token(token):
    st_javascript(f'localStorage.setItem("synapse_auth_token", "{token}");')

def clear_cache():
    st_javascript('localStorage.removeItem("synapse_auth_token");')

# --- 3. AUTHENTICATION LOGIC ---
def auth_flow():
    # Initialize Session State
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    # 1. Get Device ID (Wait for JS to return)
    device_id = get_device_fingerprint()
    if device_id == 0 or device_id is None:
        st.stop() # Halts python until JS returns the value
    
    # 2. Check for Auto-Login (only if not already logged in)
    if not st.session_state.authenticated:
        cached_token = get_cached_token()
        
        # If we found a token in browser storage, validate it silently
        if cached_token and cached_token != 0 and "auto_login_checked" not in st.session_state:
            st.session_state.auto_login_checked = True
            verify_access(cached_token, device_id, silent=True)

    # 3. Show Login Form if still not authenticated
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
        st.stop() # Stop here, don't show the app yet

def verify_access(token, device_id, silent=False):
    try:
        # Connect to Sheets (ttl=0 for instant updates)
        conn = st.connection("gsheets", type=GSheetsConnection)
        tokens_df = conn.read(worksheet="Sheet1", ttl=0)
        
        # Admin Backdoor
        if token == "ADMIN_MASTER":
            st.session_state.authenticated = True
            st.rerun()
            return

        # Find Token
        match = tokens_df[tokens_df['Token'] == token]
        
        if match.empty:
            if not silent: st.error("❌ Invalid Access Token")
            if silent: clear_cache()
            return

        # Device Binding Logic
        registered_device = str(match.iloc[0]['DeviceID']).strip()
        
        # SCENARIO A: Token is fresh (No device bound) -> BIND IT
        if registered_device in ["", "nan", "None", "NaN"]:
            tokens_df.loc[tokens_df['Token'] == token, 'DeviceID'] = device_id
            conn.update(worksheet="Sheet1", data=tokens_df)
            
            st.session_state.authenticated = True
            cache_token(token) # Save to browser
            if not silent: 
                st.balloons()
                time.sleep(1)
                st.rerun()
            else:
                st.rerun()

        # SCENARIO B: Token matches this device -> ALLOW
        elif registered_device == device_id:
            st.session_state.authenticated = True
            cache_token(token) # Refresh cache
            if not silent: st.rerun()
            else: st.rerun()

        # SCENARIO C: Token used on different device -> BLOCK
        else:
            if not silent: st.error(f"⛔ Token is bound to another device.")
            if silent: clear_cache()

    except Exception as e:
        if not silent: st.error(f"Server Connection Failed. {e}")

# --- 4. DATA LOADER ---
@st.cache_data(ttl=600)
def get_data():
    URL = "https://raw.githubusercontent.com/Imoter2233/Med_store/main/questions.csv"
    try:
        df = pd.read_csv(URL)
        df['year'] = df['year'].astype(str) # Ensure year is string for filtering
        return df
    except:
        return pd.DataFrame()

# --- 5. MAIN APPLICATION INTERFACE ---
auth_flow() # Verify Security First

df = get_data()

if not df.empty:
    # --- HEADER AREA ---
    c1, c2 = st.columns([1, 4])
    with c2:
        # Header with hidden logout mechanism (Button looks like a simple icon)
        col_h1, col_h2 = st.columns([8, 1])
        with col_h1:
            st.markdown("<h2 style='color:#4f46e5; padding-top:10px;'>Synapse Ultimate</h2>", unsafe_allow_html=True)
        with col_h2:
            if st.button("🔒", help="Secure Logout"):
                clear_cache()
                st.session_state.authenticated = False
                st.rerun()

    # --- SIDEBAR FILTERS ---
    with st.sidebar:
        st.markdown("### 📚 Knowledge Base")
        
        # Course Filter
        all_courses = sorted(df['course_code'].unique())
        sel_course = st.multiselect("Select Course", all_courses)
        
        # Year Filter
        all_years = sorted(df['year'].unique(), reverse=True)
        sel_year = st.multiselect("Select Year", all_years)
        
        # Topic Filter
        all_topics = sorted(df['topic'].unique())
        sel_topic = st.multiselect("Select Topic", all_topics)
        
        st.markdown("---")
        st.caption("Synapse System v3.0")
        st.caption("Secure Connection Active")

    # --- FILTER LOGIC ---
    filtered_df = df.copy()
    if sel_course: filtered_df = filtered_df[filtered_df['course_code'].isin(sel_course)]
    if sel_year: filtered_df = filtered_df[filtered_df['year'].isin(sel_year)]
    if sel_topic: filtered_df = filtered_df[filtered_df['topic'].isin(sel_topic)]

    # --- SEARCH BAR ---
    search_query = st.text_input("Search", placeholder="🔍 Search keywords, topics, or questions...", label_visibility="collapsed")
    if search_query:
        filtered_df = filtered_df[
            filtered_df['q'].str.contains(search_query, case=False, na=False) | 
            filtered_df['topic'].str.contains(search_query, case=False, na=False)
        ]

    # --- RESULTS AREA ---
    total_results = len(filtered_df)
    
    st.markdown(f"<p style='color:#6b7280; font-size:0.9rem; margin-top:10px;'>Found <strong>{total_results}</strong> questions</p>", unsafe_allow_html=True)

    if total_results > 0:
        # Custom Pagination
        QUESTIONS_PER_PAGE = 5
        
        # Session state for page number to persist during interactions
        if 'page_number' not in st.session_state:
            st.session_state.page_number = 1
            
        max_pages = (total_results // QUESTIONS_PER_PAGE) + (1 if total_results % QUESTIONS_PER_PAGE > 0 else 0)
        
        # Render Questions
        start_idx = (st.session_state.page_number - 1) * QUESTIONS_PER_PAGE
        end_idx = start_idx + QUESTIONS_PER_PAGE
        
        current_batch = filtered_df.iloc[start_idx:end_idx]
        
        for index, row in current_batch.iterrows():
            render_question_card(row)
            
            # Answer Reveal Toggle
            with st.expander("👁️ View Answer & Explanation"):
                st.info(f"**Correct Option:** {row['ans']}")
                st.markdown(f"**Explanation:**\n{row['exp']}")

        # Pagination Controls
        st.markdown("---")
        c_prev, c_display, c_next = st.columns([1, 2, 1])
        
        with c_prev:
            if st.button("⬅️ Previous", disabled=(st.session_state.page_number == 1), use_container_width=True):
                st.session_state.page_number -= 1
                st.rerun()
                
        with c_display:
            st.markdown(f"<div style='text-align:center; padding-top:7px; font-weight:bold; color:#6b7280;'>Page {st.session_state.page_number} of {max_pages}</div>", unsafe_allow_html=True)
            
        with c_next:
            if st.button("Next ➡️", disabled=(st.session_state.page_number == max_pages), use_container_width=True):
                st.session_state.page_number += 1
                st.rerun()
                
    else:
        st.warning("No questions match your current filters. Try adjusting your search.")

else:
    st.error("Database Connection Failed. Please contact administrator.")