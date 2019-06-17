from mock import mock_open, patch
import os
from pdfminer.pdfpage import PDFPage
from pdfminer.pdftypes import PDFStream
from services.pdfparser import DocumentParser
import pytest
from unittest.mock import MagicMock

def get_pdf_page_array():
    pdf_pages = []

    attrs = { "MediaBox": [0, 0, 400, 300] }
    for i in range(4):
        page = PDFPage(doc=None, pageid=i, attrs=attrs)
        rawdata = "Department of Homeland Security"
        pdf_stream = PDFStream(attrs, rawdata)
        pdf_stream.data = rawdata
        pdf_stream.set_objid(i, i)
        page.contents = [pdf_stream]
        pdf_pages.append(page)

    return pdf_pages

def test_extract_pdf_from_text2(monkeypatch):
    print("Within test method")
    mock_file = MagicMock()
    mock_file.readline = MagicMock(return_value="contents of file")
    mock_open = MagicMock(return_value=mock_file)
    monkeypatch.setattr("builtins.open", mock_open)

    doc_parser = DocumentParser()
    assert doc_parser != None

    # DocumentParser.get_pages.side_effect = get_pdf_pages(fh=mock_open(read_data='contents of file'), pages=[], caching=True, check_extractable=True)
    #with patch("services.pdfparser.DocumentParser.get_pages") as mock_get_pages:
    #    #mock_get_pages.return_value = iter(get_pdf_page_array())
    #    mock_get_pages.side_effect = iter(get_pdf_page_array())

    #mock_get_pages = MagicMock()
    #mock_get_pages.get_pages.return_value = iter(get_pdf_page_array())

    text = doc_parser.extract_text_from_pdf(os.getcwd() + "\Statement_of_Findings-FraudFound.pdf")
    print("Text: ", text)