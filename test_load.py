import requests

# URL del endpoint
url = 'http://127.0.0.1:8000/upload-docx/'

# Archivo .docx que quieres enviar
docx_file_path = './test3.docx'

# Enviar la solicitud POST con el archivo .docx
with open(docx_file_path, 'rb') as f:
    files = {'docx_file': f}
    response = requests.post(url, files=files)

# Imprimir la respuesta del servidor
print(response.json())
