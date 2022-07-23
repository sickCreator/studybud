# from django.http import JsonResponse
# JSON stands for javascript object notation and provides
# for a way to represent data
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer
# this view will show us all the routes in the API


@api_view(['GET'])
def getRoute(request):
    routes = [
        # will get home page
        'GET /api',
        # api for seeing all rooms in the application
        # JSON object for all the rooms in the application
        'GET /api/rooms',
        # get a specific room/single object/specific object info
        'GET /api/rooms/:id'

    ]
    # this Json Response will allow to object to be conjerted t
    return Response(routes)


@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    # pass object as well as  many (if multiple objects to serialize or one object)
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getRoom(request, room_id):
    room = Room.objects.get(id=room_id)
    # pass object as well as  many (if multiple objects to serialize or one object)
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data)
