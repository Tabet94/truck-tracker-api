# Trip Tracker Backend

This is the backend of the Trip Tracker app, built with **Django** and **Django REST Framework**.  
It handles trip creation, generates truck routes using OpenRouteService, and produces ELD logs for drivers.

---

## **Features**

- Create trips with current location, pickup, dropoff, and cycle hours.
- Generate route instructions using OpenRouteService API.
- Generate daily ELD logs (driving hours, rest hours, pickup/dropoff hours).
- Provides REST API endpoints to fetch trips, route, and logs.

---

## **Technologies**

- Python 3.x  
- Django 5.x  
- Django REST Framework  
- OpenRouteService API  
- SQLite (default) 

---

## **Installation**

1. Clone the repository:

```bash
git clone https://github.com/Tabet94/truck-tracker-api.git
2.Install dependencies:
pip install -r requirements.txt

Create a .env file at the project root:

DEBUG=True
SECRET_KEY=your_django_secret_key
ORS_API_KEY=your_openrouteservice_api_key

Apply migrations:
python manage.py migrate


Run the development server:
python manage.py runserver
