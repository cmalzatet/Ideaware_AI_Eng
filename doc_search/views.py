from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from docx import Document
from .utils import extract_text_from_doc, save_temporal_file, document_processing
from .utils import embedding_instance_setup, save_embedding_to_vdb, delete_temp_file
from .utils import setup_client, load_collection, search_query
from time import sleep

@csrf_exempt
def upload_docx(request):
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
                
                if successful_upload:
                    return JsonResponse({'message': 'Documento .docx cargado correctamente.'})
                else:
                    return JsonResponse({'message': 'Error en carga de documento'}, status=500)
            
            except Exception as e:
                print(e)
                return JsonResponse({'message': 'Error en carga de documento'}, status=500)
        else:
            return JsonResponse({'error': 'No se proporcionó ningún archivo .docx.'}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido.'}, status=405)
    



def search_documents(request):
    query = request.GET.get('query', '')  
    
    client = setup_client()
    embedding = embedding_instance_setup()
    collection = load_collection(client=client,embeddings=embedding,collection_name="documents")
    
    relevant_documents = search_query(collection=collection, query=query)
    
    # Serializar los documentos encontrados en un formato JSON
    serialized_documents = [{
        'title': doc.metadata.get('source').split('/')[-1][:-4],
        # 'content': doc.page_content,
        'score': score
    } for doc,score in relevant_documents]
    
    return JsonResponse(serialized_documents, safe=False)   