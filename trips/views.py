from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Trip, ELDLog
from .serializers import TripSerializer
from .utils import generate_route, generate_eld_logs

class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer  

    def create(self, request, *args, **kwargs):
        """
        Create a trip
        """
        serializer = TripSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        trip = serializer.save()

        try:
            # Generate ELD logs
            logs_data = generate_eld_logs(trip)
            for log in logs_data:
                ELDLog.objects.create(
                    trip=trip,
                    date=log["date"],
                    driving_hours=log["driving_hours"],
                    rest_hours=log["rest_hours"],
                    pickup_dropoff_hours=log["pickup_dropoff_hours"]
                )

            # Generate route 
            route_data = generate_route(trip)

        except Exception as e:
            # If geocoding/routing fails, return error
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    
        response_data = TripSerializer(trip).data
        response_data['route'] = route_data
        return Response(response_data)

    def retrieve(self, request, *args, **kwargs):
        """
        
        """
        trip = self.get_object()
        try:
            route_data = generate_route(trip)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        response_data = TripSerializer(trip).data
        response_data['route'] = route_data
        return Response(response_data)
