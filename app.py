import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps
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

# Custom Styling
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(16, 44, 32, 0.95) 0%, rgba(10, 15, 13, 0.98) 90%);
        color: #e0e6e3;
        font-family: 'Inter', sans-serif;
    }
    .brand-header {
        display: flex;
        align-items: center;
        gap: 15px;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(46, 204, 113, 0.2);
        margin-bottom: 1.5rem;
        flex-wrap: wrap;
    }
    .brand-title {
        font-size: clamp(1.4rem, 4vw, 2.2rem);
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 30%, #2ecc71 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    section[data-testid="stSidebar"] {
        background-color: rgba(14, 23, 19, 0.95) !important;
        border-right: 1px solid rgba(46, 204, 113, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Helper function to convert black logo to white safely
def make_logo_white(img):
    try:
        img = img.convert("RGBA")
        r, g, b, a = img.split()
        rgb_image = Image.merge('RGB', (r, g, b))
        inverted_image = ImageOps.invert(rgb_image)
        r2, g2, b2 = inverted_image.split()
        return Image.merge('RGBA', (r2, g2, b2, a))
    except Exception:
        return img

# Logo Handling
st.sidebar.header("🖼️ Branding Settings")
logo_upload = st.sidebar.file_uploader("Upload Logo (PNG)", type=["png", "jpg", "jpeg"])

top_col1, top_col2 = st.columns([1, 4])

logo_img = None
script_dir = os.path.dirname(os.path.abspath(__file__))
default_logo_path = os.path.join(script_dir, "assets", "logo.png")

if logo_upload is not None:
    try:
        logo_img = Image.open(logo_upload)
    except Exception:
        pass
elif os.path.exists(default_logo_path):
    try:
        logo_img = Image.open(default_logo_path)
    except Exception:
        pass

with top_col1:
    if logo_img is not None:
        try:
            proc_logo = make_logo_white(logo_img)
            st.image(proc_logo, width=180)
        except Exception:
            st.image(logo_img, width=180)

with top_col2:
    st.markdown('<div class="brand-header"><h1 class="brand-title">CV PIONEERING TESTIMONIES</h1></div>', unsafe_allow_html=True)

# --- Global Settings Sidebar ---
st.sidebar.markdown("---")
st.sidebar.header("🎨 Styling & Design Options")
title_font_size = st.sidebar.slider("Title Font Size", 30, 90, 55)
text_font_size = st.sidebar.slider("Body Text Font Size", 18, 50, 28)
overlay_opacity = st.sidebar.slider("Dark Overlay Opacity", 0.0, 0.9, 0.45, 0.05)

# Session State for Slides
if "slides" not in st.session_state:
    st.session_state.slides = [
        {
            "title": "FAITH IN ACTION",
            "content": "Every testimony is a footprint of God's grace pioneering into new hearts and territories.",
            "image": None,
            "brightness": 1.0
        }
    ]

# Manage Slides
st.sidebar.markdown("---")
st.sidebar.header("📑 Manage Carousel Slides")

if st.sidebar.button("➕ Add New Slide"):
    st.session_state.slides.append({
        "title": f"SLIDE {len(st.session_state.slides) + 1}",
        "content": "Enter your story or testimony details here...",
        "image": None,
        "brightness": 1.0
    })

if len(st.session_state.slides) > 1:
    if st.sidebar.button("🗑️ Remove Last Slide"):
        st.session_state.slides.pop()

# --- Image Generation Logic ---
def create_slide_image(slide, logo):
    img_width, img_height = 1080, 1080
    
    if slide["image"] is not None:
        try:
            bg_image = Image.open(slide["image"]).convert("RGBA")
            bg_image = ImageOps.fit(bg_image, (img_width, img_height), Image.Resampling.LANCZOS)
            enhancer = ImageEnhance.Brightness(bg_image)
            bg_image = enhancer.enhance(slide["brightness"])
        except Exception:
            bg_image = Image.new("RGBA", (img_width, img_height), (14, 23, 19, 255))
    else:
        bg_image = Image.new("RGBA", (img_width, img_height), (14, 23, 19, 255))

    overlay = Image.new("RGBA", (img_width, img_height), (0, 0, 0, int(255 * overlay_opacity)))
    canvas = Image.alpha_composite(bg_image, overlay)
    draw = ImageDraw.Draw(canvas)

    if logo is not None:
        try:
            l_img = make_logo_white(logo)
            l_img.thumbnail((220, 90), Image.Resampling.LANCZOS)
            canvas.paste(l_img, (60, 60), l_img)
        except Exception:
            pass

    try:
        title_font = ImageFont.truetype("arial.ttf", title_font_size)
        body_font = ImageFont.truetype("arial.ttf", text_font_size)
    except Exception:
        title_font = ImageFont.load_default()
        body_font = ImageFont.load_default()

    title_text = slide["title"].upper()
    wrapped_title = textwrap.fill(title_text, width=22)
    draw.multiline_text((60, 220), wrapped_title, fill="#2ECC71", font=title_font, spacing=10)

    content_text = slide["content"]
    wrapped_content = textwrap.fill(content_text, width=38)
    draw.multiline_text((60, 520), wrapped_content, fill="#FFFFFF", font=body_font, spacing=12)

    draw.rectangle([60, 1000, 1020, 1006], fill="#2ECC71")

    return canvas.convert("RGB")

# --- Main Editor & Preview Grid ---
col_edit, col_preview = st.columns([1, 1])

generated_images = []

with col_edit:
    st.subheader("✏️ Edit Content & Backgrounds")
    for idx, slide in enumerate(st.session_state.slides):
        with st.expander(f"📌 Slide {idx + 1}: {slide['title'][:20]}", expanded=(idx == 0)):
            slide["title"] = st.text_input(f"Title #{idx+1}", value=slide["title"], key=f"title_{idx}")
            slide["content"] = st.text_area(f"Story Text #{idx+1}", value=slide["content"], height=110, key=f"content_{idx}")
            
            img_file = st.file_uploader(f"Upload Image #{idx+1}", type=["jpg", "png", "jpeg"], key=f"img_{idx}")
            if img_file is not None:
                slide["image"] = img_file
                
            slide["brightness"] = st.slider(f"Image Brightness #{idx+1}", 0.2, 1.8, float(slide["brightness"]), 0.1, key=f"bright_{idx}")

with col_preview:
    st.subheader("👁️ Live Preview")
    for idx, slide in enumerate(st.session_state.slides):
        slide_img = create_slide_image(slide, logo_img)
        generated_images.append((f"slide_{idx+1}.png", slide_img))
        st.image(slide_img, caption=f"Slide {idx+1} Preview")

# --- Download Section ---
st.markdown("---")
st.subheader("📥 Export & Download Options")

if len(generated_images) == 1:
    buf = io.BytesIO()
    generated_images[0][1].save(buf, format="PNG")
    st.download_button(
        label="💾 Download Single Slide (PNG)",
        data=buf.getvalue(),
        file_name="pioneering_testimony.png",
        mime="image/png"
    )
else:
    zip_buf = io.BytesIO()
    with zipfile.ZipFile(zip_buf, "w") as zip_file:
        for fname, img in generated_images:
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format="PNG")
            zip_file.writestr(fname, img_byte_arr.getvalue())
            
    st.download_button(
        label=f"📦 Download All {len(generated_images)} Slides Carousel (ZIP)",
        data=zip_buf.getvalue(),
        file_name="testimonies_carousel.zip",
        mime="application/zip"
    )
