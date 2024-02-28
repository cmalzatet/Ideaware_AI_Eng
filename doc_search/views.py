import getpass
import os
from time import sleep
from docx import Document

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .utils import save_document, extract_text_from_doc, save_temporal_file, document_processing
from .utils import embedding_instance_setup, save_embedding_to_vdb, delete_temp_file
from .utils import setup_client, load_collection, search_query


# os.environ["OPENAI_API_KEY"] = getpass.getpass()

@csrf_exempt
def upload_docx(request):
    """Processess the document reception and manages the vectorization and upload to the database"""
    
    if request.method == 'POST':
        if 'docx_file' in request.FILES:
            
            try:
                docx_file = request.FILES['docx_file']
                title = docx_file.name
                
                document = Document(docx_file)
                
                text_list = extract_text_from_doc(doc=document)
                
                tempfile_path = save_temporal_file(title, text_list)
                
                processed_document = document_processing(tempfile_path)
                
                embedding = embedding_instance_setup()
                
                successful_upload = save_embedding_to_vdb(embedding=embedding,docs= processed_document)
                
                delete_temp_file(tempfile_path=tempfile_path)
                
                if successful_upload == True:
                    return JsonResponse({'message': 'Documento .docx cargado correctamente.'})
                else:
                    return JsonResponse({'error': f'Error en carga de documento {successful_upload}'}, status=500)
            
            except Exception as e:
                return JsonResponse({'error': f'Error en carga de documento. {e}'}, status=500)
        else:
            return JsonResponse({'error': 'No se proporcionó ningún archivo .docx.'}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido.'}, status=405)

def search_documents(request):
    """Processess the query to extract the document information"""
    
    query = request.GET.get('query', '')  
    
    if request.method == 'GET':
        try:
            client = setup_client()
            embedding = embedding_instance_setup()
            collection = load_collection(client=client,embeddings=embedding,collection_name="documents")
            
            relevant_documents = search_query(collection=collection, query=query)
            
            serialized_documents = [{
                'title': doc.metadata.get('source').split('/')[-1][:-4],
                'score': score
            } for doc,score in relevant_documents]
                
            return JsonResponse(serialized_documents, safe=False)
        
        except Exception as e:
            return JsonResponse({'error': f'Error en el procesamiento de la solicitud. {e}'}, status=500)
        
    else:
        return JsonResponse({'error': 'Método no permitido.'}, status=405)