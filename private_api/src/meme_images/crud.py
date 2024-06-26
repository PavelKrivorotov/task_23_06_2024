from main.minio import client
from meme_images.schemas import (
    WriteImage,
    UpdateImage,
    DeleteImage,
    ReadImage
)


class MemeImagesCRUD:
    def upload_image(self, data: WriteImage) -> str:
        if not client.bucket_exists(bucket_name=data.bucket):
            client.make_bucket(bucket_name=data.bucket)

        client.put_object(
            bucket_name=data.bucket,
            object_name=data.filename,
            data=data.file.file,
            length=data.file.size
        )

        url = ReadImage(bucket=data.bucket, filename=data.filename).model_dump()
        return url

    def update_image(self, data: UpdateImage) -> str:
        client.remove_object(
            bucket_name=data.old_bucket,
            object_name=data.old_filename
        )

        return self.upload_image(data)

    def delete_image(self, data: DeleteImage) -> None:
        client.remove_object(
            bucket_name=data.bucket,
            object_name=data.filename
        )

meme_images_crud = MemeImagesCRUD()

