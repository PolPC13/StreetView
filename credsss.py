from upload import get_creds
from upload import build

creds = get_creds()
service = build('streetviewpublish', 'v1', credentials=creds)

photo_id = "CAoSHENJQUJJaEJxdXdnZEJmSzUzZUEteVZBYl9XX3o."
resp = service.photo().get(photoId=photo_id).execute()
print("Photo get():", resp)
