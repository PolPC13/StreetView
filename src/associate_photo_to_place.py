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

def update_place():
    creds = get_creds()
    if not creds:
        return

    service = build("streetviewpublish", "v1", credentials=creds)

    photo_id = "CAoSHENJQUJJaEJxdXdnZEJmSzUzZUEteVZBYl9XX3o" 
    place_id = "ChIJhXWIG6y4pBIRR4SHaDtnrDM"

    photo_body = {
        "photoId": {"id": photo_id},
        "places": [{"placeId": place_id}],
    }

    resp = service.photo().update(
        id=photo_id,
        body=photo_body,
        updateMask="places"
    ).execute()

    print("media associated to Place:", resp)

if __name__ == "__main__":
    update_place()