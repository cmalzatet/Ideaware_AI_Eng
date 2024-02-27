from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from docx import Document
from .utils import extract_text_from_doc, save_temporal_file, document_processing
from .utils import embedding_instance_setup, save_embedding_to_vdb

@csrf_exempt
def upload_docx(request):
    if request.method == 'POST':
        if 'docx_file' in request.FILES:
            
            try:
                docx_file = request.FILES['docx_file']
                
                document = Document(docx_file)
                
                text_list = extract_text_from_doc(doc=document)
                
                tempfile_path = save_temporal_file(text_list)
                
                processed_document = document_processing(tempfile_path)
                
                embedding = embedding_instance_setup()
                
                successful_upload = save_embedding_to_vdb(embedding=embedding,
                                                          docs= processed_document)
                
                if successful_upload:
                    return JsonResponse({'message': 'Documento .docx cargado correctamente.'})
                else:
                    return JsonResponse({'message': 'Error en carga de documento'}, status=500)
            
            except:
                return JsonResponse({'message': 'Error en carga de documento'}, status=500)
        else:
            return JsonResponse({'error': 'No se proporcionó ningún archivo .docx.'}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido.'}, status=405)
    



@csrf_exempt
def search_document(request):
    if request.method == 'POST':
        if 'docx_file' in request.FILES:
            
            try:
                docx_file = request.FILES['docx_file']
                
                document = Document(docx_file)
                
                text_list = extract_text_from_doc(doc=document)
                
                tempfile_path = save_temporal_file(text_list)
                
                processed_document = document_processing(tempfile_path)
                
                embedding = embedding_instance_setup()
                
                successful_upload = save_embedding_to_vdb(embedding=embedding,
                                                          docs= processed_document)
                
                if successful_upload:
                    return JsonResponse({'message': 'Documento .docx cargado correctamente.'})
                else:
                    return JsonResponse({'message': 'Error en carga de documento'}, status=500)
            
            except:
                return JsonResponse({'message': 'Error en carga de documento'}, status=500)
        else:
            return JsonResponse({'error': 'No se proporcionó ningún archivo .docx.'}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido.'}, status=405)
    