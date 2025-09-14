import os
import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/streetviewpublish']
CLIENT_SECRETS_FILE = 'client_secret_463161281908-5sm7gtau5bbfodcscf65hckrttjlbp6a.apps.googleusercontent.com.json'

def get_creds():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def upload_360_photo(file_path):
    creds = get_creds()

    # Asegurar token válido
    if not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

    service = build('streetviewpublish', 'v1', credentials=creds)

    try:
        # Paso 1: startUpload -> obtener uploadUrl
        upload_ref = service.photo().startUpload().execute()
        upload_url = upload_ref.get('uploadUrl')
        if not upload_url:
            print("No se obtuvo uploadUrl desde startUpload().")
            return
        print(f"Upload URL: {upload_url}")

        # Leer bytes de la imagen
        with open(file_path, 'rb') as f:
            raw_data = f.read()

        headers = {
            "Authorization": f"Bearer {creds.token}",
            "Content-Type": "image/jpeg",
            "X-Goog-Upload-Protocol": "raw",
            "X-Goog-Upload-Content-Length": str(len(raw_data)),
        }

        # Subida (single PUT/POST a la uploadUrl)
        r = requests.post(upload_url, data=raw_data, headers=headers, timeout=120)
        print(f"Respuesta de upload (status {r.status_code}): {r.text!r}")

        if not r.ok:
            print("La subida no fue aceptada por el servidor. Código:", r.status_code)
            return

        # Paso 3: crear Photo en Street View usando uploadUrl
        body = {
            "uploadReference": {
                "uploadUrl": upload_url
            }
        }
        try:
            create_resp = service.photo().create(body=body).execute()
            print("create() response:", create_resp)
            photo_id = create_resp.get('photoId', {}).get('id')
            if photo_id:
                print("Foto publicada correctamente. Photo ID:", photo_id)
            else:
                print("create() no devolvió photoId. Revisa la respuesta completa arriba.")
        except HttpError as he:
            # imprimir detalle del error (cuerpo JSON si lo contiene)
            content = he.content if hasattr(he, 'content') else str(he)
            print("HttpError en photo.create():", content)
    except Exception as e:
        print("Ocurrió un error durante la subida:", repr(e))

if __name__ == "__main__":
    photo_file = '360street.jpeg'
    if not os.path.exists(photo_file):
        print("No se encontró", photo_file)
    else:
        upload_360_photo(photo_file)