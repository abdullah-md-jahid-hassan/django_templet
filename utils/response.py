from re import DEBUG
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from my_django.settings import DEBUG
from rest_framework.exceptions import APIException
from django.core.exceptions import ValidationError as DjangoValidationError
from utils.debug import request_error


def _serialize_exception(exc: Exception):
    """
    Convert different exception types into a clean, serializable format.
    """
    if isinstance(exc, DjangoValidationError):
        return exc.messages

    if isinstance(exc, APIException):
        return exc.detail

    if isinstance(exc, dict):
        return exc

    if isinstance(exc, list):
        return exc

    return str(exc)


def success_response(message="Success", data=None, status_code=status.HTTP_200_OK):
    return Response(
        {"success": True, "message": message, "data": data}, status=status_code
    )


def error_response(
    *,
    message: str = "Something went wrong.",
    errors: Exception | None = None,
    data=None,
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    request: Request | None = None,
):
    response = {
        "success": False,
        "message": message,
        "errors": _serialize_exception(errors) if errors else None,
        "data": data,
    }

    # DEBUG MODE: rich diagnostics
    if DEBUG and errors is not None:
        response["debug"] = request_error(errors=errors, request=request)

    return Response(response, status=status_code)
