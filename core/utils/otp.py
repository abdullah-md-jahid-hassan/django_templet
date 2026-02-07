import hashlib
from core.clients import redis_client

OTP_TTL_SECONDS = 300  # 5 minutes


def _otp_key(purpose: str, identifier: str) -> str:
    """
    Docstring for _otp_key
    Args:
        purpose (str): The purpose of the OTP.
        identifier (str): The identifier for the OTP.
    Returns:
        str: The OTP key.
    """
    hashed = hashlib.sha256(identifier.encode()).hexdigest()
    return f"otp:{purpose}:{hashed}"


def set_otp(purpose: str, identifier: str, otp: str) -> None:
    """
    Docstring for set_otp
    
    Args:
        purpose (str): The purpose of the OTP.
        identifier (str): The identifier for the OTP.(email/number)
        otp (str): The OTP to set.
    """
    key = _otp_key(purpose, identifier)
    redis_client.set(
        name=key,
        value=otp,
        ex=OTP_TTL_SECONDS,
    )


def get_otp(purpose: str, identifier: str) -> str | None:
    """
    Docstring for get_otp
    
    Args:
        purpose (str): The purpose of the OTP.
        identifier (str): The identifier for the OTP.(email/number)
    Returns:
        str | None: The OTP if it exists, None otherwise.
    """
    key = _otp_key(purpose, identifier)
    return redis_client.get(key)


def otp_exists(purpose: str, identifier: str) -> bool:
    """
    Docstring for otp_exists
    
    Args:
        purpose (str): The purpose of the OTP.
        identifier (str): The identifier for the OTP.
    Returns:
        bool: True if the OTP exists, False otherwise.
    """
    key = _otp_key(purpose, identifier)
    return redis_client.exists(key) == 1


def delete_otp(purpose: str, identifier: str) -> None:
    """
    Docstring for delete_otp

    Args:
        purpose (str): The purpose of the OTP.
        identifier (str): The identifier for the OTP.
    """
    key = _otp_key(purpose, identifier)
    redis_client.delete(key)
