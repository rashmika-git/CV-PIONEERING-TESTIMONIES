import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps
import io
import zipfile
import textwrap
import os
import requests

st.set_page_config(
    page_title="CV PIONEERING TESTIMONIES",
    page_icon="✝️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Premium Dark Studio UI)
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(16, 44, 32, 0.95) 0%, rgba(10, 15, 13, 0.98) 90%);
        color: #e0e6e3;
        font-family: 'Inter', sans-serif;
    }
    .element-container, .stImage {
        transition: none !important;
        opacity: 1 !important;
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
    .stExpander {
        border: 1px solid rgba(46, 204, 113, 0.2) !important;
        background-color: rgba(20, 32, 26, 0.6) !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# Reliable Font Direct URLs (CDN Links)
FONT_URLS = {
    "Roboto": "https://cdn.jsdelivr.net/fontsource/fonts/roboto@latest/latin-700-normal.ttf",
    "Montserrat": "https://cdn.jsdelivr.net/fontsource/fonts/montserrat@latest/latin-700-normal.ttf",
    "Oswald": "https://cdn.jsdelivr.net/fontsource/fonts/oswald@latest/latin-700-normal.ttf",
    "Poppins": "https://cdn.jsdelivr.net/fontsource/fonts/poppins@latest/latin-700-normal.ttf",
    "Lora": "https://cdn.jsdelivr.net/fontsource/fonts/lora@latest/latin-700-normal.ttf",
    "Playfair Display": "https://cdn.jsdelivr.net/fontsource/fonts/playfair-display@latest/latin-700-normal.ttf"
}

# Network Safe Dynamic Font Fetcher
@st.cache_resource
def get_custom_font(font_name, size):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    font_filename = f"{font_name.replace(' ', '_')}.ttf"
    font_path = os.path.join(script_dir, font_filename)
    
    if not os.path.exists(font_path) and font_name in FONT_URLS:
        try:
            response = requests.get(FONT_URLS[font_name], timeout=5)
            if response.status_code == 200:
                with open(font_path, "wb") as f:
                    f.write(response.content)
        except Exception:
            pass

    local_default = os.path.join(script_dir, "Roboto-Bold.ttf")

    if os.path.exists(font_path):
        try:
            return ImageFont.truetype(font_path, size)
        except Exception:
            pass
            
    if os.path.exists(local_default):
        try:
            return ImageFont.truetype(local_default, size)
        except Exception:
            pass

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
st.sidebar.header("🖼️ Branding & Global Settings")
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
selected_font = st.sidebar.selectbox("Choose Global Font Style", list(FONT_URLS.keys()), index=0, key="cfg_font_family")

st.sidebar.markdown("---")
st.sidebar.subheader("📐 Logo & Background Overlay")
logo_scale = st.sidebar.slider("Logo Size", 100, 400, 240, key="cfg_logo_size")
pos_logo_x = st.sidebar.slider("Logo Position X", 0, 900, 60, key="pos_l_x")
pos_logo_y = st.sidebar.slider("Logo Position Y", 0, 900, 60, key="pos_l_y")
overlay_opacity = st.sidebar.slider("Dark Overlay Opacity", 0.0, 0.95, 0.45, 0.05, key="cfg_overlay")

st.sidebar.markdown("---")
st.sidebar.subheader("➖ Bottom Accent Line")
line_color = st.sidebar.color_picker("Line Color", "#2ECC71", key="cfg_line_color")
pos_line_y = st.sidebar.slider("Line Y Position", 800, 1080, 1020, key="pos_line_y")
line_thickness = st.sidebar.slider("Line Thickness", 2, 20, 6, key="cfg_line_thick")

# Initial Slide Structure with Per-Element Custom Settings
if "slides" not in st.session_state:
    st.session_state.slides = [
        {
            "title": "FAITH IN ACTION",
            "title_size": 65,
            "title_color": "#2ECC71",
            "title_x": 60,
            "title_y": 220,
            "content": "Every testimony is a footprint of God's grace pioneering into new hearts and territories.",
            "content_size": 36,
            "content_color": "#FFFFFF",
            "content_x": 60,
            "content_y": 520,
            "text_align": "left",
            "image": None,
            "brightness": 1.0
        }
    ]

# Manage Slides Sidebar Controls
st.sidebar.markdown("---")
st.sidebar.header("📑 Carousel Slides")

if st.sidebar.button("➕ Add New Slide"):
    st.session_state.slides.append({
        "title": f"SLIDE {len(st.session_state.slides) + 1}",
        "title_size": 65,
        "title_color": "#2ECC71",
        "title_x": 60,
        "title_y": 220,
        "content": "Enter your story or testimony details here...",
        "content_size": 36,
        "content_color": "#FFFFFF",
        "content_x": 60,
        "content_y": 520,
        "text_align": "left",
        "image": None,
        "brightness": 1.0
    })

if len(st.session_state.slides) > 1:
    if st.sidebar.button("🗑️ Remove Last Slide"):
        st.session_state.slides.pop()

# --- Image Generation Logic ---
def create_slide_image(slide, logo):
    img_width, img_height = 1080, 1080
    
    if slide.get("image") is not None:
        try:
            bg_image = Image.open(slide["image"]).convert("RGBA")
            bg_image = ImageOps.fit(bg_image, (img_width, img_height), Image.Resampling.LANCZOS)
            enhancer = ImageEnhance.Brightness(bg_image)
            bg_image = enhancer.enhance(slide.get("brightness", 1.0))
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
            canvas.paste(l_img, (pos_logo_x, pos_logo_y), l_img)
        except Exception:
            pass

    # Dynamic Font Loader
    t_size = slide.get("title_size", 65)
    b_size = slide.get("content_size", 36)
    
    title_font = get_custom_font(selected_font, t_size)
    body_font = get_custom_font(selected_font, b_size)

    # Wrap Calculation
    wrap_width_title = max(10, int(9500 / t_size))
    wrap_width_body = max(15, int(11000 / b_size))

    raw_title = str(slide.get("title", ""))
    title_lines = raw_title.upper().split('\n')
    wrapped_title_lines = [textwrap.fill(line, width=wrap_width_title) for line in title_lines if line.strip()]
    wrapped_title = "\n".join(wrapped_title_lines) if wrapped_title_lines else raw_title.upper()

    raw_content = str(slide.get("content", ""))
    content_lines = raw_content.split('\n')
    wrapped_content_lines = [textwrap.fill(line, width=wrap_width_body) for line in content_lines if line.strip()]
    wrapped_content = "\n".join(wrapped_content_lines) if wrapped_content_lines else raw_content

    align_mode = slide.get("text_align", "left")

    # Draw Title Text
    draw.multiline_text(
        (slide.get("title_x", 60), slide.get("title_y", 220)), 
        wrapped_title, 
        fill=slide.get("title_color", "#2ECC71"), 
        font=title_font, 
        spacing=12, 
        align=align_mode
    )

    # Draw Body Text
    draw.multiline_text(
        (slide.get("content_x", 60), slide.get("content_y", 520)), 
        wrapped_content, 
        fill=slide.get("content_color", "#FFFFFF"), 
        font=body_font, 
        spacing=16, 
        align=align_mode
    )

    # Bottom Line Accent
    draw.rectangle([60, pos_line_y - line_thickness, 1020, pos_line_y], fill=line_color)

    return canvas.convert("RGB")

# --- Main Editor & Live Preview Grid ---
col_edit, col_preview = st.columns([1.1, 0.9])

generated_images = []

with col_edit:
    st.subheader("✏️ Content & Element Editors")
    for idx, slide in enumerate(st.session_state.slides):
        with st.expander(f"📌 Slide {idx + 1}: {slide['title'][:25]}", expanded=(idx == 0)):
            
            # --- 1. TITLE INPUT & LOCAL SETTINGS ---
            st.markdown("**1. Title Headline**")
            slide["title"] = st.text_area(f"Title Text #{idx+1}", value=slide["title"], height=70, key=f"title_{idx}")
            
            t_col1, t_col2, t_col3, t_col4 = st.columns([2, 1.2, 1.5, 1.5])
            with t_col1:
                slide["title_size"] = st.slider("Title Size", 30, 110, slide.get("title_size", 65), key=f"tsize_{idx}")
            with t_col2:
                slide["title_color"] = st.color_picker("Color", slide.get("title_color", "#2ECC71"), key=f"tcol_{idx}")
            with t_col3:
                slide["title_x"] = st.number_input("Position X", 0, 1000, slide.get("title_x", 60), key=f"tx_{idx}")
            with t_col4:
                slide["title_y"] = st.number_input("Position Y", 0, 1000, slide.get("title_y", 220), key=f"ty_{idx}")

            st.markdown("---")

            # --- 2. BODY TEXT INPUT & LOCAL SETTINGS ---
            st.markdown("**2. Story Text / Content**")
            slide["content"] = st.text_area(f"Story Text #{idx+1}", value=slide["content"], height=110, key=f"content_{idx}")
            
            b_col1, b_col2, b_col3, b_col4 = st.columns([2, 1.2, 1.5, 1.5])
            with b_col1:
                slide["content_size"] = st.slider("Body Size", 18, 70, slide.get("content_size", 36), key=f"bsize_{idx}")
            with b_col2:
                slide["content_color"] = st.color_picker("Color", slide.get("content_color", "#FFFFFF"), key=f"bcol_{idx}")
            with b_col3:
                slide["content_x"] = st.number_input("Position X", 0, 1000, slide.get("content_x", 60), key=f"bx_{idx}")
            with b_col4:
                slide["content_y"] = st.number_input("Position Y", 0, 1000, slide.get("content_y", 520), key=f"by_{idx}")

            # Alignment Control
            slide["text_align"] = st.radio("Text Alignment", ["left", "center", "right"], index=["left", "center", "right"].index(slide.get("text_align", "left")), horizontal=True, key=f"align_{idx}")

            st.markdown("---")

            # --- 3. BACKGROUND IMAGE & BRIGHTNESS ---
            st.markdown("**3. Background Image & Brightness**")
            img_file = st.file_uploader(f"Upload Image #{idx+1}", type=["jpg", "png", "jpeg"], key=f"img_{idx}")
            if img_file is not None:
                slide["image"] = img_file
                
            slide["brightness"] = st.slider(f"Brightness #{idx+1}", 0.2, 1.8, float(slide.get("brightness", 1.0)), 0.1, key=f"bright_{idx}")

with col_preview:
    st.subheader("👁️ Live Interactive Preview")
    for idx, slide in enumerate(st.session_state.slides):
        slide_img = create_slide_image(slide, logo_img)
        generated_images.append((f"slide_{idx+1}.png", slide_img))
        st.image(slide_img, caption=f"Slide {idx+1} Preview")

# --- Export & Download Section ---
st.markdown("---")
st.subheader("📥 Export Options")

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
