import io
import re
from typing import List, Tuple, Dict
import numpy as np

# Common filler words and hesitation markers in spoken English
FILLER_PATTERNS = [
    r"\b(um|umm|uh|uhh|ah|ahh|er|err)\b",
    r"\b(like)\b",
    r"\b(actually)\b",
    r"\b(basically)\b",
    r"\b(you know)\b",
    r"\b(i mean)\b",
    r"\b(so)\b(?=[\s,]+[A-Z]|\s*$)",  # 'so' as sentence filler
]

COMMON_FILLERS = [
    "um", "uh", "like", "actually", "basically", "you know", "i mean", "so"
]


def detect_filler_words(text: str) -> Tuple[int, List[str], Dict[str, int]]:
    """
    Analyze text for filler words and return count, list of found fillers, and frequency breakdown.
    """
    if not text:
        return 0, [], {}
    
    text_lower = text.lower()
    found_fillers = []
    breakdown: Dict[str, int] = {}
    
    for filler in COMMON_FILLERS:
        pattern = r"\b" + re.escape(filler) + r"\b"
        matches = re.findall(pattern, text_lower)
        if matches:
            count = len(matches)
            found_fillers.extend([filler] * count)
            breakdown[filler] = count
            
    total_count = len(found_fillers)
    return total_count, found_fillers, breakdown


def detect_repeated_words_and_phrases(text: str) -> Dict[str, int]:
    """Detect repetitive words or 2-3 word phrases in speech."""
    if not text:
        return {}
    
    words = [re.sub(r"[^\w]", "", w.lower()) for w in text.split()]
    words = [w for w in words if len(w) > 3]  # skip tiny words
    
    counts: Dict[str, int] = {}
    for w in words:
        counts[w] = counts.get(w, 0) + 1
        
    repeated = {k: v for k, v in counts.items() if v >= 3}
    return repeated


def estimate_speech_duration_from_words(text: str) -> float:
    """Estimate speech duration assuming an average conversational speech rate of 130 words per minute."""
    if not text:
        return 0.5
    word_count = len(text.split())
    # 130 words / 60 seconds = ~2.16 words per second
    return max(1.0, round(word_count / 2.16, 2))
