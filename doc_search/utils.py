from docx import Document
from django.conf import settings
import getpass
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Qdrant
from langchain_core.documents.base import Document
from langchain_openai.embeddings.base import OpenAIEmbeddings
import os
from qdrant_client import QdrantClient
import uuid
from typing import List

# os.environ["OPENAI_API_KEY"] = getpass.getpass()
os.environ["OPENAI_API_KEY"] = ""
os.environ["QDRANT_API_KEY"] = "F1zLVHYwI-dkDcAQmoRGNn_666eqsKT6V6sGw_VtL7vHjD_iV8MaUw"

def extract_text_from_doc(doc:Document)->list:    
    return [paragraph for paragraph in doc.paragraphs]

def save_temporal_file(content:list):
     
    tempfile_path = f"../temp_files/tempdoc_{uuid.uuid4().hex}.txt"    
    with open(tempfile_path) as temporal_file:
        temporal_file.writelines(content)
        
    return tempfile_path

def document_processing(doc_path:str):    
    document = load_document(doc_path=doc_path)
    return split_document(document=document)
    

def load_document(doc_path : str):
    loader = TextLoader(doc_path)
    return loader.load()

def split_document(document : List[Document]):
    doc_splitter = CharacterTextSplitter(chunk_size=16000, chunk_overlap = 100)
    return doc_splitter.split_documents(document)

def embedding_instance_setup(motor = 'openai'):
    if motor == 'openai':
        return OpenAIEmbeddings()

def save_embedding_to_vdb(embedding: OpenAIEmbeddings,
                          docs: List[Document]):
    
    try:        
        qdrant = Qdrant.from_documents(
            docs,
            embedding,
            url=settings.QDRANT_HOST,
            prefer_grpc=True,
            api_key=settings.QDRANT_API_KEY,
            collection_name="documents"
        )
        return True
    
    except:
        return False
        
    
    
def generate_embedding(doc_text:str):
    
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small",)
    embedded_text = embeddings.embed_query(doc_text)
    return embedded_text