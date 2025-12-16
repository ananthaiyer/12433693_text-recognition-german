import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import pytest
import torch
from PIL import Image, ImageDraw, ImageFont

@pytest.fixture(scope="session")
def processor():
    from transformers import TrOCRProcessor
    return TrOCRProcessor.from_pretrained("microsoft/trocr-base-printed")

def make_dummy_word_image(text="grüß", size=(256, 64)):
    img = Image.new("RGB", size, "white")
    d = ImageDraw.Draw(img)
    d.text((10, 10), text, fill="black")
    return img

def test_image_to_pixel_values(processor):
    img = make_dummy_word_image("test")
    out = processor(images=img, return_tensors="pt")
    assert "pixel_values" in out
    pv = out["pixel_values"]
    assert isinstance(pv, torch.Tensor)
    assert pv.dtype in (torch.float32, torch.float16, torch.bfloat16)
    assert pv.ndim == 4
    assert pv.shape[0] == 1
    assert pv.shape[1] == 3

def test_text_to_labels_roundtrip(processor):
    text = "grüß" 
    enc = processor.tokenizer(text, return_tensors="pt")
    assert "input_ids" in enc
    ids = enc["input_ids"][0].tolist()
    decoded = processor.tokenizer.decode(ids, skip_special_tokens=True)
    assert isinstance(decoded, str)
    assert len(decoded) > 0
