import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))


import pytest

@pytest.fixture(scope="session")
def processor():
    from transformers import TrOCRProcessor
    return TrOCRProcessor.from_pretrained("microsoft/trocr-base-printed")

def simple_cer(pred: str, target: str) -> float:
    import numpy as np
    dp = np.zeros((len(pred)+1, len(target)+1), dtype=int)
    for i in range(len(pred)+1): dp[i,0] = i
    for j in range(len(target)+1): dp[0,j] = j
    for i in range(1, len(pred)+1):
        for j in range(1, len(target)+1):
            cost = 0 if pred[i-1] == target[j-1] else 1
            dp[i,j] = min(dp[i-1,j] + 1, dp[i,j-1] + 1, dp[i-1,j-1] + cost)
    return dp[len(pred), len(target)] / max(1, len(target))

def test_decode_ids_to_string(processor):
    text = "straße"
    ids = processor.tokenizer(text, return_tensors="pt")["input_ids"][0].tolist()
    decoded = processor.tokenizer.decode(ids, skip_special_tokens=True)
    assert isinstance(decoded, str)
    assert len(decoded) > 0

def test_cer_perfect_match():
    assert simple_cer("hallo", "hallo") == 0.0

def test_cer_detects_difference():
    assert simple_cer("hallo", "halo") > 0.0
