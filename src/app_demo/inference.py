import json
import torch
from pathlib import Path
from PIL import Image, ImageOps, ImageFilter
from transformers import VisionEncoderDecoderModel, TrOCRProcessor

### Loads TrOCR artifacts and does model.generate(..)-> decode tokens -> raw OCR string

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts" / "trocr_finetuned"

_device = "cuda" if torch.cuda.is_available() else "cpu"

processor = TrOCRProcessor.from_pretrained(ARTIFACTS)
model = VisionEncoderDecoderModel.from_pretrained(ARTIFACTS).to(_device)
model.eval()

with open(ARTIFACTS / "generation_config.json", encoding="utf-8") as f:
    GEN_CFG = json.load(f)

# keep only safe keys
allowed = {
    "max_length", "num_beams", "early_stopping", "do_sample",
    "temperature", "top_k", "top_p",
    "decoder_start_token_id", "bos_token_id", "pad_token_id"
}
GEN_CFG = {k: v for k, v in GEN_CFG.items() if k in allowed}

# token ids
cls_id = processor.tokenizer.cls_token_id
bos_id = processor.tokenizer.bos_token_id
pad_id = processor.tokenizer.pad_token_id

start_id = cls_id if cls_id is not None else bos_id
if start_id is None:
    raise RuntimeError("Tokenizer has no cls_token_id or bos_token_id; cannot set decoder start token.")

model.config.decoder_start_token_id = start_id
model.config.bos_token_id = bos_id if bos_id is not None else start_id
model.config.pad_token_id = pad_id

model.generation_config.decoder_start_token_id = start_id
model.generation_config.bos_token_id = bos_id if bos_id is not None else start_id
model.generation_config.pad_token_id = pad_id

GEN_CFG["decoder_start_token_id"] = start_id
GEN_CFG["bos_token_id"] = bos_id if bos_id is not None else start_id
GEN_CFG["pad_token_id"] = pad_id

# deterministic OCR decoding
GEN_CFG["do_sample"] = False
GEN_CFG["num_beams"] = 5
GEN_CFG["early_stopping"] = True
GEN_CFG["max_length"] = 32

def preprocess(img: Image.Image) -> Image.Image:
    img = img.convert("L")
    img = ImageOps.autocontrast(img)
    img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=200, threshold=3))
    w, h = img.size
    img = img.resize((w * 2, h * 2))
    return img.convert("RGB")

@torch.inference_mode()
def ocr_word(image: Image.Image) -> str:
    img = preprocess(image)
    pixel_values = processor(images=img, return_tensors="pt").pixel_values.to(_device)
    ids = model.generate(pixel_values, **GEN_CFG)
    return processor.batch_decode(ids, skip_special_tokens=True)[0].strip()
