import streamlit as st
from PIL import Image, ImageDraw, ImageEnhance, ImageOps
import io
import zipfile
import textwrap
import os

st.set_page_config(
    page_title="CV PIONEERING TESTIMONIES",
    page_icon="✝️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium Styling - Dark Emerald Gradient Look & Feel
st.markdown("""
<style>
    /* Dark background with subtle green glow/fade */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(16, 44, 32, 0.95) 0%, rgba(10, 15, 13, 0.98) 90%);
        color: #e0e6e3;
        font-family: 'Inter', sans-serif;
    }
    
    /* Header branding styling */
    .brand-header {
        display: flex;
        align-items: center;
        gap: 20px;
        padding-bottom: 1rem;
        border-bottom: 1px solid rgba(46, 204, 113, 0.2);
        margin-bottom: 2rem;
    }
    .brand-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: 2px;
        background: linear-gradient(135deg, #ffffff 30%, #2ecc71 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    
    /* Custom Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(14, 23, 19, 0.95) !important;
        border-right: 1px solid rgba(46, 204, 113, 0.2);
    }
    
    /* Input field styling */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(10, 18, 14, 0.8) !important;
        color: #f0f4f2 !important;
        border: 1px solid rgba(46, 204, 113, 0.3) !important;
        border-radius: 8px !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #2ecc71 !important;
        box-shadow: 0 0 10px rgba(46, 204, 113, 0.3) !important;
    }
    
    /* Custom Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #1e7e48 0%, #114e2b 100%);
        color: white;
        border: 1px solid #2ecc71;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #27ae60 0%, #1e7e48 100%);
        box-shadow: 0 0 15px rgba(46, 204, 113, 0.5);
        color: white;
        border-color: #58d68d;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(20, 32, 26, 0.5);
        border-radius: 6px;
        color: #a0b2a8;
        padding: 8px 16px;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(46, 204, 113, 0.2) !important;
        color: #2ecc71 !important;
        border-bottom: 2px solid #2ecc71 !important;
    }
</style>
""", unsafe_allow_html=True)

# Top Bar with Logo and Premium Title
top_col1, top_col2 = st.columns([1, 5])
with top_col1:
    # Check relative path & script dir path to ensure logo is found
    script_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(script_dir, "assets", "logo.png")
    
    if not os.path.exists(logo_path):
        logo_path = os.path.join("assets", "logo.png")
        
    if os.path.exists(logo_path):
        try:
            logo_img = Image.open(logo_path).convert("RGBA")
            # Invert black logo pixels to crisp white for dark UI
            datas = logo_img.getdata()
            newData = []
            for item in datas:
                # If pixel is dark (black logo mark), turn it to bright white/emerald tint
                if item[0] < 100 and item[1] < 100 and item[2] < 100 and item[3] > 30:
                    newData.append((255, 255, 255, item[3]))
                else:
                    newData.append(item)
            logo_img.putdata(newData)
            st.image(logo_img, width=170)
        except Exception:
            st.image(logo_path, width=170)
    else:
        st.markdown("### **[ CV LOGO ]**")

with top_col2:
    st.markdown('<div class="brand-header"><h1 class="brand-title">CV PIONEERING TESTIMONIES</h1></div>', unsafe_allow_html=True)

# Sidebar Design & Advanced User Controls
st.sidebar.header("⚙️ Design & Formatting Settings")

design_theme = st.sidebar.selectbox("Color Theme", ["Emerald Gold (Signature)", "Deep Dark Emerald", "Warm Sunrise", "Midnight Navy"])

PALETTES = {
    "Emerald Gold (Signature)": {
        "bg": (12, 22, 17),
        "primary": (46, 204, 113),
        "text": (245, 247, 246),
        "accent": (212, 175, 55),
        "overlay": (10, 18, 14, 180)
    },
    "Deep Dark Emerald": {
        "bg": (8, 14, 11),
        "primary": (39, 174, 96),
        "text": (230, 235, 232),
        "accent": (52, 152, 219),
        "overlay": (5, 10, 8, 200)
    },
    "Warm Sunrise": {
        "bg": (25, 20, 18),
        "primary": (230, 126, 34),
        "text": (250, 245, 240),
        "accent": (241, 196, 15),
        "overlay": (20, 15, 12, 170)
    },
    "Midnight Navy": {
        "bg": (15, 23, 36),
        "primary": (52, 152, 219),
        "text": (240, 244, 248),
        "accent": (155, 89, 182),
        "overlay": (10, 15, 25, 180)
    }
}
palette = PALETTES[design_theme]

st.sidebar.markdown("---")
st.sidebar.subheader("🔤 Typography & Font Controls")
title_font_size = st.sidebar.slider("Title Font Size", min_value=36, max_value=80, value=58, step=2)
body_font_size = st.sidebar.slider("Body Text Font Size", min_value=24, max_value=60, value=42, step=2)

st.sidebar.markdown("---")
st.sidebar.subheader("🖼️ Image Adjustments")
img_brightness = st.sidebar.slider("Image Brightness", min_value=0.2, max_value=1.8, value=0.8, step=0.05)
img_overlay_opacity = st.sidebar.slider("Dark Overlay Opacity", min_value=50, max_value=240, value=170, step=10)

if "num_slides" not in st.session_state:
    st.session_state.num_slides = 4

col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.subheader("1. Mission Metadata")
    ministry_name = st.text_input("Ministry / Field Location", "CV Gospel Pioneer Team - Northern Field")
    cover_title = st.text_input("Testimony Cover Title", "Light Shines in the Remote Village of Kalugala")
    cover_verse = st.text_input("Key Scripture / Tagline", "Isaiah 52:7 - 'How beautiful on the mountains...'")

    st.subheader("2. Carousel Content (Dynamic Slides)")
    
    slide_texts = []
    for i in range(st.session_state.num_slides):
        default_val = f"Slide {i+1} Content: Add testimony details, prayer needs, or outcomes here."
        if i == 0:
            default_val = "For over 20 years, no church existed in Kalugala. The community faced spiritual isolation and poverty."
        elif i == 1:
            default_val = "Our pioneering team walked 14km through mountain trails to share the Gospel and pray with families."
        elif i == 2:
            default_val = "3 families surrendered their lives to Christ! A vibrant new house fellowship was established with 15 believers."
        elif i == 3:
            default_val = "Pray for Pastor David as he disciples new believers. Partner with CV to reach 5 more unreached villages!"

        st_text = st.text_area(f"Slide {i+1} Text", value=default_val, height=85, key=f"slide_v4_{i}")
        slide_texts.append(st_text)

    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("➕ Add New Slide"):
            st.session_state.num_slides += 1
            st.rerun()
    with btn_col2:
        if st.button("➖ Remove Last Slide") and st.session_state.num_slides > 1:
            st.session_state.num_slides -= 1
            st.rerun()

    st.subheader("3. Mission Field Photos")
    uploaded_files = st.file_uploader("Upload photos for background (PNG / JPG)", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

def create_slide_v4(text, title_str, verse_str, bg_img, palette, slide_num, total_slides, is_title=False):
    size = (1080, 1080)
    img = Image.new("RGB", size, palette["bg"])
    
    if bg_img:
        bg_proc = bg_img.convert("RGBA")
        
        enhancer = ImageEnhance.Brightness(bg_proc)
        bg_proc = enhancer.enhance(img_brightness)
        
        aspect = bg_proc.width / bg_proc.height
        if aspect > 1.0:
            new_h = 1080
            new_w = int(1080 * aspect)
        else:
            new_w = 1080
            new_h = int(1080 / aspect)
            
        bg_proc = bg_proc.resize((new_w, new_h), Image.Resampling.LANCZOS)
        left = (new_w - 1080) // 2
        top = (new_h - 1080) // 2
        bg_proc = bg_proc.crop((left, top, left + 1080, top + 1080))
        
        overlay_color = (palette["overlay"][0], palette["overlay"][1], palette["overlay"][2], img_overlay_opacity)
        overlay = Image.new("RGBA", size, overlay_color)
        img.paste(bg_proc, (0, 0))
        img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")

    draw = ImageDraw.Draw(img)
    
    # Premium Header Bar
    draw.text((60, 60), ministry_name.upper(), fill=palette["primary"], font_size=26)
    draw.line([(60, 105), (1020, 105)], fill=palette["accent"], width=3)
    
    if is_title:
        wrapped_title = textwrap.fill(title_str, width=22)
        draw.text((60, 320), wrapped_title, fill=palette["text"] if not bg_img else (255, 255, 255), font_size=title_font_size)
        
        wrapped_verse = textwrap.fill(verse_str, width=35)
        draw.text((60, 760), wrapped_verse, fill=palette["accent"], font_size=32)
    else:
        wrapped_text = textwrap.fill(text, width=28)
        draw.text((80, 380), wrapped_text, fill=palette["text"] if not bg_img else (255, 255, 255), font_size=body_font_size)
        
    # Premium Footer Navigation
    draw.text((60, 980), f"CV PIONEERING TESTIMONY ({slide_num}/{total_slides})", fill=(160, 175, 168), font_size=22)
    if slide_num < total_slides:
        draw.text((850, 980), "SWIPE ➡️", fill=palette["primary"], font_size=24)
    else:
        draw.text((850, 980), "AMEN 🙏", fill=palette["accent"], font_size=24)
    
    return img

with col_right:
    st.subheader("🖼️ Live Preview & High-Res Export")
    
    all_slides = [{"text": "", "is_title": True}] + [{"text": txt, "is_title": False} for txt in slide_texts]
    total_count = len(all_slides)
    
    generated_images = []
    
    for idx, slide_info in enumerate(all_slides):
        bg_photo = None
        if uploaded_files and idx < len(uploaded_files):
            bg_photo = Image.open(uploaded_files[idx])
        elif uploaded_files:
            bg_photo = Image.open(uploaded_files[0])
            
        card_img = create_slide_v4(
            text=slide_info["text"],
            title_str=cover_title,
            verse_str=cover_verse,
            bg_img=bg_photo,
            palette=palette,
            slide_num=idx+1,
            total_slides=total_count,
            is_title=slide_info["is_title"]
        )
        generated_images.append(card_img)
        
    tabs = st.tabs([f"Cover" if i==0 else f"Slide {i}" for i in range(len(generated_images))])
    for i, tab in enumerate(tabs):
        with tab:
            st.image(generated_images[i], caption=f"Slide {i+1} Preview (1080x1080)", use_container_width=True)
            
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for idx, img in enumerate(generated_images):
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            fname = "00_cover.png" if idx == 0 else f"slide_{idx}.png"
            zip_file.writestr(fname, img_byte_arr.getvalue())
            
    st.download_button(
        label=f"📥 Download All {total_count} Carousel Slides (.ZIP)",
        data=zip_buffer.getvalue(),
        file_name="cv_pioneering_testimony_carousel.zip",
        mime="application/zip",
        use_container_width=True
    )
