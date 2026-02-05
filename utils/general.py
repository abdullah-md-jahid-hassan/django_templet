from typing import Any
from rest_framework import status
from utils.response import error_response


def get_or_400(data: dict, required_keys: list):
    values = {}
    missing_keys = []

    for key in required_keys:
        value = data.get(key, None)
        if value is None:
            missing_keys.append(key)
        else:
            values[key] = value

    if missing_keys:
        return (
            status.HTTP_400_BAD_REQUEST,
            error_response(
                message=f"Missing required field(s): {', '.join(missing_keys).replace(' ', '_').title()}",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        )

    return (status.HTTP_200_OK, values)


def availability_check(data: dict)->tuple:
    missing_keys = []
    for key, value in data.items():
        if value is None:
            missing_keys.append(key)
    if missing_keys:
        return False, error_response(
                message=f"Data is not available for: {', '.join(missing_keys).replace(' ', '_').title()}",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
    return True, None
    


def str_replace_from_dict(text: str, replacements: dict[str, str]) -> str:
    """
    Docstring for str_replace_from_dict
    
    :param text: Description
    :type text: str
    :param replacements: Description
    :type replacements: dict[str, str]
    :return: Description
    :rtype: str
    """
    for key, value in replacements.items():
        text = text.replace(key, str(value))
    return text


def update_record(qs:object, data: dict[str, Any]) -> object:
    qs.update(**data)
    return qs