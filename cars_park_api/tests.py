from datetime import datetime
from django.urls import reverse
from django.test import TestCase
from django.utils import timezone
from .models import Driver, Vehicle
from .converters import driver_to_dict, vehicle_to_dict


def create_driver(first_name, last_name, created_at=None):
    return Driver.objects.create(first_name=first_name, last_name=last_name, created_at=created_at)


def create_vehicle(make, model, plate_number, driver=None):
    return Vehicle.objects.create(make=make, model=model, plate_number=plate_number, driver=driver)


class DriverIndexViewTests(TestCase):
    def test_no_drivers(self):
        response = self.client.get(reverse('cars_park_api:driver_index'))
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response.json()['drivers'], [])

    def test_drivers(self):
        d1 = create_driver("Tom", "Jerry")
        response = self.client.get(reverse('cars_park_api:driver_index'))
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response.json()['drivers'], [driver_to_dict(d1)])

    def test_drivers_created_at_gte(self):
        d1 = create_driver("Tom", "Jerry")
        d2 = create_driver("Tom", "Hank")
        d1.created_at = datetime(2021, 1, 1, tzinfo=timezone.get_current_timezone())
        d1.save()
        response = self.client.get(reverse('cars_park_api:driver_index') + f'?created_at__gte=15-10-2021')
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response.json()['drivers'], [driver_to_dict(d2)])


class VehicleIndexViewTests(TestCase):
    def test_no_vehicles(self):
        response = self.client.get(reverse('cars_park_api:vehicle_index'))
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response.json()['vehicles'], [])

    def test_vehicles(self):
        v1 = create_vehicle("AUDI", "TT", "AO 3405 KO")
        response = self.client.get(reverse('cars_park_api:vehicle_index'))
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response.json()['vehicles'], [vehicle_to_dict(v1)])

    def test_vehicles_with_drivers_yes(self):
        v1 = create_vehicle("AUDI", "TT", "AO 3403 KO", driver=create_driver("Miki", "Mouse"))
        create_vehicle("AUDI", "TT", "AO 3404 KO")
        response = self.client.get(reverse('cars_park_api:vehicle_index') + '?with_drivers=yes')
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response.json()['vehicles'], [vehicle_to_dict(v1)])

    def test_vehicles_with_drivers_no(self):
        create_vehicle("AUDI", "TT", "AO 3403 KO", driver=create_driver("Miki", "Mouse"))
        v2 = create_vehicle("AUDI", "TT", "AO 3404 KO")
        response = self.client.get(reverse('cars_park_api:vehicle_index') + '?with_drivers=no')
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response.json()['vehicles'], [vehicle_to_dict(v2)])

    def test_vehicles_delete(self):
        v1 = create_vehicle("AUDI", "TT", "AO 3403 KO", driver=create_driver("Miki", "Mouse"))
        create_vehicle("AUDI", "TT", "AO 3404 KO")
        response = self.client.delete(reverse('cars_park_api:vehicle_detail', args=(v1.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Successfully deleted')

    def test_vehicles_detail(self):
        v1 = create_vehicle("AUDI", "TT", "AO 3403 KO", driver=create_driver("Miki", "Mouse"))
        response = self.client.get(reverse('cars_park_api:vehicle_detail', args=(v1.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json()['vehicle'], vehicle_to_dict(v1))
