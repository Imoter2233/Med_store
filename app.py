import streamlit as st
import pandas as pd
import hashlib
from datetime import datetime
from ui_templates import (
    load_synapse_ui, 
    render_question_card, 
    generate_device_fingerprint,
    is_token_valid_for_device,
    log_security_event
)
from streamlit_gsheetsconnection import GSheetsConnection

# ============================================================================
# PAGE CONFIGURATION & INITIALIZATION
# ============================================================================

st.set_page_config(
    page_title="Synapse Ultimate",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded"
)

load_synapse_ui()

# ============================================================================
# SESSION STATE MANAGEMENT
# ============================================================================

def initialize_session():
    """Initialize all session variables on first load"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'device_id' not in st.session_state:
        st.session_state.device_id = None
    if 'token_used' not in st.session_state:
        st.session_state.token_used = None
    if 'session_start' not in st.session_state:
        st.session_state.session_start = datetime.now()
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 1
    if 'search_query' not in st.session_state:
        st.session_state.search_query = ""
    if 'selected_courses' not in st.session_state:
        st.session_state.selected_courses = []
    if 'selected_years' not in st.session_state:
        st.session_state.selected_years = []
    if 'selected_topics' not in st.session_state:
        st.session_state.selected_topics = []

initialize_session()

# ============================================================================
# DEVICE FINGERPRINTING & PERSISTENT AUTHENTICATION
# ============================================================================

def authenticate_user():
    """
    Bulletproof authentication with device binding
    - Same device returns to app without re-entering token
    - Different device is denied even with same token
    - Uses enhanced device fingerprinting
    """
    
    # Generate device fingerprint
    current_device_id = generate_device_fingerprint()
    st.session_state.device_id = current_device_id
    
    # Check if already authenticated in this session
    if st.session_state.authenticated:
        return True
    
    # AUTH UI
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔐 Synapse Access")
    
    token_input = st.sidebar.text_input(
        "Enter Access Token",
        type="password",
        placeholder="Token required",
        key="auth_token_input"
    )
    
    # If no token provided, show welcome message
    if not token_input:
        st.sidebar.info(
            "👋 Welcome to **Synapse Ultimate**\n\n"
            "Enter your access token to proceed."
        )
        return False
    
    try:
        # Connect to Google Sheets
        conn = st.connection("gsheets", type=GSheetsConnection)
        tokens_df = conn.read(worksheet="Tokens", ttl=0)
        
        # Find matching token
        token_match = tokens_df[tokens_df['Token'] == token_input]
        
        if token_match.empty:
            st.sidebar.error("❌ Invalid token. Access denied.")
            log_security_event("AUTH_FAILED", token_input, current_device_id, "INVALID_TOKEN")
            return False
        
        registered_device_id = str(token_match.iloc[0].get('DeviceID', '')).strip()
        registered_date = token_match.iloc[0].get('RegisteredDate', datetime.now().isoformat())
        
        # VALIDATION LOGIC
        is_valid, validation_status = is_token_valid_for_device(
            token_input,
            registered_device_id,
            current_device_id
        )
        
        if validation_status == "NEW_DEVICE":
            # First time binding this token to device
            tokens_df.loc[tokens_df['Token'] == token_input, 'DeviceID'] = current_device_id
            tokens_df.loc[tokens_df['Token'] == token_input, 'RegisteredDate'] = datetime.now().isoformat()
            
            conn.update(worksheet="Tokens", data=tokens_df)
            
            st.sidebar.success("✨ Device bound successfully!")
            st.balloons()
            
            log_security_event("AUTH_SUCCESS", token_input, current_device_id, "NEW_DEVICE_BOUND")
            
            st.session_state.authenticated = True
            st.session_state.token_used = token_input
            return True
        
        elif validation_status == "VERIFIED":
            # Same device, same token - seamless access
            st.sidebar.success("🔓 Access granted")
            log_security_event("AUTH_SUCCESS", token_input, current_device_id, "DEVICE_VERIFIED")
            
            st.session_state.authenticated = True
            st.session_state.token_used = token_input
            return True
        
        else:  # DEVICE_MISMATCH
            st.sidebar.error(
                "🚫 **Access Denied**\n\n"
                "This token is registered to another device. "
                "For security, tokens are bound to single devices. "
                "Contact administrator if unauthorized."
            )
            log_security_event("AUTH_FAILED", token_input, current_device_id, "DEVICE_MISMATCH")
            return False
    
    except Exception as e:
        st.sidebar.warning(f"⚠️ Error: {str(e)[:40]}...")
        log_security_event("AUTH_ERROR", token_input, current_device_id, f"ERROR: {str(e)[:30]}")
        return False


def show_logout_button():
    """Show logout button in sidebar if authenticated"""
    if st.session_state.authenticated:
        st.sidebar.markdown("---")
        if st.sidebar.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.token_used = None
            st.session_state.device_id = None
            st.sidebar.success("Logged out successfully!")
            st.rerun()

# ============================================================================
# DATA LOADING & CACHING
# ============================================================================

@st.cache_data(ttl=300)
def load_questions():
    """
    Load questions from GitHub CSV
    Updates every 5 minutes automatically
    """
    CSV_URL = "https://raw.githubusercontent.com/Imoter2233/Med_store/main/questions.csv"
    try:
        df = pd.read_csv(CSV_URL)
        df['year'] = df['year'].astype(str)
        
        # Data validation
        required_cols = ['id', 'q', 'a', 'b', 'c', 'd', 'ans', 'exp', 'year', 'course_code', 'topic']
        for col in required_cols:
            if col not in df.columns:
                df[col] = ""
        
        return df
    except Exception as e:
        st.error(f"Failed to load questions: {str(e)[:50]}")
        return pd.DataFrame()

# ============================================================================
# FILTERING ENGINE
# ============================================================================

def apply_filters(df):
    """Apply all filters from sidebar"""
    filtered = df.copy()
    
    # Course filter
    if st.session_state.selected_courses:
        filtered = filtered[filtered['course_code'].isin(st.session_state.selected_courses)]
    
    # Year filter
    if st.session_state.selected_years:
        filtered = filtered[filtered['year'].isin(st.session_state.selected_years)]
    
    # Topic filter
    if st.session_state.selected_topics:
        filtered = filtered[filtered['topic'].isin(st.session_state.selected_topics)]
    
    # Search filter
    if st.session_state.search_query:
        mask = (
            filtered['q'].str.contains(st.session_state.search_query, case=False, na=False) |
            filtered['topic'].str.contains(st.session_state.search_query, case=False, na=False) |
            filtered['course_code'].str.contains(st.session_state.search_query, case=False, na=False)
        )
        filtered = filtered[mask]
    
    return filtered

# ============================================================================
# MAIN APPLICATION
# ============================================================================

# AUTHENTICATION CHECK
if not authenticate_user():
    st.info("🔐 Please authenticate to continue")
    st.stop()

# Show logout button
show_logout_button()

# Load data
df = load_questions()

if df.empty:
    st.error("📚 Library is empty. Questions not found.")
    st.stop()

# HEADER
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(
        "<h1 style='text-align:center; margin-bottom:5px;'>🧠 Synapse Ultimate</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align:center; opacity:0.6; margin-bottom:20px;'>Professional Past Questions Engine</p>",
        unsafe_allow_html=True
    )

# SIDEBAR FILTERS
st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Refine Search")

# Course filter
courses = sorted(df['course_code'].unique())
st.session_state.selected_courses = st.sidebar.multiselect(
    "Select Course",
    courses,
    default=st.session_state.selected_courses,
    key="filter_courses"
)

# Year filter
years = sorted(df['year'].unique(), reverse=True)
st.session_state.selected_years = st.sidebar.multiselect(
    "Select Year",
    years,
    default=st.session_state.selected_years,
    key="filter_years"
)

# Topic filter
topics = sorted(df['topic'].unique())
st.session_state.selected_topics = st.sidebar.multiselect(
    "Select Topic",
    topics,
    default=st.session_state.selected_topics,
    key="filter_topics"
)

# Search
st.markdown("### 🔍 Search Database")
search_col1, search_col2 = st.columns([4, 1])
with search_col1:
    st.session_state.search_query = st.text_input(
        "Search keywords...",
        value=st.session_state.search_query,
        placeholder="Type to search...",
        key="search_input"
    )
with search_col2:
    if st.button("🔄", help="Reset search", key="reset_search"):
        st.session_state.search_query = ""
        st.rerun()

# Apply filters
filtered_df = apply_filters(df)

# RESULTS INFO
total_results = len(filtered_df)
st.markdown(f"<small style='opacity:0.6;'>**Found:** {total_results} question{'s' if total_results != 1 else ''}</small>", unsafe_allow_html=True)

# PAGINATION
if total_results > 0:
    items_per_page = 10
    total_pages = (total_results // items_per_page) + (1 if total_results % items_per_page else 0)
    
    # Pagination controls
    pag_col1, pag_col2, pag_col3 = st.columns([1, 2, 1])
    
    with pag_col1:
        if st.button("⬅️ Previous", key="prev_page", disabled=(st.session_state.current_page <= 1)):
            st.session_state.current_page -= 1
            st.rerun()
    
    with pag_col2:
        page_display = st.columns(total_pages, gap="small")
        for i in range(total_pages):
            with page_display[i]:
                if st.button(
                    str(i + 1),
                    key=f"page_{i+1}",
                    use_container_width=True,
                ):
                    st.session_state.current_page = i + 1
                    st.rerun()
    
    with pag_col3:
        if st.button("Next ➡️", key="next_page", disabled=(st.session_state.current_page >= total_pages)):
            st.session_state.current_page += 1
            st.rerun()
    
    # Validate current page
    if st.session_state.current_page > total_pages:
        st.session_state.current_page = total_pages
    if st.session_state.current_page < 1:
        st.session_state.current_page = 1
    
    st.markdown(
        f"<small style='text-align:center;'><strong>Page {st.session_state.current_page} of {total_pages}</strong></small>",
        unsafe_allow_html=True
    )
    
    # Render questions
    start_idx = (st.session_state.current_page - 1) * items_per_page
    end_idx = min(start_idx + items_per_page, total_results)
    
    st.markdown("---")
    
    for idx in range(start_idx, end_idx):
        row = filtered_df.iloc[idx]
        render_question_card(row)
        
        # Answer expandable section
        with st.expander(f"📖 View Answer & Explanation", key=f"answer_{row.get('id', idx)}"):
            col1, col2 = st.columns([1, 3])
            
            with col1:
                st.markdown(f"**Answer:**")
            with col2:
                st.markdown(f"`{row.get('ans', 'N/A')}`")
            
            st.markdown("---")
            st.markdown(f"**Explanation:**\n\n{row.get('exp', 'No explanation available')}")

else:
    st.warning("📭 No questions match your selection. Try adjusting filters.")

# FOOTER
st.markdown("---")
st.markdown(
    "<small style='text-align:center; opacity:0.5;'>© 2026 Synapse Ultimate | Secure Learning Platform</small>",
    unsafe_allow_html=True
)