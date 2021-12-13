from django.http import JsonResponse


def response_with_message(message, payload=None, error=False):
    return JsonResponse({
        'message': message,
        'payload': payload,
        'error': error
    })
