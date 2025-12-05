from rest_framework.serializers import ModelSerializer
from main.models import Room
class Roomserialzer(ModelSerializer):
    class Meta:
        model= Room
        fields='__all__'