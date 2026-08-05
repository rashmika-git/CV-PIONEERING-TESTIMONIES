import streamlit as st
from PIL import Image
import os

st.set_page_config(
    page_title="CV PIONEERING TESTIMONIES",
    page_icon="✝️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(16, 44, 32, 0.95) 0%, rgba(10, 15, 13, 0.98) 90%);
        color: #e0e6e3;
        font-family: 'Inter', sans-serif;
    }
    .brand-title {
        font-size: clamp(1.4rem, 4vw, 2.2rem);
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 30%, #2ecc71 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar - Logo Uploader
st.sidebar.header("🖼️ Branding & Logo")
logo_upload = st.sidebar.file_uploader("Upload Logo (PNG/JPG)", type=["png", "jpg", "jpeg"])

top_col1, top_col2 = st.columns([1, 4])

logo_img = None
script_dir = os.path.dirname(os.path.abspath(__file__))
default_logo_path = os.path.join(script_dir, "assets", "logo.png")

if logo_upload is not None:
    try:
        logo_img = Image.open(logo_upload)
    except Exception:
        st.sidebar.error("Error loading uploaded image.")
elif os.path.exists(default_logo_path):
    try:
        logo_img = Image.open(default_logo_path)
    except Exception:
        pass

with top_col1:
    if logo_img is not None:
        try:
            proc_logo = logo_img.convert("RGBA")
            datas = proc_logo.getdata()
            newData = []
            for item in datas:
                if item[0] < 120 and item[1] < 120 and item[2] < 120 and item[3] > 30:
                    newData.append((255, 255, 255, item[3]))
                else:
                    newData.append(item)
            proc_logo.putdata(newData)
            st.image(proc_logo, use_container_width=True)
        except Exception:
            st.image(logo_img, use_container_width=True)
    else:
        st.info("💡 Upload Logo from Sidebar")

with top_col2:
    st.markdown('<h1 class="brand-title">CV PIONEERING TESTIMONIES</h1>', unsafe_allow_html=True)

st.success("App deployed successfully! Ready to design testimonies.")
