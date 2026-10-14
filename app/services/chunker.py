
def split_text(
    text: str,
    chunk_size: int = 1200,
    chunk_overlap: int = 150,
) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")

    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be non-negative and smaller than chunk_size."
        )

    text = text.strip()
    if not text:
        return []

    chunks: list[str] = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)

        if end < text_length:
            # Prefer a word or paragraph boundary when practical.
            boundary = max(
                text.rfind("\n", start + chunk_size // 2, end),
                text.rfind(" ", start + chunk_size // 2, end),
            )
            if boundary > start:
                end = boundary

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end >= text_length:
            break

        next_start = max(start + 1, end - chunk_overlap)

        # Avoid starting in the middle of a word.
        while next_start < end and not text[next_start - 1].isspace():
            next_start += 1

        start = next_start

    return chunks
