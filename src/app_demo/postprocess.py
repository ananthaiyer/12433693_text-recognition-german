from pathlib import Path
from rapidfuzz import process, fuzz

### Loads the German word list "words_de.txt" and uses RapidFuzz to suggest the closest words. 
## Also removes junk words (like a, ad) and duplicates.

ROOT = Path(__file__).resolve().parents[1]
WORDS_PATH = ROOT / "words_de.txt"

def norm(s: str) -> str:
    s = s.lower()
    return (s.replace("ä","ae")
             .replace("ö","oe")
             .replace("ü","ue")
             .replace("ß","ss"))

_raw = [
    w.strip().lower()
    for w in WORDS_PATH.read_text(encoding="utf-8", errors="ignore").splitlines()
    if w.strip()
]

VOWELS = set("aeiouäöü")

WORDS = [
    w for w in _raw
    if len(w) >= 4 and w.isalpha() and any(c in VOWELS for c in w)
]

# normalized view + mapping back
WORDS_NORM = [norm(w) for w in WORDS]
NORM_TO_ORIG = {}
for w in WORDS:
    NORM_TO_ORIG.setdefault(norm(w), w)

def suggest_words(raw: str, k=5, min_score=75):
    raw = (raw or "").strip().lower()
    if len(raw) < 3:
        return []

    raw_n = norm(raw)

    matches = process.extract(
        raw_n,
        WORDS_NORM,
        scorer=fuzz.ratio,
        limit=200
    )

    seen = set()
    reranked = []

    for wn, score, _ in matches:
        w = NORM_TO_ORIG.get(wn, wn)
        if w in seen:
            continue
        seen.add(w)

        length_penalty = abs(len(wn) - len(raw_n)) * 2.0
        final_score = score - length_penalty

        if final_score >= min_score:
            reranked.append((w, round(final_score, 1)))
        if len(reranked) >= k:
            break

    reranked.sort(key=lambda x: x[1], reverse=True)
    return reranked[:k]
