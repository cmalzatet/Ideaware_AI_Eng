from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from docx import Document
from .utils import extract_text_from_doc, generate_embedding


@csrf_exempt
def upload_docx(request):
    if request.method == 'POST':
        if 'docx_file' in request.FILES:
            docx_file = request.FILES['docx_file']
            document = Document(docx_file)
            text = extract_text_from_doc(doc=document)
            embedded_text = generate_embedding(doc_text=text)
            
            return JsonResponse({'message': 'Documento .docx cargado correctamente.'})
        else:
            return JsonResponse({'error': 'No se proporcionó ningún archivo .docx.'}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido.'}, status=405)
    
    
