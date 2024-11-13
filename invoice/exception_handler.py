import logging
from functools import wraps
from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError


logger = logging.getLogger('myapp')


def handle_exceptions(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except ValidationError as e:
            # Handle specific ValidationError
            logger.exception("Validation error occurred in the view: %s", view_func.__name__)
            return JsonResponse(
                {"error": "Invalid data provided.", "details": e.detail},
                status=status.HTTP_400_BAD_REQUEST
            )
        except IntegrityError as e:
            logger.exception("Integrity error occurred in the view: %s", view_func.__name__)
            return JsonResponse(
                {"error": "Database integrity error.", "details": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except KeyError as e:
            logger.exception("Key error occurred in the view: %s", view_func.__name__)
            return JsonResponse(
                {"error": f"Missing key: {str(e)} in the request."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.exception("An unexpected error occurred in the view: %s", view_func.__name__)
            logger.error(f"Error details: {str(e)}")
            return JsonResponse(
                {"error": "An unexpected error occurred. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    return wrapper
