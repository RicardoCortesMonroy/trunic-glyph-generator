import streamlit as st
import base64
from trunic_generator import english_to_trunic
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

def get_url(font_name: Path) -> str:
    """Get source url for direct font injection into HTML style tag"""
    ttf_path = BASE_DIR / "font" / f"{font_name}.ttf"
    with open(ttf_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f'data:font/truetype;base64,{b64}'

# @st.cache_data
def english_to_trunic_cache(*args, **kwargs):
    """Wrapper for english_to_trunic function with data cache for Streamlit"""
    return english_to_trunic(*args, **kwargs)


# Page Title
st.markdown(f"""
    <style>
    @font-face {{
        font-family: 'Trunic-Regular';
        src: url('{get_url("Trunic-Regular")}') format('truetype');
    }}
    @font-face {{
        font-family: 'Trunic-Strikethrough';
        src: url('{get_url("Trunic-Strikethrough")}') format('truetype');
    }}
    
    .hero {{
        position: relative;
        height: 160px;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
    }}      

    .bg-glyphs {{
        position: absolute;
        inset: 0;
        font-family: 'Trunic-Strikethrough';
        font-size: 120px;
        top: 20px;
        opacity: 0.10;
        z-index: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        pointer-events: none;
        white-space: nowrap;
    }}

    .title {{
        position: relative;
        z-index: 2;
        font-size: 3rem;
        font-weight: 700;
    }}
    </style>

    <div class="hero">
        <div class="bg-glyphs">&#xe084&#xe0b4&#xe12e&#xe0d0 &#xe022&#xe11d&#xe24d&#xe1d4</div>
        <div class="title">Trunic Generator</div>
    </div>
    """,
    unsafe_allow_html=True
)

# English input text
english = st.text_area("Input:", value="Hello, World!")

# Trunic formatting options

col1, col2 = st.columns(2)
with col1:
    strikethrough_enabled = st.checkbox("Strikethrough", True)

with col2:
    col21, col22 = st.columns(2)
    with col21:
        minimise_inversions = st.checkbox("Minimise inversions", False)
    with col22:
        st.markdown(
            """
            <div style="position:absolute;top:9px">
                <span title="Prevents adjacent inverted glyph characters that may make certain words harder to read\ne.g. &quot;anemone&quot;, &quot;aluminum&quot;, &quot;biohazard&quot;">
                ⓘ
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

col1, col2 = st.columns(2)
with col1:
    with st.container(horizontal=True, vertical_alignment="center"):
        st.write("Font size")
        font_size = st.number_input(
            label = "Font size",
            label_visibility = "collapsed",
            min_value=0,
            max_value=200,
            value=40,
            width=130
        )
with col2:
    with st.container(horizontal=True, vertical_alignment="center"):
        st.write("Word spacing")
        word_spacing = st.number_input(
            label = "Word spacing",
            label_visibility = "collapsed",
            min_value=0,
            max_value=50,
            value=15,
            width=130
        ) - 10


glyph_unicode_list = english_to_trunic_cache(english, minimise_inversions)
unicode_text = ''.join([c if not isinstance(c,int) else f"&#x{c:x}" for c in glyph_unicode_list])

font_family = "Trunic-Strikethrough" if strikethrough_enabled else "Trunic-Regular"

# Trunic output box
st.markdown(f"""
    <div style="
        font-family: {font_family}, serif;
        font-size: {font_size}px;
        line-height: 1.0;
        letter-spacing: 0.0em;
        word-spacing: {word_spacing}px;
        padding: 1rem;
        border: 1px solid #ccc;
        border-radius: 8px;
        min-height: 80px;
    ">
        {unicode_text}
    </div>
    """,
    unsafe_allow_html=True
)

# Link to repo
st.markdown(f"""
    <div style="
        font-size: 12px;
        font-style: italic;
        color: #c0c0c0;
    ">
        <br>
        Source Code: <a href="https://github.com/RicardoCortesMonroy/trunic-glyph-generator">trunic-glyph-generator</a>
    </div>
    """,
    unsafe_allow_html=True
)