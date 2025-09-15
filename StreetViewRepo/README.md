# 360° Image Upload to Google Street View
Este script te permite subir imágenes de 360° a Google Street View utilizando la API de Google Street View Publish.

## Requisitos

Python 3.7 o superior.

Dependencias instaladas: google-auth, google-auth-oauthlib, google-api-python-client y requests.

Un archivo de credenciales de cliente (client_secrets.json) proporcionado por Google Cloud Console.

Una imagen de 360° llamada 360street.jpeg en el directorio actual.

## Instalación

Clona este repositorio.

Instala las dependencias necesarias con este comando:

pip install -r requirements.txt
Asegúrate de que el archivo client_secrets.json se encuentra en el directorio raíz.


## Uso

Para ejecutar el script, utiliza el siguiente comando:
Para autenticarte (una sola vez):

Bash
python3 src/auth/authenticate.py

Para subir la foto:

Bash
python3 src/upload.py

Si la imagen se sube correctamente, verás el ID de la foto en la consola.



Si ocurre un error durante la subida, el script mostrará los detalles del error, incluyendo el cuerpo de la respuesta JSON si está disponible.

