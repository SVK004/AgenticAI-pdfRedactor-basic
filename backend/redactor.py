import fitz  # PyMuPDF
from crew_agent import redact_text_with_crew

def redact_file(src_path, dst_path):
    doc = fitz.open(src_path)
    for page in doc:
        original_text = page.get_text()
        redacted_text = redact_text_with_crew(original_text)

        # Normalize output to string
        if isinstance(redacted_text, (list, tuple)):
            redacted_text = redacted_text[0]
        redacted_text = str(redacted_text)

        # Remove original content: white background wipe
        page.draw_rect(page.rect, fill=(1, 1, 1))  # RGB white

        # Redraw redacted content line by line to maintain spacing
        lines = redacted_text.split('\n')
        y = 50  # Start printing text 50px from top
        for line in lines:
            page.insert_text((50, y), line, fontsize=12, color=(0, 0, 0))  # Black text
            y += 18  # line spacing

    doc.save(dst_path)
