"""Very lightweight hashed bag-of-words embedding."""

import math
import re

TOKEN_PATTERN = re.compile(r"\b[a-zA-Z0-9_]+\b")


def tokenize(text: str) -> list[str]:
    return [match.group(0).lower() for match in TOKEN_PATTERN.finditer(text)]


def embed_text(text: str, dimensions: int = 512) -> list[float]:
    vec = [0.0] * dimensions
    tokens = tokenize(text)
    if not tokens:
        return vec
    for token in tokens:
        idx = hash(token) % dimensions
        vec[idx] += 1.0

    norm = math.sqrt(sum(v * v for v in vec))
    if norm == 0:
        return vec
    return [v / norm for v in vec]


def cosine_similarity(v1: list[float], v2: list[float]) -> float:
    return sum(a * b for a, b in zip(v1, v2, strict=False))
