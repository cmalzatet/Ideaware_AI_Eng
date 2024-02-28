import os
from typing import List
from docx import Document

from django.conf import settings

from qdrant_client import QdrantClient

from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Qdrant
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from langchain_core.documents.base import Document
from langchain_openai.embeddings.base import OpenAIEmbeddings



def extract_text_from_doc(doc:Document)->list:
    """ Extracts document paragraphs into a list """
    
    return [paragraph.text for paragraph in doc.paragraphs]

def save_document(doc: Document):
    """ Saves .docx document locally """
    
    _ = default_storage.save(f'./documents/{doc.name}', ContentFile(doc.read()))

def save_temporal_file(title:str ,content:list): 
    """ Saves temporal .txt file with the document's content to be embedded and uploaded to the database """
        
    tempfile_path = f"./temp_files/{title}.txt"    
    with open(tempfile_path, 'w') as temporal_file:
        temporal_file.writelines(content)
        
    return tempfile_path

def document_processing(doc_path:str):
    """ Processess the document to be uploaded to the database """
     
    document = load_document(doc_path=doc_path)
    return split_document(document=document)
    
def load_document(doc_path : str):
    """ Uses langchain loader to load the document content """
    
    loader = TextLoader(doc_path)
    return loader.load()

def split_document(document : List[Document]):
    """ Uses langhcain text splitter to upload adequally the content to the database """
    
    doc_splitter = CharacterTextSplitter(chunk_size=16000, chunk_overlap = 100)
    return doc_splitter.split_documents(document)

def embedding_instance_setup(motor = 'openai'):
    """ Sets up the embeddings motor, only implemented OpenAIEmbeddings and uses it by default """
    
    if motor == 'openai':
        return OpenAIEmbeddings()
    
def delete_temp_file(tempfile_path:str):
    """ Deletes the temporal file"""
    os.remove(tempfile_path)

def save_embedding_to_vdb(embedding: OpenAIEmbeddings,
                          docs: List[Document]):
    
    """Uses LangChain's Qdrant method to embed and save the embedding to the database"""
    
    try:        
        qdrant = Qdrant.from_documents(
            docs,
            embedding,
            url=settings.QDRANT_HOST,
            collection_name="documents"
        )
        return True
    
    except Exception as e:
        return e
    
def setup_client():
    """Set's up a QdrantClient to start the search process"""
    
    return QdrantClient(settings.QDRANT_HOST)

def load_collection(client:QdrantClient, embeddings:OpenAIEmbeddings, collection_name:str):
    """Load the vector collection where the search is gonna be done"""
    
    return Qdrant(client=client, embeddings=embeddings, collection_name=collection_name)
    
def search_query(collection:Qdrant, query: str):
    """Executes the search process using the a Qdrant collection and the query"""
        
    return collection.similarity_search_with_score(query)[:3]