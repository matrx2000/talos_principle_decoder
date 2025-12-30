"""Core hex decoding logic."""
import re
from typing import List

from models import Replacement


# Detect runs of hex bytes like "65 68 6F ..." possibly spanning whitespace/newlines.
# {3,} avoids false positives; change to {1,} if you want to decode very short runs too.
HEX_RUN = re.compile(r'(?:\b[0-9A-Fa-f]{2}\b(?:\s+|$)){3,}', re.MULTILINE)


def _decode_hex_bytes(byte_tokens: List[str]) -> str:
    """Decode a list of hex byte tokens to UTF-8 string."""
    hx = "".join(byte_tokens)
    try:
        return bytes.fromhex(hx).decode("utf-8", errors="replace")
    except Exception:
        return ""


def find_replacements(text: str) -> List[Replacement]:
    """
    Find all hex byte sequences in text and return replacement information.
    
    Args:
        text: Input text that may contain hex byte sequences
        
    Returns:
        List of Replacement objects containing position and decoded information
    """
    reps: List[Replacement] = []
    for m in HEX_RUN.finditer(text):
        run = m.group(0)
        # Strip trailing whitespace from the match to preserve spaces after hex sequences
        run_stripped = run.rstrip()
        trailing_ws = run[len(run_stripped):] if len(run_stripped) < len(run) else ""
        
        tokens = re.findall(r"\b[0-9A-Fa-f]{2}\b", run_stripped)
        decoded = _decode_hex_bytes(tokens)
        if decoded:
            # Preserve trailing whitespace after decoded text
            decoded_with_spaces = decoded + trailing_ws
            reps.append(Replacement(m.start(), m.end(), run, decoded_with_spaces))
    return reps


def apply_replacements(text: str, reps: List[Replacement]) -> str:
    """
    Apply replacements to text, converting hex sequences to decoded text.
    
    Args:
        text: Original text
        reps: List of replacements to apply
        
    Returns:
        Text with hex sequences replaced by decoded text
    """
    if not reps:
        return text

    # Apply from end to start to keep indices valid.
    out = text
    for r in reversed(reps):
        out = out[:r.start] + r.decoded + out[r.end:]
    return out


def decode_text(text: str):
    """
    Decode text containing hex byte sequences.
    
    Args:
        text: Input text that may contain hex byte sequences
        
    Returns:
        DecodeResult containing original, decoded text, and replacement information
    """
    from models import DecodeResult
    
    reps = find_replacements(text)
    decoded_str = apply_replacements(text, reps)
    
    return DecodeResult(
        original=text,
        decoded=decoded_str,
        replacements=reps,
        num_replacements=len(reps)
    )

