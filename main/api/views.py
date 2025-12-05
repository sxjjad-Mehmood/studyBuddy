from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import Roomserialzer
from main.models import Room
@api_view(['GET'])
def getroutes(request):
    routes = [
        'GET /api/',
        'GET /api/rooms',
        'GET /api/rooms/:id',
    ]
    return Response(routes)
@api_view(['GET'])
def getrooms(request):
    room=Room.objects.all()
    serializer=Roomserialzer(room,many=True)
    return Response(serializer.data)
@api_view(['GET'])
def getroom(request,pk):
    room=Room.objects.get(id=pk)
    serializer=Roomserialzer(room,many=False)
    return Response(serializer.data)