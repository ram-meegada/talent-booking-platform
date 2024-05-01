from artist_app.utils import messages
from artist_app.models.talentCategoryModel import TalentCategoryModel
from artist_app.models.talentSubCategoryModel import TalentSubCategoryModel
from artist_app.serializers import adminSerializer

class AdminService:
    def add_category(self, request):
        name = request.data["name"]
        talent_obj = TalentCategoryModel.objects.create(name=name)
        return {"data": request.data, "message": messages.CATEGORY_ADDED, "status": 201}
    
    def add_sub_category(self, request):
        name = request.data["name"]
        category_id = request.data["category"]
        talent_sub_category = TalentSubCategoryModel.objects.create(
            name=name,
            category_id=category_id
        )
        return {"data": request.data, "message": messages.SUB_CATEGORY_ADDED, "status": 201}
    
    def subcategory_listing_by_category_id(self, request):
        sub_categories = TalentSubCategoryModel.objects.filter(category = request.data["category"])
        serializer = adminSerializer.SubCategorySerializer(sub_categories, many=True)
        return {"data": serializer.data, "message": messages.SUB_CATEGORIES_LISTING, "status": 200}