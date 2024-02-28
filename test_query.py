import requests

# URL del endpoint
url = 'http://127.0.0.1:8000/search-documents/'

# Archivo .docx que quieres enviar
query = input()

params = {'query': query}
response = requests.get(url, params=params)

# Imprimir la respuesta del servidor
print(response.json())
