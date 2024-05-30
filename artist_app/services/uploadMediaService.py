from artist_app.models.uploadMediaModel import UploadMediaModel
from artist_app.utils.saveImage import save_image
from artist_app.serializers.uploadMediaSerializer import CreateUpdateUploadMediaSerializer
from artist_app.utils import messages
import mimetypes

class UploadMediaService:
    def upload_media(self, request):
        images = dict(request.data)["media"]
        is_video = False
        try:
            response_data = []
            for img in images:
                image_response = save_image(img)
                try:
                    if "video" in img.content_type:
                        is_video = True
                except:
                    pass         
                data = {
                    "media_file_url": image_response[0],
                    "media_file_type": img.content_type,
                    "media_file_name": image_response[1],
                    "is_video": is_video
                }
                serializer = CreateUpdateUploadMediaSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                response_data.append(serializer.data)    
            return {"data": response_data, "message": messages.MEDIA_UPLOADED, "status": 200}
        except Exception as error:
            return {"data": "", "message": messages.WENT_WRONG, "status": 400}

    def create_upload_media_xl(self, request, file):
        media_list = []
        
        # Process the in-memory file object
        image_url, image_name = save_image(file)
        media = UploadMediaModel()
        media.media_file_url = image_url
        media.media_file_name = image_name
        media.file_type = mimetypes.guess_type(file.name)[0]
        if media.file_type is None:
            media.file_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        media.save()

        media_list.append(media)

        serializer = CreateUpdateUploadMediaSerializer(media_list, many=True)
        return {
            "file_url": media.media_file_url,
            "status": "success",
            "message": "Excel file uploaded successfully."
        }