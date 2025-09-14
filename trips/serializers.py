from rest_framework import serializers
from .models import Trip, ELDLog, Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["id", "name", "latitude", "longitude"]


class ELDLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ELDLog
        fields = "__all__"


class TripSerializer(serializers.ModelSerializer):
    current_location = LocationSerializer(read_only=True)
    pickup_location = LocationSerializer(read_only=True)
    dropoff_location = LocationSerializer(read_only=True)
    logs = ELDLogSerializer(many=True, read_only=True)

    
    current_location_input = serializers.CharField(write_only=True)
    pickup_location_input = serializers.CharField(write_only=True)
    dropoff_location_input = serializers.CharField(write_only=True)

    class Meta:
        model = Trip
        fields = "__all__"

    def create(self, validated_data):
        current_input = validated_data.pop("current_location_input")
        pickup_input = validated_data.pop("pickup_location_input")
        dropoff_input = validated_data.pop("dropoff_location_input")

        try:
            current_loc = self._get_or_create_location(current_input)
            pickup_loc = self._get_or_create_location(pickup_input)
            dropoff_loc = self._get_or_create_location(dropoff_input)

            trip = Trip.objects.create(
                current_location=current_loc,
                pickup_location=pickup_loc,
                dropoff_location=dropoff_loc,
                **validated_data
            )
            return trip
        except Exception as e:
            raise serializers.ValidationError(f"Error creating trip: {str(e)}")

    def _get_or_create_location(self, value):
        """

        """
        if not value:
            raise serializers.ValidationError("Location value cannot be empty.")
            
        try:
            # If it's an ID
            if str(value).isdigit():
                location = Location.objects.get(id=int(value))
                return location
            # If it's a name
            else:
                
                try:
                    location = Location.objects.get(name__iexact=value)
                    return location
                except Location.DoesNotExist:
                    # Create new location
                    location = Location.objects.create(name=value)
                    return location
                    
        except Location.DoesNotExist:
            raise serializers.ValidationError(f"Location with ID '{value}' not found.")
        except ValueError:
            raise serializers.ValidationError(f"Invalid location value: '{value}'.")
        except Exception as e:
            raise serializers.ValidationError(f"Error processing location '{value}': {str(e)}")