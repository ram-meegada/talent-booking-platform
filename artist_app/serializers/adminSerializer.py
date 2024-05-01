from rest_framework import serializers

from artist_app.models.talentCategoryModel import TalentCategoryModel
from artist_app.models.talentSubCategoryModel import TalentSubCategoryModel

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TalentCategoryModel
        fields = ["id", "name"]

class SubCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = TalentSubCategoryModel
        fields = ["id", "name", "category"]