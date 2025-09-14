from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from upload import get_creds

photo_id = "CAoSHENJQUJJaEJxdXdnZEJmSzUzZUEteVZBYl9XX3o"  # tu Photo ID
place_id = "ChIJhXWIG6y4pBIRR4SHaDtnrDM"  # Place ID de tu punto aprobado

def update_place():
    creds = get_creds()
    service = build("streetviewpublish", "v1", credentials=creds)

    photo_body = {
        "photoId": {"id": photo_id},
        "places": [{"placeId": place_id}],
    }

    resp = service.photo().update(
        id=photo_id,
        body=photo_body,
        updateMask="places"
    ).execute()

    print("Foto asociada al place:", resp)

if __name__ == "__main__":
    update_place()
