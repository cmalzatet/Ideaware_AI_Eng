import requests
import os

# URL del endpoint
APP_PORT = os.environ.get('APP_PORT')

url = f'http://127.0.0.1:{APP_PORT}/search-documents/'

# Archivo .docx que quieres enviar
query = input()

params = {'query': query}
response = requests.get(url, params=params)

# Imprimir la respuesta del servidor
print(response.json())
