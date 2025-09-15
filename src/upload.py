import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/streetviewpublish']

def upload_360_photo(file_path):
    # Carga las credenciales del token.json
    if not os.path.exists('token.json'):
        print("Error: 'token.json' no encontrado. Por favor, ejecuta el script de autenticación primero.")
        return

    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        print("Error: El token de autenticación no es válido. Ejecuta el script de autenticación.")
        return

    service = build('streetviewpublish', 'v1', credentials=creds)

    try:
        # Paso 1: Iniciar la subida para obtener una URL
        upload_request = service.photo().startUpload().execute()
        upload_url = upload_request.get('uploadUrl')

        if not upload_url:
            print("Error: No se pudo obtener la URL de subida.")
            return

        print(f"URL de subida obtenida: {upload_url}")

        # Paso 2: Subir la foto y sus metadatos
        media_body = MediaFileUpload(file_path, mimetype='image/jpeg', chunksize=-1, resumable=True)

        upload_body = {
            'upload_reference': {
                'uploadUrl': upload_url
            }
        }

        request = service.photo().create(body=upload_body)
        request.body = media_body

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"Subiendo... {int(status.resumable_progress * 100)}%")

        print("\n¡Foto subida con éxito!")
        print(f"ID de la foto: {response.get('photoId', {}).get('id')}")

    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    photo_file = 'media/360street.jpeg'
    if not os.path.exists(photo_file):
        print(f"Error: No se pudo encontrar {photo_file}. Por favor, verifica el nombre y la ubicación.")
    else:
        upload_360_photo(photo_file)