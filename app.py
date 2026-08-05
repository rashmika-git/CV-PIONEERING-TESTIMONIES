import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps
import io
import zipfile
import textwrap
import os
import urllib.request

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

# Google Fonts Collection
FONT_URLS = {
    "Roboto": "https://github.com/google/fonts/raw/main/apache/roboto/Roboto-Bold.ttf",
    "Montserrat": "https://github.com/google/fonts/raw/main/ofl/montserrat/Montserrat-Bold.ttf",
    "Oswald": "https://github.com/google/fonts/raw/main/ofl/oswald/Oswald-Bold.ttf",
    "Poppins": "https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-Bold.ttf",
    "Lora": "https://github.com/google/fonts/raw/main/ofl/lora/Lora-Bold.ttf",
    "Playfair Display": "https://github.com/google/fonts/raw/main/ofl/playfairdisplay/PlayfairDisplay-Bold.ttf"
}

# Dynamic Font Fetcher
@st.cache_resource
def get_custom_font(font_name, size):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    font_filename = f"{font_name.replace(' ', '_')}.ttf"
    font_path = os.path.join(script_dir, font_filename)
    
    if not os.path.exists(font_path) and font_name in FONT_URLS:
        try:
            urllib.request.urlretrieve(FONT_URLS[font_name], font_path)
        except Exception:
            pass

    local_default = os.path.join(script_dir, "Roboto-Bold.ttf")

    if os.path.exists(font_path):
        return ImageFont.truetype(font_path, size)
    elif os.path.exists(local_default):
        return ImageFont.truetype(local_default, size)
    else:
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

# --- Global Settings Sidebar ---
st.sidebar.markdown("---")
st.sidebar.header("🎨 Full Design Customizer")

# Typography Controls
st.sidebar.subheader("✍️ Typography Settings")
selected_font = st.sidebar.selectbox("Choose Font Style", list(FONT_URLS.keys()), index=0)
title_font_size = st.sidebar.slider("Title Font Size", 30, 110, 65)
text_font_size = st.sidebar.slider("Body Text Font Size", 18, 70, 36)
text_align = st.sidebar.selectbox("Text Alignment", ["left", "center", "right"])

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

# --- Element Position Settings (X & Y Axis) ---
st.sidebar.markdown("---")
st.sidebar.header("🎯 Precise X & Y Positioning")

element_to_move = st.sidebar.selectbox(
    "Select Element to Position", 
    ["Title Text", "Body Text", "Logo", "Accent Line"]
)

# Persistent positions using Session State or default values
if "pos_title_x" not in st.session_state: st.session_state.pos_title_x = 60
if "pos_title_y" not in st.session_state: st.session_state.pos_title_y = 220

if "pos_body_x" not in st.session_state: st.session_state.pos_body_x = 60
if "pos_body_y" not in st.session_state: st.session_state.pos_body_y = 520

if "pos_logo_x" not in st.session_state: st.session_state.pos_logo_x = 60
if "pos_logo_y" not in st.session_state: st.session_state.pos_logo_y = 60

if "pos_line_y" not in st.session_state: st.session_state.pos_line_y = 1020

# Dynamic Sliders based on selected element
if element_to_move == "Title Text":
    st.session_state.pos_title_x = st.sidebar.slider("Title X Position (Left/Right)", 0, 1000, st.session_state.pos_title_x)
    st.session_state.pos_title_y = st.sidebar.slider("Title Y Position (Top/Bottom)", 50, 900, st.session_state.pos_title_y)

elif element_to_move == "Body Text":
    st.session_state.pos_body_x = st.sidebar.slider("Body X Position (Left/Right)", 0, 1000, st.session_state.pos_body_x)
    st.session_state.pos_body_y = st.sidebar.slider("Body Y Position (Top/Bottom)", 100, 950, st.session_state.pos_body_y)

elif element_to_move == "Logo":
    st.session_state.pos_logo_x = st.sidebar.slider("Logo X Position (Left/Right)", 0, 900, st.session_state.pos_logo_x)
    st.session_state.pos_logo_y = st.sidebar.slider("Logo Y Position (Top/Bottom)", 0, 900, st.session_state.pos_logo_y)

elif element_to_move == "Accent Line":
    st.session_state.pos_line_y = st.sidebar.slider("Accent Line Y Position", 800, 1080, st.session_state.pos_line_y)

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

    # Logo Display with Custom Position
    if logo is not None:
        try:
            l_img = make_logo_white(logo)
            l_img.thumbnail((logo_scale, int(logo_scale * 0.5)), Image.Resampling.LANCZOS)
            canvas.paste(l_img, (st.session_state.pos_logo_x, st.session_state.pos_logo_y), l_img)
        except Exception:
            pass

    # Dynamic Font Loader
    title_font = get_custom_font(selected_font, title_font_size)
    body_font = get_custom_font(selected_font, text_font_size)

    # Dynamic Auto Wrap Calculation
    wrap_width_title = max(10, int(9500 / title_font_size))
    wrap_width_body = max(15, int(11000 / text_font_size))

    title_text = slide["title"].upper()
    wrapped_title = textwrap.fill(title_text, width=wrap_width_title)

    content_text = slide["content"]
    wrapped_content = textwrap.fill(content_text, width=wrap_width_body)

    # Draw Title & Body Text with Explicit X & Y Coordinates
    draw.multiline_text((st.session_state.pos_title_x, st.session_state.pos_title_y), wrapped_title, fill=title_color, font=title_font, spacing=12, align=text_align)
    draw.multiline_text((st.session_state.pos_body_x, st.session_state.pos_body_y), wrapped_content, fill=body_color, font=body_font, spacing=16, align=text_align)

    # Bottom Line Accent
    line_y = st.session_state.pos_line_y
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
