import streamlit as st

def load_synapse_ui():
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

    .stApp { 
        background-color: var(--bg) !important; 
        color: var(--text); 
        font-family: 'Nunito', sans-serif; 
    }
    
    /* THE CENTERED LOGIN BOX */
    .login-container {
        background: var(--bg);
        padding: 40px;
        border-radius: 30px;
        box-shadow: 10px 10px 20px var(--shadow-dark), -10px -10px 20px var(--shadow-light);
        margin: 100px auto;
        max-width: 450px;
        border: 2px solid var(--primary);
        text-align: center;
    }

    .neu-card {
        background: var(--bg);
        box-shadow: 7px 7px 14px var(--shadow-dark), -7px -7px 14px var(--shadow-light);
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 25px;
    }

    div[data-baseweb="input"] {
        background-color: var(--bg) !important;
        border-radius: 10px !important;
        box-shadow: inset 4px 4px 8px var(--shadow-dark), inset -4px -4px 8px var(--shadow-light) !important;
        border: none !important;
    }

    header, footer, #MainMenu {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

def render_question_card(row):
    img_tag = f'<img src="{row["img"]}" style="width:100%; border-radius:15px; margin-bottom:15px; border:2px solid var(--primary);">' if str(row.get('img')) != 'nan' and row.get('img', '') != "" else ""
    
    st.markdown(f"""
    <div class="neu-card">
        <div style="display:flex; justify-content:space-between; font-weight:900;">
            <span style="color:var(--primary); text-transform:uppercase;">{row['course_code']}</span>
            <span style="opacity:0.5;">{row['year']} | {row['topic']}</span>
        </div>
        <div style="font-size:1.1rem; font-weight:800; margin:20px 0;">{row['q']}</div>
        {img_tag}
        <div style="padding:12px; border-radius:10px; background:rgba(0,0,0,0.02); margin-bottom:8px;">A. {row['a']}</div>
        <div style="padding:12px; border-radius:10px; background:rgba(0,0,0,0.02); margin-bottom:8px;">B. {row['b']}</div>
        <div style="padding:12px; border-radius:10px; background:rgba(0,0,0,0.02); margin-bottom:8px;">C. {row['c']}</div>
        <div style="padding:12px; border-radius:10px; background:rgba(0,0,0,0.02); margin-bottom:8px;">D. {row['d']}</div>
    </div>
    """, unsafe_allow_html=True)
