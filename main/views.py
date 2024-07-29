from django.core.cache import cache
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Event, StatusChoice, SellModeChoice
from .serializers import EventModelSerializer


class EventsListView(APIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "start_date",
                openapi.IN_QUERY,
                description="Start date (YYYY-MM-DD) to filter events",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
                required=True,
            ),
            openapi.Parameter(
                "end_date",
                openapi.IN_QUERY,
                description="End date (YYYY-MM-DD) to filter events",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description="Successful fetching of events",
                schema=EventModelSerializer(many=True),
            ),
            400: openapi.Response(
                description="Invalid request parameters",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
            ),
            500: openapi.Response(description="Internal server error"),
        },
    )
    def get(self, request, *args, **kwargs):
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        if start_date and end_date:
            cache_key = f"event_{start_date}_{end_date}"
            cached_data = cache.get(cache_key)

            if cached_data:
                return Response(cached_data)

            try:
                events_qs = Event.objects.filter(
                    start_date__date__gte=start_date,
                    end_date__date__lte=end_date,
                    sell_mode=SellModeChoice.ONLINE,
                )
                serializer = EventModelSerializer(events_qs, many=True)

                cache.set(cache_key, serializer.data, timeout=3600)  # Cache for 1 hour
                return Response(serializer.data)
            except Exception as e:
                return Response(
                    {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(
                {
                    "error": "Provide start_date & end_date in YYYY-MM-DD format."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
