import streamlit as st
from PIL import Image

from inference import ocr_word
from postprocess import suggest_words
from translate import translate_de_to_en

##  this code is for the Streamlit UI: Upload image -> calls OCR -> shows raw text -> show suggestions -> show translation

st.set_page_config(page_title="German OCR → Offline Translate", layout="centered")
st.title("German Word OCR → Offline English")

uploaded = st.file_uploader("Upload an image containing a single German word", type=["png", "jpg", "jpeg", "webp"])

if uploaded:
    img = Image.open(uploaded).convert("RGB")
    st.image(img, use_container_width=True)

    raw = ocr_word(img)
    st.write(f"**Raw OCR:** `{raw}`")

    candidates = suggest_words(raw, k=5, min_score=60)
    if candidates:
        labels = [f"{w} (score {s})" for w, s in candidates]
        choice_label = st.radio("Pick corrected word:", labels, index=0)
        chosen = choice_label.split(" (score")[0].strip()
    else:
        st.warning("No good dictionary match found — using raw OCR.")
        chosen = raw

    st.write(f"**Selected:** `{chosen}`")

    en = translate_de_to_en(chosen)
    st.write(f"**English:** `{en}`")

    st.caption("Note: single-word translation can be ambiguous without context.")
