from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from upload import get_creds


photo_id = "CAoSHENJQUJJaEJxdXdnZEJmSzUzZUEteVZBYl9XX3o"

creds = get_creds()
service = build("streetviewpublish", "v1", credentials=creds)

resp = service.photo().get(photoId=photo_id).execute()
print(resp.get("places"))
