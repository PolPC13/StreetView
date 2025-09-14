from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def get_creds():
    return Credentials.from_authorized_user_file(
        "token.json", ["https://www.googleapis.com/auth/streetviewpublish"]
    )

photo_id = "CAoSHENJQUJJaEJxdXdnrZEteVZBYl9XX3o"  # tu Photo ID
place_id = "ChIJhXWIG6y4pBIRR4SHaDtnrDM"          # tu Place ID

def update_place():
    creds = get_creds()
    service = build("streetviewpublish", "v1", credentials=creds)

    photo_body = {
        "photoId": {"id": photo_id},
        "places": [{"placeId": place_id}],
    }

    # 👉 aquí pasamos id=photo_id como parámetro obligatorio
    resp = service.photo().update(
        id=photo_id,
        body=photo_body,
        updateMask="places"
    ).execute()

    print("Foto actualizada:", resp)

if __name__ == "__main__":
    update_place()