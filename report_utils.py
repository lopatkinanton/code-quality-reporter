from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm

trans_dict = {
    "patterns": "Паттерны",
    "anti-patterns": "Анти-Паттерны",
    "code-style": "Code-style",
    "recommendations": "Рекомендации",
    "rating": "Оценка по 10-балльной шкале"
}

pdfmetrics.registerFont(TTFont('DejaVuSans', 'assets/fonts/DejaVuLGCSans.ttf'))

def generate_pdf_from_json(data: dict, author: str, start_date: datetime, end_date: datetime, filename: str = "code_review_report.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=A4,
                            rightMargin=2 * cm, leftMargin=2 * cm,
                            topMargin=2 * cm, bottomMargin=2 * cm)

    header_style = ParagraphStyle(
        name='Header',
        fontName='DejaVuSans',
        fontSize=16,
        leading=20,
        spaceAfter=12,
        alignment=1  # center
    )

    meta_style = ParagraphStyle(
        name='Meta',
        fontName='DejaVuSans',
        fontSize=12,
        leading=15,
        spaceAfter=10
    )

    title_style = ParagraphStyle(
        name='Title',
        fontName='DejaVuSans',
        fontSize=14,
        spaceAfter=6,
        leading=16
    )

    body_style = ParagraphStyle(
        name='Body',
        fontName='DejaVuSans',
        fontSize=11,
        spaceAfter=12,
        leading=14
    )

    list_style = ParagraphStyle(
        name='List',
        fontName='DejaVuSans',
        fontSize=11,
        leftIndent=12,
        spaceAfter=6,
        leading=14
    )

    story = []

    # Заголовок отчёта
    story.append(Paragraph("Отчёт о качестве кода", header_style))
    story.append(Paragraph(f"<b>Разработчик:</b> {author}", meta_style))
    story.append(Paragraph(f"<b>Период:</b> {start_date.strftime('%d.%m.%Y')} - {end_date.strftime('%d.%m.%Y')}", meta_style))
    story.append(Spacer(1, 0.5 * cm))

    for key, value in data.items():
        translated_title = trans_dict.get(key, key.capitalize())
        story.append(Paragraph(f"<b>{translated_title}:</b>", title_style))

        if isinstance(value, list):
            list_items = [ListItem(Paragraph(str(item), list_style)) for item in value]
            story.append(ListFlowable(list_items, bulletType='bullet', start='-'))
        else:
            story.append(Paragraph(str(value), body_style))

        story.append(Spacer(1, 0.4 * cm))

    doc.build(story)
    print(f"PDF успешно создан: {filename}")
