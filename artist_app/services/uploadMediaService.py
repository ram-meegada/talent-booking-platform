from artist_app.models.uploadMediaModel import UploadMediaModel
from artist_app.utils.saveImage import save_image
from artist_app.serializers.uploadMediaSerializer import CreateUpdateUploadMediaSerializer
from artist_app.utils import messages

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
            print(error)
            return {"data": "", "message": messages.WENT_WRONG, "status": 400}