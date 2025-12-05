from django .forms import ModelForm
from .models import Room
from django.contrib.auth.models import User
class RoomForm(ModelForm):
    class Meta: # SPECIAl inner class that tell django about how forms are configure
        model=Room
        fields='__all__'
        exclude=['host','participants']
class UserForm(ModelForm):
    class Meta:
        model =User
        fields = ['username','email']