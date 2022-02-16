from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import EventSerializer
from events.models import Event

@api_view(['GET'])
def getEvents(request):
    print('USER:',request.user)
    events = Event.objects.all()
    serializer = EventSerializer(events,many=True)
    return Response(serializer.data)

class EventList(generics.ListCreateAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = Event.objects.all()
    serializer_class = EventSerializer
