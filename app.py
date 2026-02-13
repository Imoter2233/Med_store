import streamlit as st
import sqlite3
import os
from datetime import datetime

# --- CONFIG ---
st.set_page_config(page_title="MedLib Live", layout="wide", page_icon="💊")

# Ensure upload directory exists
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# Database setup (Persistent only while app is running)
def get_db():
    conn = sqlite3.connect("medstore.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

db = get_db()
db.execute('''CREATE TABLE IF NOT EXISTS medbooks 
             (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, cat TEXT, img TEXT, pdf TEXT)''')
db.commit()

# --- STYLING ---
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #f4f7f9; }
    .main-title { color: #2c3e50; font-size: 40px; font-weight: bold; text-align: center; margin-bottom: 10px; }
    .jumia-card {
        background: white; padding: 15px; border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08); text-align: center;
        border-bottom: 4px solid #e67e22; height: 100%;
    }
    .carousel-box {
        display: flex; overflow-x: auto; gap: 20px; padding: 20px 0;
        scrollbar-width: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ADMIN ---
st.sidebar.header("🔐 Staff Only")
pw = st.sidebar.text_input("Enter Secret Code", type="password")
is_admin = (pw == "MED777") # Your secret key

if is_admin:
    st.sidebar.success("Admin Verified")
    with st.sidebar.expander("➕ Add New Textbook", expanded=True):
        t = st.text_input("Book Name")
        c = st.selectbox("Category", ["Anatomy", "Surgery", "Pathology", "Nursing"])
        img_f = st.file_uploader("Cover Image", type=['jpg','png','jpeg'])
        pdf_f = st.file_uploader("PDF File", type=['pdf'])
        
        if st.button("🚀 Upload & Publish"):
            if t and img_f and pdf_f:
                with st.status("Uploading to Server...", expanded=True) as s:
                    # Save files
                    img_path = os.path.join("uploads", img_f.name)
                    pdf_path = os.path.join("uploads", pdf_f.name)
                    with open(img_path, "wb") as f: f.write(img_f.getbuffer())
                    s.write("✅ Image Processed...")
                    with open(pdf_path, "wb") as f: f.write(pdf_f.getbuffer())
                    s.write("✅ PDF Uploaded...")
                    
                    db.execute("INSERT INTO medbooks (title, cat, img, pdf) VALUES (?,?,?,?)", (t, c, img_path, pdf_path))
                    db.commit()
                    s.update(label="Library Updated!", state="complete")
                st.rerun()

# --- MAIN UI ---
st.markdown('<p class="main-title">Medical Textbook Hub</p>', unsafe_allow_html=True)

# Fetch Data
cursor = db.execute("SELECT * FROM medbooks ORDER BY id DESC")
books = cursor.fetchall()

# 1. TOP CAROUSEL (Jumia Look)
if books:
    st.subheader("🌟 Featured Resources")
    # Horizontal scroll simulation using columns
    top_five = books[:5]
    cols = st.columns(len(top_five))
    for i, book in enumerate(top_five):
        with cols[i]:
            st.image(book['img'], use_container_width=True)
            st.caption(book['title'])

st.divider()

# 2. SEARCHBAR
search = st.text_input("🔍 Search over 1,000+ textbooks...", placeholder="Type 'Anatomy' or 'Gray'...")

# 3. THE GRID
if not books:
    st.info("The library is currently being stocked. Check back in 5 mins!")
else:
    # Filtering
    display_books = [b for b in books if search.lower() in b['title'].lower()] if search else books
    
    # Create rows of 3
    for i in range(0, len(display_books), 3):
        cols = st.columns(3)
        for j, book in enumerate(display_books[i:i+3]):
            with cols[j]:
                st.markdown(f'<div class="jumia-card">', unsafe_allow_html=True)
                st.image(book['img'], use_container_width=True)
                st.markdown(f"**{book['title']}**")
                st.markdown(f"<small>{book['cat']}</small>", unsafe_allow_html=True)
                
                with open(book['pdf'], "rb") as f:
                    st.download_button("📥 Download", f, file_name=f"{book['title']}.pdf", key=f"dl_{book['id']}")
                st.markdown('</div>', unsafe_allow_html=True)
                st.write("") # Spacer

st.markdown("<br><hr><center>Managed by Medical Dept. © 2024</center>", unsafe_allow_html=True)
