import cloudinary
from fastapi.params import File


class Uploader():
    def __init__(self, settings) -> None:
        cloudinary.config(
            cloud_name=settings.CLOUNDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET
        )

    def upload(self, file: File):
        return cloudinary.uploader.upload(file)
