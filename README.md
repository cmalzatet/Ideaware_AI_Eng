# BASE DE DATOS VECTORIAL

Este consiste de una aplicación a la cual, usando requests POST para cargar el contenido de documentos .docx a una base de datos vectorial y GET para hacer preguntas y obtener los documentos (top 3) en los cuales se pueda encontrar la respuesta a la pregunta.

## HERRAMIENTAS

En esta aplicación se utiliza:

-- Python 3.8.10
-- Pip 21.1.1
-- Docker 25.0.3

## CONFIGURACIÓN

Inicialmente se debe definir variables de entorno y configuración del Dockerfile:

-- Define el puerto en el que se expone la base de datos vectorial:

```
export DB_PORT="<PUERTO_DB>"
export APP_PORT="<PUERTO_APP>"
```

por ejemplo:

```
export DB_PORT="6333"
export APP_PORT="8000"
```

-- En el archivo Dockerfile, se encuentran las líneas:

```
ENV DB_PORT=<DB_PORT>
ENV OPENAI_API_KEY=<OPENAI_API_KEY>
```

En estas es necesario que se reemplacen los valores por defecto por los valores del caso particular (DB_PORT debe corresponder en el definido en el entorno)

## EJECUCIÓN

Suponiendo que se tienen los privilegios necesarios.

Primero, requerimos establecer una red en la cual se puedan comunicar los contenedores:

```
docker network create nombre_de_la_red
```

Luego es encesario que inicializar la base de datos vectorial y conectarla a la red:

```
docker pull qdrant/qdrant
docker run --network nombre_de_la_red --name qdrant -p 6333:$DB_PORT  qdrant/qdrant
```

Posteriormente, se construye y ejecuta la imagen de docker de la aplicación:

```
docker build -t <app_name> .
docker run --network doc_network --name <app_name> -p 8000:$APP_PORT <app_name>
```

En este caso, los recursos son accesibles en las urls:

- Qdrant DB: http://localhost:DB_PORT
- App: http://localhost:APP_PORT


## EJEMPLOS DE USO

El la fuente de la aplicación se incluyen scripts para la prueba de los endpoints y documentos de ejemplo. Estos requieren las librerías os y requests:

### CARGA DE DOCUMENTOS

Al ejecutar el script 'test_load.py', el usuario ingresa un número entre 1,2,3 para escoger entre los tres documentos de prueba disponibles. Luego, este utiliza el endpoint /upload-docx/ para cargar el binario del documento seleccionado en el paquete: {'docx_file': <binario_del_documento>} y finalmente hacer la solicitud POST con el paquete en el campo de files:


```
response = requests.post(f'http://localhost:{APP_PORT}/upload-docx/', files = {'docx_file': <binario_del_documento>})
```

La respuesta confirmará si el documento fue cargado correctamente o si hubo un error en el proceso.

### PREGUNTA Y EXTRACCIÓN DE DOCUMENTOS

Al ejecutar el script 'test_load.py', el usuario ingresa la pregunta o query deseada. Luego, se utiliza el método GET en el endpoint /search-documents/ para procesar la query e identificar el documento más probable a responder la pregunta. 


```
response = requests.get(f'http://127.0.0.1:{APP_PORT}/search-documents/', params={'query': <pregunta_del_usuario>})
```

La respuesta entregará el nombre del documento con mayor probabilidad de responder la pregunta en el campo "title" y la respectiva probabilidad en el campo "score"




