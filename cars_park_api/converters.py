from .models import Driver, Vehicle

DATE_FORMAT = '%d/%m/%Y'
DATE_TIME_FORMAT = '%d/%m/%Y %H:%M:%S'


def driver_to_dict(driver: Driver):
    return {
        'id': driver.id,
        'first_name': driver.first_name,
        'last_name': driver.last_name,
        'created_at': driver.created_at.strftime(DATE_TIME_FORMAT),
        'updated_at': driver.updated_at.strftime(DATE_TIME_FORMAT),
    }


def vehicle_to_dict(vehicle: Vehicle):
    return {
        'id': vehicle.id,
        'driver_id': vehicle.driver.id if vehicle.driver else None,
        'make': vehicle.make,
        'model': vehicle.model,
        'plate_number': vehicle.plate_number,
        'created_at': vehicle.created_at.strftime(DATE_TIME_FORMAT),
        'updated_at': vehicle.updated_at.strftime(DATE_TIME_FORMAT),
    }
