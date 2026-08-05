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

# Safe Local Font Loader Function
def load_font(size):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(script_dir, "Roboto-Bold.ttf")
    
    if os.path.exists(font_path):
        return ImageFont.truetype(font_path, size)
    else:
        # Fallback if file not found in github
        return ImageFont.load_default()

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
st.sidebar.header("🖼️ Branding & Logo")
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

# Check Font Availability Alert
font_check_path = os.path.join(script_dir, "Roboto-Bold.ttf")
if not os.path.exists(font_check_path):
    st.warning("⚠️ 'Roboto-Bold.ttf' font file එක GitHub එකට upload කර නොමැති නිසා Font Size වෙනස් කිරීම සීමා වී ඇත. කරුණාකර Roboto-Bold.ttf file එක repository එකට upload කරන්න.")

# --- Global Settings Sidebar ---
st.sidebar.markdown("---")
st.sidebar.header("🎨 Full Design Customizer")

# Typography Controls
st.sidebar.subheader("✍️ Typography Settings")
title_font_size = st.sidebar.slider("Title Font Size", 30, 110, 65)
text_font_size = st.sidebar.slider("Body Text Font Size", 18, 70, 36)
text_align = st.sidebar.selectbox("Text Alignment", ["left", "center", "right"])

title_y_pos = st.sidebar.slider("Title Y Position", 150, 400, 220)
body_y_pos = st.sidebar.slider("Body Text Y Position", 400, 800, 520)

# Color Controls
st.sidebar.subheader("🎨 Color Settings")
title_color = st.sidebar.color_picker("Title Color", "#2ECC71")
body_color = st.sidebar.color_picker("Body Text Color", "#FFFFFF")
line_color = st.sidebar.color_picker("Bottom Accent Line Color", "#2ECC71")

# Layout & Branding Controls
st.sidebar.subheader("📐 Element Sizes & Overlays")
logo_scale = st.sidebar.slider("Logo Size", 100, 400, 240)
overlay_opacity = st.sidebar.slider("Dark Overlay Opacity", 0.0, 0.95, 0.45, 0.05)
line_thickness = st.sidebar.slider("Accent Line Thickness", 2, 20, 6)

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

    # Dark Overlay
    overlay = Image.new("RGBA", (img_width, img_height), (0, 0, 0, int(255 * overlay_opacity)))
    canvas = Image.alpha_composite(bg_image, overlay)
    draw = ImageDraw.Draw(canvas)

    # Logo Display
    if logo is not None:
        try:
            l_img = make_logo_white(logo)
            l_img.thumbnail((logo_scale, int(logo_scale * 0.5)), Image.Resampling.LANCZOS)
            canvas.paste(l_img, (60, 60), l_img)
        except Exception:
            pass

    # Load Fonts using local loader
    title_font = load_font(title_font_size)
    body_font = load_font(text_font_size)

    # Dynamic Auto Wrap Calculation
    wrap_width_title = max(10, int(9500 / title_font_size))
    wrap_width_body = max(15, int(11000 / text_font_size))

    title_text = slide["title"].upper()
    wrapped_title = textwrap.fill(title_text, width=wrap_width_title)

    content_text = slide["content"]
    wrapped_content = textwrap.fill(content_text, width=wrap_width_body)

    # Precise X-Positioning
    if text_align == "center":
        x_pos = 540
    elif text_align == "right":
        x_pos = 1020
    else:
        x_pos = 60

    # Draw Text
    draw.multiline_text((x_pos, title_y_pos), wrapped_title, fill=title_color, font=title_font, spacing=12, align=text_align)
    draw.multiline_text((x_pos, body_y_pos), wrapped_content, fill=body_color, font=body_font, spacing=16, align=text_align)

    # Bottom Line Accent
    line_y = 1020
    draw.rectangle([60, line_y - line_thickness, 1020, line_y], fill=line_color)

    return canvas.convert("RGB")

# --- Main Editor & Live Preview Grid ---
col_edit, col_preview = st.columns([1, 1])

generated_images = []

with col_edit:
    st.subheader("✏️ Edit Content & Images")
    for idx, slide in enumerate(st.session_state.slides):
        with st.expander(f"📌 Slide {idx + 1}: {slide['title'][:20]}", expanded=(idx == 0)):
            slide["title"] = st.text_input(f"Title #{idx+1}", value=slide["title"], key=f"title_{idx}")
            slide["content"] = st.text_area(f"Story Text #{idx+1}", value=slide["content"], height=120, key=f"content_{idx}")
            
            img_file = st.file_uploader(f"Upload Background Image #{idx+1}", type=["jpg", "png", "jpeg"], key=f"img_{idx}")
            if img_file is not None:
                slide["image"] = img_file
                
            slide["brightness"] = st.slider(f"Image Brightness #{idx+1}", 0.2, 1.8, float(slide["brightness"]), 0.1, key=f"bright_{idx}")

with col_preview:
    st.subheader("👁️ Live Interactive Preview")
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
