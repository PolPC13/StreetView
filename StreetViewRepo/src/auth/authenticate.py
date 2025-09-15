import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Si modificas los scopes, elimina el token.json para forzar una nueva autenticación.
SCOPES = ['https://www.googleapis.com/auth/streetviewpublish']

# Nombre de tu archivo de credenciales JSON.
CLIENT_SECRETS_FILE = 'client_secret_YOUR_CLIENT_ID.json'

def get_creds():
    creds = None
    # Intenta cargar el token existente
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # Si no hay credenciales válidas o están a punto de expirar
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Inicia el flujo de autenticación en el navegador
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Guarda el token para futuros usos
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

if __name__ == '__main__':
    get_creds()
    print("Autenticación completada. El archivo token.json se ha creado en la carpeta raíz.")