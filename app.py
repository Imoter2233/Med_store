import streamlit as st
import pandas as pd
from ui_templates import load_synapse_ui, render_question_card
from streamlit_gsheets import GSheetsConnection 

# --- 1. INITIAL SETUP ---
st.set_page_config(page_title="Synapse Ultimate", layout="centered")
load_synapse_ui()

# --- 2. SECURITY LAYER (UPDATED FOR CENTERED UI) ---
def security_check():
    device_id = str(hash(st.context.headers.get("User-Agent", "unknown")))
    
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        # CENTERED LOGIN BOX
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown("<h1 style='color: #4C51BF;'>Synapse Ultimate</h1>", unsafe_allow_html=True)
        st.write("👋 Welcome. Please enter your activation token.")
        
        token = st.text_input("Enter Access Token", type="password", label_visibility="collapsed", placeholder="Activation Token")
        
        if st.button("Unlock Dashboard", use_container_width=True):
            if not token:
                st.warning("Please enter a token.")
            else:
                try:
                    conn = st.connection("gsheets", type=GSheetsConnection)
                    tokens_df = conn.read(worksheet="Sheet1", ttl=0)
                    match = tokens_df[tokens_df['Token'] == token]
                    
                    if match.empty:
                        # Backup Admin Check
                        if token == "ADMIN2024":
                            st.session_state.authenticated = True
                            st.rerun()
                        else:
                            st.error("❌ Token invalid.")
                    else:
                        registered_device = str(match.iloc[0]['DeviceID']).strip()
                        if registered_device in ["", "nan", "None"]:
                            tokens_df.loc[tokens_df['Token'] == token, 'DeviceID'] = device_id
                            conn.update(worksheet="Sheet1", data=tokens_df)
                            st.session_state.authenticated = True
                            st.balloons()
                            st.rerun()
                        elif registered_device != device_id:
                            st.error("🚫 Used on another device.")
                        else:
                            st.session_state.authenticated = True
                            st.rerun()
                except Exception as e:
                    if token == "ADMIN2024":
                        st.session_state.authenticated = True
                        st.rerun()
                    else:
                        st.error("Connection Error. Check your Sheet settings.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.stop() # Prevents loading data until auth is done

# --- 3. DATA ENGINE ---
@st.cache_data(ttl=300)
def load_questions():
    URL = "https://raw.githubusercontent.com/Imoter2233/Med_store/main/questions.csv"
    try:
        df = pd.read_csv(URL)
        df['year'] = df['year'].astype(str)
        return df
    except:
        return pd.DataFrame()

# --- 4. MAIN APP ---
security_check() # Handles login UI
df = load_questions()

if not df.empty:
    st.markdown("<h1 style='text-align:center; color:#4C51BF;'>Synapse Ultimate</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; opacity:0.6;'>Professional Past Questions Engine</p>", unsafe_allow_html=True)

    # SIDEBAR FILTERS
    st.sidebar.button("🔓 Log Out", on_click=lambda: st.session_state.update({"authenticated": False}))
    st.sidebar.divider()
    
    courses = sorted(df['course_code'].unique())
    f_course = st.sidebar.multiselect("Select Course", courses)

    years = sorted(df['year'].unique(), reverse=True)
    f_year = st.sidebar.multiselect("Select Year", years)

    topics = sorted(df['topic'].unique())
    f_topic = st.sidebar.multiselect("Select Topic", topics)

    # Filter Application
    filtered = df
    if f_course: filtered = filtered[filtered['course_code'].isin(f_course)]
    if f_year: filtered = filtered[filtered['year'].isin(f_year)]
    if f_topic: filtered = filtered[filtered['topic'].isin(f_topic)]

    # SEARCH
    search = st.text_input("🔍 Search database...", placeholder="Search keywords...")
    if search:
        filtered = filtered[filtered['q'].str.contains(search, case=False, na=False) | filtered['topic'].str.contains(search, case=False, na=False)]

    # PAGINATION
    limit = 10
    total = len(filtered)
    pages = (total // limit) + (1 if total % limit > 0 else 0)

    if total > 0:
        c1, c2 = st.columns([1, 2])
        with c1:
            curr_page = st.number_input("Page", min_value=1, max_value=max(1, pages), step=1)
        with c2:
            st.markdown(f"<br><small>Showing {len(filtered.iloc[(curr_page-1)*limit : curr_page*limit])} of {total} items</small>", unsafe_allow_html=True)

        for _, row in filtered.iloc[(curr_page-1)*limit : curr_page*limit].iterrows():
            render_question_card(row)
            with st.expander("📖 View Answer & Explanation"):
                st.success(f"**Correct Answer: {row['ans']}**")
                st.write(row['exp'])
    else:
        st.warning("No questions match your selection.")
else:
    st.error("The library is empty. Please check your GitHub CSV link.")
