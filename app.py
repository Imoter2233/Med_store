import streamlit as st
import sqlite3
import os
from datetime import datetime

# --- SET PAGE CONFIG ---
st.set_page_config(page_title="MedLib Pro", layout="wide", page_icon="💊")

# Ensure upload directory exists
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# --- DATABASE ---
def get_db():
    conn = sqlite3.connect("medstore.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

db = get_db()
db.execute('''CREATE TABLE IF NOT EXISTS medbooks 
             (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, cat TEXT, img TEXT, pdf TEXT)''')
db.commit()

# --- PROFESSIONAL CSS (JUMIA / MODERN LOOK) ---
st.markdown("""
    <style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
    }

    /* Main background */
    .stApp {
        background-color: #f8f9fa;
    }

    /* Custom Header */
    .header-box {
        background: linear-gradient(90deg, #2c3e50, #4ca1af);
        padding: 40px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }

    /* Jumia-Style Card */
    .book-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        transition: transform 0.3s ease;
        border: 1px solid #eee;
        text-align: center;
        margin-bottom: 25px;
    }
    
    .book-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 12px 30px rgba(0,0,0,0.1);
        border-color: #4ca1af;
    }

    /* Category Badge */
    .badge {
        background: #e1f5fe;
        color: #039be5;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 10px;
        display: inline-block;
    }

    /* Download Button Styling */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #e67e22, #d35400) !important;
        color: white !important;
        border: none !important;
        padding: 10px 20px !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        width: 100% !important;
    }

    /* Carousel Image effect */
    .carousel-img {
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }

    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ADMIN ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/387/387561.png", width=100)
    st.title("Admin Portal")
    pw = st.text_input("Enter Secret Code", type="password")
    is_admin = (pw == "MED777")

    if is_admin:
        st.success("Authorized")
        with st.expander("➕ Add New Resource", expanded=True):
            t = st.text_input("Textbook Name")
            c = st.selectbox("Category", ["Anatomy", "Physiology", "Surgery", "Pharmacology", "Internal Medicine"])
            img_f = st.file_uploader("Cover Image", type=['jpg','png','jpeg'])
            pdf_f = st.file_uploader("PDF File", type=['pdf'])
            
            if st.button("🚀 Upload Now"):
                if t and img_f and pdf_f:
                    with st.status("Uploading...", expanded=True) as s:
                        img_path = os.path.join("uploads", img_f.name)
                        pdf_path = os.path.join("uploads", pdf_f.name)
                        with open(img_path, "wb") as f: f.write(img_f.getbuffer())
                        with open(pdf_path, "wb") as f: f.write(pdf_f.getbuffer())
                        db.execute("INSERT INTO medbooks (title, cat, img, pdf) VALUES (?,?,?,?)", (t, c, img_path, pdf_path))
                        db.commit()
                        s.update(label="Published!", state="complete")
                    st.rerun()

# --- MAIN APP INTERFACE ---
st.markdown("""
    <div class="header-box">
        <h1>🏥 Medical Hub</h1>
        <p>Premium Medical Textbooks for Future Doctors</p>
    </div>
    """, unsafe_allow_html=True)

# Fetch Data
cursor = db.execute("SELECT * FROM medbooks ORDER BY id DESC")
books = cursor.fetchall()

# 1. TOP CAROUSEL (The Jumia Top Banner)
if books:
    st.markdown("### 🔥 Trending This Week")
    top_items = books[:4]
    cols = st.columns(len(top_items))
    for i, book in enumerate(top_items):
        with cols[i]:
            st.image(book['img'], use_container_width=True)
            st.markdown(f"<center><small>{book['title']}</small></center>", unsafe_allow_html=True)

st.write("---")

# 2. SEARCH & FILTER
c1, c2 = st.columns([3, 1])
with c1:
    search = st.text_input("🔍 Find your textbook...", placeholder="Search for 'Gray's' or 'Guyton'...")
with c2:
    cat_filter = st.selectbox("Filter", ["All", "Anatomy", "Physiology", "Surgery", "Pharmacology", "Internal Medicine"])

# 3. THE PROFESSIONAL GRID
if not books:
    st.info("The library is being prepared. Check back shortly!")
else:
    # Logic for search and category filter
    display_books = books
    if search:
        display_books = [b for b in display_books if search.lower() in b['title'].lower()]
    if cat_filter != "All":
        display_books = [b for b in display_books if b['cat'] == cat_filter]

    # Display in Grid
    for i in range(0, len(display_books), 3):
        row_cols = st.columns(3)
        for j, book in enumerate(display_books[i:i+3]):
            with row_cols[j]:
                # Card Container
                st.markdown(f"""
                    <div class="book-card">
                        <div class="badge">{book['cat']}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                st.image(book['img'], use_container_width=True)
                st.markdown(f"**{book['title']}**")
                
                # Download Button
                try:
                    with open(book['pdf'], "rb") as f:
                        st.download_button(
                            label="📥 Download PDF",
                            data=f,
                            file_name=f"{book['title']}.pdf",
                            key=f"btn_{book['id']}"
                        )
                except:
                    st.error("File error")
                
                st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br><br><center><p style='color: #999;'>© 2024 MedLib Pro • Built for Medical Students</p></center>", unsafe_allow_html=True)
