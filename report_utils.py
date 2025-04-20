from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm

pdfmetrics.registerFont(TTFont('DejaVuSans', 'assets/fonts/DejaVuLGCSans.ttf'))

CRITERIA_TITLES = {
    "readability_and_style": "Читаемость и стиль",
    "patterns_and_anti_patterns": "Паттерны и антипаттерны",
    "logic_and_architecture": "Логика и архитектура",
    "reliability_and_safety": "Надёжность и безопасность",
    "contextual_fit": "Контекстуальное соответствие"
}

STYLES = {
    "header": ParagraphStyle(name='Header', fontName='DejaVuSans', fontSize=16, leading=20, spaceAfter=12, alignment=1),
    "meta": ParagraphStyle(name='Meta', fontName='DejaVuSans', fontSize=12, leading=15, spaceAfter=10),
    "section_title": ParagraphStyle(name='SectionTitle', fontName='DejaVuSans', fontSize=14, spaceAfter=6, leading=16),
    "score": ParagraphStyle(name='Score', fontName='DejaVuSans', fontSize=12, leading=14, spaceAfter=4),
    "comment": ParagraphStyle(name='Comment', fontName='DejaVuSans', fontSize=11, leading=14, spaceAfter=12),
}


def build_header(story, author, repo, start_date, end_date):
    story.append(Paragraph("Отчёт о качестве кода", STYLES["header"]))
    story.append(Paragraph(f"<b>Разработчик:</b> {author}", STYLES["meta"]))
    story.append(Paragraph(f"<b>Репозиторий:</b> {repo}", STYLES["meta"]))
    story.append(Paragraph(f"<b>Период:</b> {start_date.strftime('%d.%m.%Y')} - {end_date.strftime('%d.%m.%Y')}", STYLES["meta"]))
    story.append(Spacer(1, 0.5 * cm))


def build_summary(story, summary):
    total_score = summary.get("total_score", "N/A")
    max_score = summary.get("max_score", "N/A")
    story.append(Paragraph(f"<b>Итоговая оценка:</b> {total_score} из {max_score}", STYLES["section_title"]))
    story.append(Spacer(1, 0.3 * cm))


def build_criteria_section(story, criteria):
    for key, details in criteria.items():
        title = CRITERIA_TITLES.get(key, key.replace("_", " ").capitalize())
        score = details.get("score", "N/A")
        comment = details.get("comment", "")

        story.append(Paragraph(f"<b>{title}</b>", STYLES["section_title"]))
        story.append(Paragraph(f"Оценка: {score}", STYLES["score"]))
        if comment:
            story.append(Paragraph(comment, STYLES["comment"]))


def generate_pdf_report(report_data: dict, author: str, repo_name: str,
                        start_date: datetime, end_date: datetime,
                        output_file: str = "report.pdf"):

    doc = SimpleDocTemplate(output_file, pagesize=A4,
                            rightMargin=2 * cm, leftMargin=2 * cm,
                            topMargin=2 * cm, bottomMargin=2 * cm)

    story = []

    build_header(story, author, repo_name, start_date, end_date)
    build_summary(story, report_data.get("summary", {}))
    build_criteria_section(story, report_data.get("criteria", {}))

    doc.build(story)
    print(f"Отчёт сохранён: {output_file}")
