from pathlib import Path
import re

from fpdf import FPDF

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MARKDOWN_PATH = PROJECT_ROOT / "docs" / "report.md"
PDF_PATH = PROJECT_ROOT / "docs" / "project_report.pdf"

IMAGE_PATTERN = re.compile(r"!\[(.*?)\]\((.*?)\)")


class ReportPDF(FPDF):
    def header(self):
        pass


def render_markdown_to_pdf(markdown_path: Path, pdf_path: Path) -> None:
    with markdown_path.open("r", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f]

    pdf = ReportPDF(format="A4")
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()
    pdf.set_margins(left=18, top=18, right=18)
    pdf.set_font("Arial", size=11)

    def render_text(text: str, height: int = 6) -> None:
        if pdf.w - pdf.r_margin - pdf.x <= 0:
            pdf.ln(5)
            pdf.set_x(pdf.l_margin)
        try:
            pdf.multi_cell(0, height, text)
        except Exception as exc:
            print(f"Available width: {pdf.w - pdf.r_margin - pdf.x}")
            print(f"PDF rendering failed on line: {repr(text)}")
            raise

    for line in lines:
        if not line:
            pdf.ln(4)
            continue

        img_match = IMAGE_PATTERN.match(line)
        if img_match:
            caption, rel_path = img_match.groups()
            img_path = (PROJECT_ROOT / rel_path).resolve()
            if img_path.exists():
                max_width = pdf.w - pdf.l_margin - pdf.r_margin
                try:
                    pdf.image(str(img_path), w=max_width)
                except RuntimeError:
                    pass
            pdf.ln(3)
            pdf.set_font("Arial", style="I", size=10)
            render_text(caption, height=5)
            pdf.set_font("Arial", size=11)
            pdf.ln(4)
            continue

        if line.startswith("# "):
            pdf.set_font("Arial", "B", 18)
            render_text(line[2:].strip(), height=8)
            pdf.ln(3)
            pdf.set_font("Arial", size=11)
            continue

        if line.startswith("## "):
            pdf.set_font("Arial", "B", 15)
            render_text(line[3:].strip(), height=7)
            pdf.ln(2)
            pdf.set_font("Arial", size=11)
            continue

        if line.startswith("### "):
            pdf.set_font("Arial", "B", 13)
            render_text(line[4:].strip(), height=6)
            pdf.ln(2)
            pdf.set_font("Arial", size=11)
            continue

        if line.startswith("- "):
            text = f"- {line[2:].strip()}"
            render_text(text, height=6)
            continue

        render_text(line, height=6)

    pdf.output(str(pdf_path))


if __name__ == "__main__":
    render_markdown_to_pdf(MARKDOWN_PATH, PDF_PATH)
    print(f"Generated PDF report at {PDF_PATH}")
