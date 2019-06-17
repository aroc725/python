from glob import glob
from os.path import join
import docxpy
from services.pdfparser import DocumentParser

class DocumentProcessor:
    def __init__(self, inputFilePath, outputFilePath, documentParser=None):
        self.inputFilePath = inputFilePath
        self.outputFilePath = outputFilePath
        self.documentParser = documentParser or DocumentParser()

    def extracted_text(self, files):
        """
        :param files: all the files for which text needs to be extracted
        :return: a list containing the extracted text for each file
        """
        all_documents = []
        extracted_file_names = []

        for doc in files:
            key = doc.split("/")[-1]
            extracted_file_names.append(key)

            if doc.endswith(".docx"):
                all_documents.append(docxpy.process(doc))
            elif doc.endswith(".pdf"):
                all_documents.append("".join(self.documentParser.extract_text_from_pdf(doc).values()))
        return all_documents, extracted_file_names

    def get_file(self, path):
        """
        :param path: directory where the files are located
        :return: the list of files in the directory
        """
        files = []
        for ext in ("*.pdf", "*.docx"):
            files.extend(glob(join(path, ext)))
        return files