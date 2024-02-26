from docx import Document
from django.conf import settings
import getpass
from langchain_openai import OpenAIEmbeddings
import os

# os.environ["OPENAI_API_KEY"] = getpass.getpass()
os.environ["OPENAI_API_KEY"] = "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"

def extract_text_from_doc(doc:Document)->str:
    content = ''
    paragraphs = doc.paragraphs
    for paragraph in paragraphs:
        content += paragraph.text + '\n'
        
    return content

def generate_embedding(doc_text:str):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small",)
    embedded_text = embeddings.embed_query(doc_text)
    return embedded_text