from rest_framework.viewsets import ModelViewSet
from airport.models import *
from airport.api.serializers import *
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from django.views.decorators.cache import cache_page, cache_control



class AirportViewSet(ModelViewSet):
    serializer_class = AirportSerializer
    queryset = Airport.objects.all()
    pagination_class = None
    

    # @method_decorator(cache_page(60*1))
    def list(self, request):
        queryset = Airport.objects.all()
        serializer = AirportSerializer(queryset, many=True)
        return Response(serializer.data)