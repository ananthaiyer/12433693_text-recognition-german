import argostranslate.translate

## Uses Argos Translate offline to translate the final selected German word to English

def translate_de_to_en(word: str) -> str:
    word = (word or "").strip()
    if not word:
        return ""
    return argostranslate.translate.translate(word, "de", "en")
