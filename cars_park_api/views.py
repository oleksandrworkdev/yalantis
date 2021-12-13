from django.http import JsonResponse, HttpRequest
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from .models import Driver, Vehicle
from .helpers import response_with_message
from .converters import driver_to_dict, vehicle_to_dict


def driver_index(request: HttpRequest):
    if request.method == 'GET':
        created_at__gte = request.GET.get('created_at__gte', None)
        created_at__lte = request.GET.get('created_at__lte', None)
        if created_at__gte:
            drivers = Driver.get_created_at__gte(created_at__gte)
        elif created_at__lte:
            drivers = Driver.get_created_at__lte(created_at__lte)
        else:
            drivers = Driver.objects.all()

        return JsonResponse({'drivers': [driver_to_dict(d) for d in drivers]})
    elif request.method == 'POST':
        first_name = request.GET.get('first_name')
        last_name = request.GET.get('last_name')
        if not first_name or not last_name:
            response_with_message('Error. Missing firstname or lastname.')
        else:
            try:
                new_driver = Driver(first_name=first_name, last_name=last_name)
                new_driver.save()
                response_with_message(f'Successfully created {new_driver}', payload=driver_to_dict(new_driver))
            except Exception as err:
                response_with_message('Error. Creating driver failed.', payload=err, error=True)
    else:
        response_with_message('Error. Unsupported method.', True)


def driver_detail(request: HttpRequest, driver_id):
    driver = get_object_or_404(Driver, pk=driver_id)
    if request.method == 'GET':
        return JsonResponse({'driver': driver_to_dict(driver)})
    elif request.method == 'UPDATE':
        driver.first_name = request.POST.get('first_name', driver.first_name)
        driver.last_name = request.POST.get('last_name', driver.last_name)
        try:
            driver.save()
            response_with_message(f'Successfully updated {driver}', payload=driver_to_dict(driver))
        except Exception as err:
            response_with_message('Error. Updating driver failed.', payload=err, error=True)

    elif request.method == 'DELETE':
        driver.delete()
        response_with_message(f'Successfully deleted driver {driver}')
    else:
        response_with_message('Error. Unsupported method.', True)


def vehicle_index(request: HttpRequest):
    if request.method == 'GET':
        with_drivers = request.GET.get('with_drivers', None)
        if with_drivers:
            vehicles = Vehicle.objects.filter(driver__isnull=with_drivers == 'no')
        else:
            vehicles = Vehicle.objects.all()
        return JsonResponse({'vehicles': [vehicle_to_dict(v) for v in vehicles]})
    elif request.method == 'POST':
        make = request.POST.get('make')
        model = request.POST.get('model')
        plate_number = request.POST.get('plate_number')
        if not make or not model or not plate_number:
            response_with_message('Error. Missing make or model or plate_number.')
        else:
            try:
                new_vehicle = Vehicle(make=make, model=model, plate_number=plate_number)
                new_vehicle.save()
                response_with_message(f'Successfully created {new_vehicle}', payload=vehicle_to_dict(new_vehicle))
            except Exception as err:
                response_with_message('Error. Creating vehicle failed.', payload=err, error=True)
    else:
        response_with_message('Error. Unsupported method.', True)


def vehicle_detail(request: HttpRequest, vehicle_id):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    if request.method == 'GET':
        return JsonResponse({'vehicle': vehicle_to_dict(vehicle)})
    elif request.method == 'UPDATE':
        vehicle.make = request.POST.get('make', vehicle.make)
        vehicle.model = request.POST.get('model', vehicle.model)
        vehicle.plate_number = request.POST.get('plate_number', vehicle.plate_number)
        try:
            vehicle.save()
            response_with_message(f'Successfully updated {vehicle}', payload=vehicle_to_dict(vehicle))
        except Exception as err:
            response_with_message('Error. Updating vehicle failed.', payload=err, error=True)
    elif request.method == 'DELETE':
        vehicle.delete()
        response_with_message(f'Successfully deleted vehicle {vehicle}')
    else:
        response_with_message('Error. Unsupported method.', True)


def vehicle_set_driver(request: HttpRequest, vehicle_id):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    if request.method == 'POST':
        driver_id = request.POST.get('driver_id')
        driver = None
        if driver_id:
            try:
                driver = Driver.objects.get(pk=driver_id)
            except ObjectDoesNotExist as err:
                return response_with_message('Error. Setting vehicle driver failed.', payload=err, error=True)
        vehicle.driver = driver
        try:
            vehicle.save()
            response_with_message(f'Successfully set driver for vehicle {vehicle}')
        except Exception as err:
            response_with_message('Error. Setting vehicle driver failed.', payload=err, error=True)
    else:
        response_with_message('Error. Unsupported method.', True)
