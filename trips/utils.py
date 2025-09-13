
import openrouteservice
from django.conf import settings
import datetime

def generate_route(trip):
    client = openrouteservice.Client(key=settings.ORS_API_KEY)

    # Convert addresses to coordinates
    current_coords = geocode_address(trip.current_location)
    pickup_coords = geocode_address(trip.pickup_location)
    dropoff_coords = geocode_address(trip.dropoff_location)

    coords = [current_coords, pickup_coords, dropoff_coords]

    route = client.directions(
        coordinates=coords,
        profile='driving-hgv',  # truck profile
        format='geojson',
        instructions=True
    )

    geometry = route["features"][0]["geometry"]
    summary = route["features"][0]["properties"]["summary"]
    instructions = route["features"][0]["properties"]["segments"][0]["steps"]

    return {
        "geometry": geometry,
        "distance_km": summary["distance"] / 1000,
        "duration_hr": summary["duration"] / 3600,
        "instructions": [
            {"text": step["instruction"], "distance": step["distance"], "duration": step["duration"]}
            for step in instructions
        ]
    }
def generate_eld_logs(trip):
    """
    Generate simple ELD logs for a trip based on driving rules.
    Assumptions:
    - Max 11 driving hrs/day
    - 10 hrs rest/day
    - 1 hr pickup/drop-off (on first day only)
    """
    logs = []
    # Let's assume trip distance implies ~20 total driving hrs (just example).
    # Later you can calculate from route distance/duration.
    total_driving_hours = 20  
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
