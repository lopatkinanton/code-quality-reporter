from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm

pdfmetrics.registerFont(TTFont('DejaVuSans', 'assets/fonts/DejaVuLGCSans.ttf'))

criteria_titles = {
    "readability_and_style": "Читаемость и стиль",
    "patterns_and_anti_patterns": "Паттерны и антипаттерны",
    "logic_and_architecture": "Логика и архитектура",
    "reliability_and_safety": "Надёжность и безопасность",
    "contextual_fit": "Контекстуальное соответствие"
}

def generate_pdf_from_json(json_data: dict, author: str, repo: str, start_date: datetime, 
                           end_date: datetime, filename: str = "code_review_report.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=A4,
                            rightMargin=2 * cm, leftMargin=2 * cm,
                            topMargin=2 * cm, bottomMargin=2 * cm)

    header_style = ParagraphStyle(name='Header', fontName='DejaVuSans', fontSize=16, leading=20, spaceAfter=12, alignment=1)
    meta_style = ParagraphStyle(name='Meta', fontName='DejaVuSans', fontSize=12, leading=15, spaceAfter=10)
    section_title_style = ParagraphStyle(name='SectionTitle', fontName='DejaVuSans', fontSize=14, spaceAfter=6, leading=16)
    score_style = ParagraphStyle(name='Score', fontName='DejaVuSans', fontSize=12, leading=14, spaceAfter=4)
    comment_style = ParagraphStyle(name='Comment', fontName='DejaVuSans', fontSize=11, leading=14, spaceAfter=12)

    story = []

    story.append(Paragraph("Отчёт о качестве кода", header_style))
    story.append(Paragraph(f"<b>Разработчик:</b> {author}", meta_style))
    story.append(Paragraph(f"<b>Репозиторий:</b> {repo}", meta_style))
    story.append(Paragraph(f"<b>Период:</b> {start_date.strftime('%d.%m.%Y')} - {end_date.strftime('%d.%m.%Y')}", meta_style))
    story.append(Spacer(1, 0.5 * cm))

    summary = json_data.get("summary", {})
    total_score = summary.get("total_score", "N/A")
    max_score = summary.get("max_score", "N/A")
    story.append(Paragraph(f"<b>Итоговая оценка:</b> {total_score} из {max_score}", section_title_style))
    story.append(Spacer(1, 0.3 * cm))

    criteria = json_data.get("criteria", {})
    for key, details in criteria.items():
        title = criteria_titles.get(key, key.replace("_", " ").capitalize())
        score = details.get("score", "N/A")
        comment = details.get("comment", "")

        story.append(Paragraph(f"<b>{title}</b>", section_title_style))
        story.append(Paragraph(f"Оценка: {score}", score_style))
        story.append(Paragraph(comment, comment_style))

    doc.build(story)
    print(f"Отчёт сохранён: {filename}")
