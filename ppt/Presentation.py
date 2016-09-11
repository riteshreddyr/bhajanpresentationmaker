__author__ = 'RiteshReddy'
from pptx import Presentation
from pptx.util import Inches
from pptx.enum.text import PP_PARAGRAPH_ALIGNMENT as PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.util import Pt
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE
from datetime import date
import os
from flaskappbase import app
import random

class SaiPresentation():
    def __init__(self, title_silde_image = os.path.join(app.config['DATA_DIRECTORY'], "title_slide.jpg")):
        self.prs = Presentation()
        self.add_title_slide(title_silde_image)

    @staticmethod
    def set_run_font(run, size, color = RGBColor(0x00, 0x00, 0x00), bold = False, italic = None):
        font = run.font
        font.size = size
        font.color.rgb = color
        font.bold = bold
        font.italic = italic

    @staticmethod
    def add_new_run_with_text(para, text = ""):
        run = para.add_run()
        run.text = text
        return run

    @staticmethod
    def add_paragraph_with_alignment(textBox, alignment = PP_ALIGN.CENTER):
        para = textBox.text_frame.add_paragraph()
        para.alignment = alignment
        return para

    @staticmethod
    def add_textBox(slide, left, top, width, height):
        text_box = slide.shapes.add_textbox(left, top, width, height)
        text_box.text_frame.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE
        return text_box

    @staticmethod
    def add_run_to_slide_with_font(slide, left, top, width, height, text_size, alignment = PP_ALIGN.CENTER, color = RGBColor(0xff, 0xff, 0xff), bold = False, italic = None):
        text_box = SaiPresentation.add_textBox(slide, left, top, width, height)
        para = SaiPresentation.add_paragraph_with_alignment(text_box, alignment)
        run = SaiPresentation.add_new_run_with_text(para, "")
        SaiPresentation.set_run_font(run, text_size, color, bold, italic)
        return run

    def add_full_image_slide(self, img_path):
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[6])
        left = top = Inches(0)
        height = Inches(7.5)
        width = Inches(10)
        pic = slide.shapes.add_picture(img_path, left, top, height=height, width=width)

    def add_title_slide(self, image_path = "title_slide.jpg"):
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[6])
        left = top = Inches(0)
        height = Inches(7.5)
        width = Inches(10)
        pic = slide.shapes.add_picture(image_path, left, top, height=height, width=width)
        text_box = SaiPresentation.add_textBox(slide, Inches(2.5), Inches(3.2), Inches(5), Inches(1))
        para = SaiPresentation.add_paragraph_with_alignment(text_box)
        run = SaiPresentation.add_new_run_with_text(para, "Central London \n Sai Center\n" )
        SaiPresentation.set_run_font(run, Pt(44), RGBColor(0xFF, 0xFF, 0xFF), True)
        run = SaiPresentation.add_new_run_with_text(para, date.today().strftime("%B %d, %Y"))
        SaiPresentation.set_run_font(run, Pt(32), RGBColor(0xFF, 0xFF, 0x0F), True)


    def add_bhajan_slide(self, bhajan_name, bhajan_txt, key="", next_bhajan_name="", next_key="" ):
        """
        One slide can hold 10 rows and 49 characters per row.
        :param bhajan_name:
        :param bhajan_txt:
        :param key:
        :param next_bhajan_name:
        :param next_key:
        :return:
        """
        MAX_ROW_LENGTH = 49
        MAX_ROW_COUNT = 9
        def bhajan_slide_template(background_path=None):
            slide = self.prs.slides.add_slide(self.prs.slide_layouts[6])
            if not background_path is None:
                slide.shapes.add_picture(background_path, Inches(0), Inches(0), height=Inches(7.5), width=Inches(10))
            title_rn = self.add_run_to_slide_with_font(slide, Inches(0.5), Inches(0.25), Inches(9), Inches(1), Pt(36))
            bhajan_rn = self.add_run_to_slide_with_font(slide,Inches(0.5), Inches(1.25), Inches(9), Inches(5.5), Pt(32))
            key_rn = self.add_run_to_slide_with_font(slide,Inches(0.5), Inches(6.5), Inches(1), Inches(0.75), Pt(16), PP_ALIGN.LEFT)
            next_bhajan_name_rn = self.add_run_to_slide_with_font(slide, Inches(2.5), Inches(6.5), Inches(4), Inches(0.75), Pt(16))
            next_key_rn = self.add_run_to_slide_with_font(slide, Inches(8), Inches(6.5), Inches(1), Inches(0.75), Pt(16), PP_ALIGN.RIGHT)

            return slide, title_rn, bhajan_rn, key_rn, next_bhajan_name_rn, next_key_rn

        def get_true_lines(text):
            line_list = text.split("\n")
            for ind, line in enumerate(line_list):
                if len(line) > MAX_ROW_LENGTH:
                    """ Break into spaces and reconstruct at 49 intervals : handles multiple lines in one go """
                    space_break = line.split(" ")
                    new_line = "" #string concat...so bad :(
                    cur_line_length = 0
                    for broken in space_break:
                        if cur_line_length + len(broken) > MAX_ROW_LENGTH :
                            new_line += "\n" + broken
                            cur_line_length = len(broken)
                        else :
                            new_line += " " + broken
                            cur_line_length += len(broken) + 1
                    line_list[ind] = new_line
            return '\n'.join(line_list)



        def handle_user_defined_pagebreaks(text):
            def get_text_per_slide(text):
                lines = text.split("\r\n")
                this_set = []
                for i in range(0, len(lines), MAX_ROW_COUNT):
                    for j in range(i, min(len(lines), i+MAX_ROW_COUNT)):
                        this_set.append(lines[j])
                    slide_text.append('\n'.join(this_set))
                    this_set = []
            PAGE_BREAK_MARKER = '\r\n[pagebreak]\r\n'
            slide_text = []
            lines = text.split(PAGE_BREAK_MARKER)
            map(get_text_per_slide, lines)
            return slide_text


        def add_a_bhajan_slide(bhajan_name, text, final = True, key="", next_bhajan_name="", next_key="", background_path=None):
            slide, title_rn, bhajan_rn, key_rn, nxt_bhajan_rn, nxt_key_rn = bhajan_slide_template(background_path)
            title_rn.text = bhajan_name
            bhajan_rn.text = text.strip()
            key_rn.text = key
            if not final:
                nxt_bhajan_rn.text = "Continued"
            else:
                nxt_bhajan_rn.text = next_bhajan_name
                nxt_key_rn.text = next_key

        files = os.listdir(os.path.join(app.config['DATA_DIRECTORY'], 'backgrounds'))
        background_path = None
        if len(files) != 0:
            index = random.randint(0, len(files) - 1)
            background_path = os.path.join(os.path.join(app.config['DATA_DIRECTORY'], 'backgrounds'), files[index])

        text_per_slide = handle_user_defined_pagebreaks(get_true_lines(bhajan_txt))
        for pos, text in enumerate(text_per_slide, start = 1):
            if pos == len(text_per_slide):
                final = True
            else:
                final = False
            if len(bhajan_txt) == 0: # Empty Bhajan
                self.add_full_image_slide(os.path.join(app.config['DATA_DIRECTORY'], 'filler.jpg'))
            else:
                add_a_bhajan_slide(bhajan_name, text, final, key, next_bhajan_name, next_key, background_path)

    def save_presentation(self, filename):
        self.prs.save(filename)

    def create_test_presentation(self):
        self.add_bhajan_slide("Ganesha Sharanam Ganesha Sharanam Ganesha Sharanam Ganesha Sharanam", "Ganesha Ganesha Ganesha Ganesha Ganesha Ganesha GaneshaGanesha Ganesha Ganesha Ganesha GaneshaGanesha Ganesha Ganesha Ganesha Ganesha\nGanesha Ganesha Ganesha Ganesha Ganesha Ganesha GaneshaGanesha Ganesha Ganesha Ganesha GaneshaGanesha Ganesha Ganesha Ganesha Ganesha\nGanesha Ganesha Ganesha Ganesha Ganesha Ganesha GaneshaGanesha Ganesha Ganesha Ganesha GaneshaGanesha Ganesha Ganesha Ganesha Ganesha\nGanesha Ganesha Ganesha Ganesha Ganesha Ganesha GaneshaGanesha Ganesha Ganesha Ganesha GaneshaGanesha Ganesha Ganesha Ganesha Ganesha\nGanesha Ganesha Ganesha Ganesha Ganesha Ganesha GaneshaGanesha Ganesha Ganesha Ganesha GaneshaGanesha Ganesha Ganesha Ganesha Ganesha\nGanesha Ganesha Ganesha Ganesha Ganesha Ganesha GaneshaGanesha Ganesha Ganesha Ganesha GaneshaGanesha Ganesha Ganesha Ganesha Ganesha\n", "Am", "Guru Baba", "B#")
        self.prs.save("test.pptx")


if __name__ == "__main__":
    SaiPresentation().create_test_presentation()