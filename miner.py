import math
import fitz
from tkinter import PhotoImage

class PDFMiner:
    def __init__(self, filepath):
        self.filepath = filepath
        self.pdf = fitz.open(self.filepath)
        self.first_page = self.pdf.load_page(0)
        # getting height and width of the PDF
        self.width, self.height = self.first_page.rect.width, self.first_page.rect.height
        # zooming the page            
        zoomdict = {800: 0.8, 700: 0.6, 600: 1.0, 500: 1.0}
        width = int(math.floor(self.width / 100.0) * 100)
        self.zoom = zoomdict[width]

    def get_metadata(self):
        metadata = self.pdf.metadata
        numPages = self.pdf.page_count
        return metadata, numPages

    # function for getting the page
    def get_page(self, page_num):
        # loading the page
        page = self.pdf.load_page(page_num)
        # checking if zoom is True
        if self.zoom:
            # creating a Matrix whose zoom factor is self.zoom
            mat = fitz.Matrix(self.zoom, self.zoom)
            # gets the image of the page
            pix = page.get_pixmap(matrix=mat)
        # returns the image of the page  
        else:
            pix = page.get_pixmap()
        # a variable that holds a transparent image
        px1 = fitz.Pixmap(pix, 0) if pix.alpha else pix
        # converting the image to bytes
        imgdata = px1.tobytes("ppm")
        # returning the image data
        return PhotoImage(data=imgdata)

    def get_text(self,page_num):
        # load page
        page = self.pdf.load_page(page_num)
        # getting text from loaded page
        text = page.getText('text')
        return text
