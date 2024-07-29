from datetime import datetime, timedelta

import pytz
from django.urls import reverse  # Import reverse for URL resolution
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .models import Event, StatusChoice, SellModeChoice
from .serializers import EventModelSerializer  # Import the actual serializer


class EventsListViewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def test_successful_event_retrieval(self):
        # Creating test Event in the db
        event = Event.objects.create(
            event_id=1,
            name="Test Event",
            start_date=datetime.now(pytz.utc),
            end_date=datetime.now(pytz.utc) + timedelta(hours=3),
            sell_mode=SellModeChoice.ONLINE,
            status=StatusChoice.ACTIVE,
        )

        # Test successful retrieval using reverse for URL resolution
        url = reverse("main:events-list") + "?start_date=2024-07-28&end_date=2024-07-29"
        response = self.client.get(url)

        # Validating response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serialized_data = EventModelSerializer(event).data  # Serialize the test Event
        self.assertEqual(
            len(response.data), len([serialized_data])
        )  # if retrieved data match with serialized data
        self.assertEqual(
            response.data[0]["name"], serialized_data.get("name")
        )  # if retrieved data matched with serialized data

    def test_invalid_parameters(self):
        # Testing missing parameters
        url = reverse("main:events-list")
        response = self.client.get(url)

        # Validate response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {
                "error": "Provide start_date & end_date in YYYY-MM-DD format."
            },
        )
