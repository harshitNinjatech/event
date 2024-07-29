import xml.etree.ElementTree as ET
import json

import requests
from celery import shared_task
from django.conf import settings

from .models import Event


@shared_task
def fetch_and_save_events():
    url = settings.PROVIDER_URL
    response = requests.get(url)
    if response.status_code == 200:
        parse_and_save_events(response.content)
        return True


def parse_and_save_events(xml_content):
    root = ET.fromstring(xml_content)
    for base_event in root.findall(".//base_event"):
        sell_mode = base_event.get("sell_mode")
        title = base_event.get("title")
        for event in base_event.findall("event"):
            event_id = int(event.get("event_id"))
            start_date = event.get("event_start_date")
            end_date = event.get("event_end_date")
            sold_out = event.get("sold_out")

            Event.objects.update_or_create(
                event_id=event_id,
                defaults={
                    "name": title,
                    "start_date": start_date,
                    "end_date": end_date,
                    "sell_mode": sell_mode,
                    "status": sold_out,
                },
            )
