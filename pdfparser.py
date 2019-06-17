import io
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage


class DocumentParser:
    def __init__(self):
        self.fake_file_handle = None

    def page_interpreters(self):

        resource_manager = PDFResourceManager()
        self.fake_file_handle = io.StringIO()
        converter = TextConverter(resource_manager, self.fake_file_handle)
        page_interpreter = PDFPageInterpreter(resource_manager, converter)

        return converter, page_interpreter, self.fake_file_handle


    def extract_text_from_pdf(self, pdf_path, pages=None):
        converter, page_interpreter, self.fake_file_handle = self.page_interpreters()

        document = {}
        p = 1

        with self.get_file_handle(pdf_path, "rb") as fh:

            pages = self.get_pages(fh, pages, caching=True, check_extractable=True)
            print("Pages: ", pages)
            #print("Number of 'pages' = {}".format(len(pages)))
            for page in pages:
                print("Within 'for'-loop")
                page_interpreter.process_page(page)
                document[p] = self.get_fake_file_handle_string_value().strip()
                p += 1
            converter.close()
            self.fake_file_handle.close()

            if document:
                return document

    def get_file_handle(self, path, mode):
        return open(path, mode)

    def get_pages(self, fh, pages, caching, check_extractable):
        return PDFPage.get_pages(fh, pages, caching=True, check_extractable=True)

    def get_fake_file_handle_string_value(self):
        return self.fake_file_handle.getvalue()
