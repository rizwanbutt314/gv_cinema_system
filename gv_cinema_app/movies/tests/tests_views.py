import json

from events.models import Events

from django.test import TestCase
from django.urls import reverse_lazy
from rest_framework import status


class EventsAPIIndexTest(TestCase):
    """
        Make a GET request to endpoint "/events/" to
        1. get all events data
        2. get events using search
        3. get events using currency filter
        4. Sort events on amount filter in ascending and descending order
    """
    fixtures = ['events.json']

    def setUp(self):
        self.url = reverse_lazy('events:events_listing')

    def test_get_all_events(self):
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        api_index_data = r.json()
        self.assertIsNotNone(api_index_data)
        self.assertEqual(api_index_data['count'], 10)
        self.assertEqual(api_index_data['num_pages'], 1)
        self.assertEqual(api_index_data['results'][0]['uuid'], 'be93b325-8244-4ab4-bc60-8d774d1d4d7e')
        self.assertEqual(api_index_data['results'][0]['amount'], 1001)
        self.assertEqual(api_index_data['results'][0]['currency'], 'SLL')
        self.assertEqual(api_index_data['results'][0]['employee_first_name'], 'Andree')

    def test_get_events_using_search(self):
        r = self.client.get(self.url, {'search': 'bri'})
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        api_index_data = r.json()
        self.assertIsNotNone(api_index_data)
        self.assertEqual(api_index_data['count'], 2)
        self.assertIn('bri', api_index_data['results'][0]['employee_first_name'].lower())
        self.assertIn('bri', api_index_data['results'][1]['employee_last_name'].lower())

    def test_get_events_using_currency_filter(self):
        r = self.client.get(self.url, {'currency': 'SAR'})
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        api_index_data = r.json()
        self.assertIsNotNone(api_index_data)
        self.assertEqual(api_index_data['count'], 2)

        for record in api_index_data['results']:
            self.assertEqual(record['currency'], 'SAR')

    def test_get_events_using_ordering(self):
        # Sort events on amount filter in ascending order
        r = self.client.get(self.url, {'ordering': 'amount'})
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        api_index_data = r.json()
        self.assertIsNotNone(api_index_data)
        self.assertGreater(api_index_data['results'][-1]['amount'], api_index_data['results'][0]['amount'])

        # Sort events on amount filter in descending order
        r = self.client.get(self.url, {'ordering': '-amount'})
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        api_index_data = r.json()
        self.assertIsNotNone(api_index_data)
        self.assertGreater(api_index_data['results'][0]['amount'], api_index_data['results'][-1]['amount'])


class EventsAPIDetailTests(TestCase):
    """
        Make a GET request to endpoint "/events/<pk>/" to
        1. get event data using id
        2. update event data using id
    """
    fixtures = ['events.json']

    def setUp(self):
        self.available_event_id = 2
        self.unavailable_event_id = 20
        self.available_event_url = reverse_lazy('events:event_detail', args=(self.available_event_id,))
        self.unavailable_event_url = reverse_lazy('events:event_detail', args=(self.unavailable_event_id,))

    def test_get_event(self):
        # get existing event data using id
        r = self.client.get(self.available_event_url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        api_index_data = r.json()
        self.assertIsNotNone(api_index_data)
        self.assertEqual(api_index_data['id'], 2)
        self.assertEqual(api_index_data['uuid'], '741d3430-db11-435f-b9f0-88c8285c01cc')
        self.assertEqual(api_index_data['amount'], 7756)
        self.assertEqual(api_index_data['currency'], 'PKR')
        self.assertEqual(api_index_data['employee_first_name'], 'Niko')

        # get non-exisiting event data using id
        r = self.client.get(self.unavailable_event_url)
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

        api_index_data = r.json()
        self.assertEqual(api_index_data['detail'], 'Not found.')

    def test_update_event(self):
        # Event data before update
        event_before_update = Events.objects.get(id=self.available_event_id)
        self.assertEqual(event_before_update.status, 'P')

        # update existing event
        r = self.client.put(self.available_event_url,
                            json.dumps({'status': 'A'}),
                            content_type='application/json')
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        # Event data after update
        event_after_update = Events.objects.get(id=self.available_event_id)
        self.assertEqual(event_after_update.status, 'A')
