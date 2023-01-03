import json
import operator
from django.http import JsonResponse
from django.shortcuts import render
import requests
from rest_framework.views import APIView
from math import radians, cos, sin, asin, sqrt
from rest_framework.response import Response
from datetime import datetime
from rest_framework import status
from .models import Airport
# Create your views here.
EXTERNAL_API_URL = "http://stub.2xt.com.br/air/search/pzrvlDwoCwlzrWJmOzviqvOWtm4dkvuc"
EXTERNAL_API_USER = "demo"
EXTERNAL_API_PSWD = "swnvlD"

class FlightQueryView(APIView):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        
    def get(self, request, *args, **kwargs) -> Response:
        self.origin = request.query_params.get("origin")
        self.destination = request.query_params.get("destination")
        self.departure_date = request.query_params.get("departure_date")
        self.return_date = request.query_params.get("return_date")
        error_message = self.validate()
        if error_message:
            return Response(
                {"error": error_message},
                status=status.HTTP_400_BAD_REQUEST
            )

        response = self.main()
        response.sort(key=operator.itemgetter('price'))
        return Response({'options': response})
    
    def main(self):
        self.getApiData()
        
        self.all_going_flights = self.going_flights_data["options"]
        self.all_return_flights = self.return_flights_data["options"]

        for flight in self.all_going_flights:
            flight = self.calculateParams(flight)

        for flight in self.all_return_flights:
            flight = self.calculateParams(flight)
      
        result = []
        for going_flight in self.all_going_flights:
            for return_flight in self.all_return_flights:
                option = { }
                option["price"] = round(return_flight["price"]["total"] + going_flight["price"]["total"],2)
                option["going_flight"] = going_flight
                option["return_flight"] = return_flight
                result.append(option)
        
        return result
        
    def validate(self) -> str:
        """this method returns the error message in case of something goes wrong or None if everything goes right"""
        conditions = [
            {
                "condition": not self.origin or not self.destination,
                "message": "Both origin and destination airports must be informed."
            },
            {   
                "condition": not self.return_date or not self.departure_date,
                "message": "Both departure and return date must be informed."
            },
            {
                "condition": self.origin == self.destination, 
                "message": "The origin and destination airport cannot be the same."
            },
            {
                "condition": len(Airport.objects.filter(iata=self.origin)) == 0, 
                "message":  f"The origin Airport {self.origin} is not registered in our database."
            },
            {
                "condition": len(Airport.objects.filter(iata=self.destination)) == 0, 
                "message":  f"The destination Airport {self.destination} is not registered in our database."
            },
            {
                "condition":  datetime.strptime(self.departure_date, '%Y-%m-%d') < datetime.now() if self.departure_date else True, 
                "message": "The departure date cannot be earlier than today's date",
            },
            {
                "condition": datetime.strptime(self.return_date, '%Y-%m-%d') < datetime.strptime(self.departure_date, '%Y-%m-%d') if self.return_date else True , 
                "message":  "The return date cannot be earlier than the departure date.",
            },
        ]
        
        for condition in conditions:
            if condition["condition"]:
                return condition["message"]
            
        return None
        
    def getApiData(self):
        request_going = requests.get(
            url=f"{EXTERNAL_API_URL}/{self.origin}/{self.destination}/{self.departure_date}",
            auth=(EXTERNAL_API_USER,EXTERNAL_API_PSWD)
        )
        self.going_flights_data = json.loads(request_going.content)
        
        request_return = requests.get(
            url=f"{EXTERNAL_API_URL}/{self.destination}/{self.origin}/{self.return_date}",
            auth=(EXTERNAL_API_USER,EXTERNAL_API_PSWD)
        )
        self.return_flights_data = json.loads(request_return.content)
    
    def calculateParams(self, flight):
        self.calculatePrice(flight["price"])
        self.calculateMeta(flight)
    
    def harversine(self, lat1, lon1, lat2, lon2):
        R = 6372.8

        dLat = radians(lat2 - lat1)
        dLon = radians(lon2 - lon1)
        lat1 = radians(lat1)
        lat2 = radians(lat2)

        a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
        c = 2*asin(sqrt(a))

        return R * c
    
    def calculateDuration(self,meta):
        dep_time = datetime.strptime(meta["departure_time"], '%Y-%m-%dT%H:%M:%S')
        arr_time = datetime.strptime(meta["arrival_time"], '%Y-%m-%dT%H:%M:%S')
        
        duration = arr_time - dep_time
        duration_in_s = duration.total_seconds()  
        return duration_in_s/3600
    
    def calculatePrice(self, price):
        if price["fare"] * 0.1 < 40.0:
            price["fees"] = 40.0
        else:
            price["fees"] = round(price["fare"] * 0.1,2)
        price["total"] = round(price["fare"] + price["fees"], 2)
        
    def calculateMeta(self, meta):
        lat_origin = self.going_flights_data["summary"]["from"]["lat"]
        lon_origin = self.going_flights_data["summary"]["from"]["lon"]
        lat_destination = self.going_flights_data["summary"]["to"]["lat"]
        lon_destination = self.going_flights_data["summary"]["to"]["lon"]
        meta["meta"]["range"] = self.harversine(lat_origin, lon_origin, lat_destination, lon_destination)
        hours = self.calculateDuration(meta)
        meta["meta"]["cruise_speed_kmh"] = round(meta["meta"]["range"]/hours,2)
        meta["meta"]["cost_per_km"] = round(meta["price"]["fare"]/meta["meta"]["range"],2)
        
        
    