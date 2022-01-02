from reportlab.lib.units import inch, cm
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


from reportlab.platypus import PageTemplate, BaseDocTemplate, NextPageTemplate, PageBreak, Frame, Paragraph
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet


from pprint import pprint
import os
import json
 
 
def load_text_json():

    JSON_PATH = os.path.join('..', 'transcript_utf_pb_new')
    json_files =  list()
    return_obj = dict()

    for root, dirs, files in os.walk(JSON_PATH):
        for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.join(root, file))

    # pprint(json_files)
    # pprint(len(json_files))

    for json_file in json_files:
        return_obj[json_file] = json.load(open(json_file, encoding="utf-8"))

    return return_obj


# def create_pdfx():

#     pdf_file = 'Philosophize This! - The Podcast Transcripts by Stephen West.pdf'
    
#     pdfmetrics.registerFont(TTFont('georgia-bold', os.path.join(os.getcwd(), 'georgia', 'georgia-bold.ttf')))
#     pdfmetrics.registerFont(TTFont('georgia-italic', os.path.join(os.getcwd(), 'georgia', 'georgia-italic.ttf')))
#     pdfmetrics.registerFont(TTFont('georgia-regular', os.path.join(os.getcwd(), 'georgia', 'georgia-regular.ttf')))
        
#      # page1
#     can = Canvas(pdf_file, pagesize=(8.3 * inch, 11.7 * inch))
#     can.setFont("georgia-bold", 32)
#     can.drawString(1 * inch, 10 * inch, "Philosophize This!")
#     can.setFont("georgia-italic", 15)
#     can.drawString(1 * inch, 9.7 * inch, "The Podcast Transcripts")
#     can.setFont("georgia-regular", 13)
#     can.drawString(1 * inch, 9 * inch, "By Stephen West")
#     can.showPage()

#     spoken_texts = load_json()

#     for episode in spoken_texts.values(): 

#         title = episode["title"]
#         ep_no = episode["ep"]
#         text = episode["spoken_text"]

#         wrapper = textwrap.TextWrapper(width=100)
  
#         dedented_text = textwrap.dedent(text=text)
#         original = wrapper.fill(text=dedented_text)
          
#         shortened = textwrap.shorten(text=original, width=100)
#         shortened_wrapped = wrapper.fill(text=shortened)

#         can.setFont("georgia-bold", 18)
#         can.drawString(1 * inch, 10 * inch, title)
#         can.setFont("georgia-italic", 16)
#         can.drawString(1 * inch, 9.7 * inch, ep_no)
#         can.setFont("georgia-regular", 13)
#         can.drawString(1 * inch, 9 * inch, spoken_text)
#         can.showPage()

#         break


#     can.save()

# def create_pdf2():

#     from reportlab.pdfgen import canvas
#     from reportlab.lib.pagesizes import A4
#     from reportlab.platypus import SimpleDocTemplate, Paragraph
#     from reportlab.lib.styles import getSampleStyleSheet
#     from reportlab.lib.units import cm

#     my_text = "Hello\nThis is a multiline text\nHere wennnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn do not have to handle the positioning of each line manually"

#     doc = SimpleDocTemplate("example_flowable.pdf",pagesize=A4,
#                             rightMargin=2*cm,leftMargin=2*cm,
#                             topMargin=2*cm,bottomMargin=2*cm)

#     doc.build([Paragraph(my_text.replace("\n", "<br />"), getSampleStyleSheet()['Normal']),])

def add_page_number(canvas, doc):

     canvas.saveState()
     canvas.setFont('Times-Roman', 10)
     page_number_text = "%d" % (doc.page)
     canvas.drawCentredString(
         4.15 * inch,
         0.5 * inch,
         page_number_text
     )
     canvas.restoreState()

def add_title_page(can, doc):

    can.saveState()
    can.setFont("georgia-bold", 32)
    can.drawString(1 * inch, 10 * inch, "Philosophize This!")
    can.setFont("georgia-bold", 16)
    can.drawString(1 * inch, 9.7 * inch, "The Podcast Transcripts")
    can.setFont("georgia-regular", 16)
    can.drawString(1 * inch, 9 * inch, "Written By Stephen West")

    can.restoreState()

def get_body_style():

    sample_style_sheet = getSampleStyleSheet()
    style = sample_style_sheet['Normal']
    style.fontName = 'georgia-regular'
    style.fontSize = 12
    style.leading = 24
    return style

def get_title_style():

    sample_style_sheet = getSampleStyleSheet()
    style = sample_style_sheet['Heading2']
    style.fontName = 'georgia-bold'
    style.fontSize = 16
    return style

def get_subtitle_style():

    sample_style_sheet = getSampleStyleSheet()
    style = sample_style_sheet['Heading3']
    style.fontName = 'georgia-italic'
    style.fontSize = 14
    return style

def create_pdf():

    pdfmetrics.registerFont(TTFont('georgia-bold', os.path.join(os.getcwd(), 'georgia', 'georgia-bold.ttf')))
    pdfmetrics.registerFont(TTFont('georgia-italic', os.path.join(os.getcwd(), 'georgia', 'georgia-italic.ttf')))
    pdfmetrics.registerFont(TTFont('georgia-regular', os.path.join(os.getcwd(), 'georgia', 'georgia-regular.ttf')))

    myFrame = Frame(0, 0, 8.3 * inch, 11.7 * inch, id='myFrame')

    elements = list()

    spoken_texts = load_text_json()
    spoken_texts = sorted(spoken_texts.items(), key=lambda x:x[0])

    body_style = get_body_style()
    title_style = get_title_style()
    subtitle_style = get_subtitle_style()

    for member in spoken_texts: 
        episode = member[1]
        title = episode["title"] 
        ep_no = episode["ep"]
        text = "<br/><br/>" + episode["spoken_text"].replace("\n", "<br />")


        elements.append(PageBreak())
        elements.append(Paragraph(title, title_style))
        elements.append(Paragraph(ep_no, subtitle_style))
        elements.append(Paragraph(text, body_style))
        elements.append(PageBreak())


    doc = SimpleDocTemplate("Philosophize This! - The Podcast Transcripts by Stephen West.pdf",pagesize=A4,
                            rightMargin=2*cm,leftMargin=2*cm,
                            topMargin=2*cm,bottomMargin=2*cm)

    doc.build(elements, onFirstPage=add_title_page, onLaterPages=add_page_number)


# create_pdf()
create_pdf()