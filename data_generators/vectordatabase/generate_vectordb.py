from langchain.vectorstores import FAISS
from PyPDF2 import PdfReader
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
file_path = os.path.join(parent_directory, 'pdf_data/car_brands_curiosities.pdf')

pdf_data = PdfReader(file_path)

pdf_text = ""

for i, page in enumerate(pdf_data.pages):
    text = page.extract_text()
    if text:
        pdf_text += text

text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=400,
    chunk_overlap=0
)

final_data = text_splitter.split_text(pdf_text)

embeddings = OpenAIEmbeddings()
db = FAISS.from_texts(final_data, embeddings)
db.save_local('FAISS_car_brands_curiosities')
