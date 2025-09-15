import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/streetviewpublish']

def get_creds():
    """Carga las credenciales desde token.json."""
    if not os.path.exists('token.json'):
        print("Error: 'token.json' no encontrado.")
        return None

    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        print("Error: El token de autenticación no es válido. Ejecuta el script de autenticación.")
        return None
    return creds

creds = get_creds()
if creds:
    service = build('streetviewpublish', 'v1', credentials=creds)

    photo_id = "CAoSHENJQUJJaEJxdXdnZEJmSzUzZUEteVZBYl9XX3o."
    resp = service.photo().get(photoId=photo_id).execute()
    print("Photo get():", resp)