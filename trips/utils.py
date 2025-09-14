import openrouteservice
from django.conf import settings
import datetime


def get_coordinates(location):
    """Return (lon, lat) tuple for openrouteservice."""
    if not location or not location.latitude or not location.longitude:
        raise ValueError(f"Location '{location}' does not have coordinates.")
    return (location.longitude, location.latitude)  # ORS expects (lon, lat)


def generate_route(trip):
    client = openrouteservice.Client(key=settings.ORS_API_KEY)

    # Use stored coordinates from Location model
    current_coords = get_coordinates(trip.current_location)
    pickup_coords = get_coordinates(trip.pickup_location)
    dropoff_coords = get_coordinates(trip.dropoff_location)

    coords = [current_coords, pickup_coords, dropoff_coords]

    route = client.directions(
        coordinates=coords,
        profile="driving-hgv",  # truck profile
        format="geojson",
        instructions=True,
    )

    geometry = route["features"][0]["geometry"]
    summary = route["features"][0]["properties"]["summary"]
    instructions = route["features"][0]["properties"]["segments"][0]["steps"]

    return {
        "geometry": geometry,
        "distance_km": summary["distance"] / 1000,
        "duration_hr": summary["duration"] / 3600,
        "instructions": [
            {
                "text": step["instruction"],
                "distance": step["distance"],
                "duration": step["duration"],
            }
            for step in instructions
        ],
    }


def generate_eld_logs(trip):
    
    logs = []
    total_driving_hours = 20  # TODO: later base this on route distance
    rest_hours_per_day = 10
    pickup_dropoff_hours = 1

    days_needed = (total_driving_hours + pickup_dropoff_hours) // 11 + 1
    start_date = trip.start_date

    for i in range(int(days_needed)):
        driving_today = min(11, total_driving_hours)
        log = {
            "trip": trip.id,
            "date": start_date + datetime.timedelta(days=i),
            "driving_hours": driving_today,
            "rest_hours": rest_hours_per_day,
            "pickup_dropoff_hours": pickup_dropoff_hours if i == 0 else 0,
        }
        total_driving_hours -= driving_today
        logs.append(log)

    return logs
