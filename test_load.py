import requests
import os

APP_PORT = os.environ.get('APP_PORT')

# URL del endpoint
url = f'http://localhost:{APP_PORT}/upload-docx/'

doc_num = input("document number [1,2,3]: ")

# Archivo .docx que quieres enviar
docx_file_path = f'./test{doc_num}.docx'

# Enviar la solicitud POST con el archivo .docx
with open(docx_file_path, 'rb') as f:
    files = {'docx_file': f}
    response = requests.post(url, files=files)

# Imprimir la respuesta del servidor
print(response.json())
