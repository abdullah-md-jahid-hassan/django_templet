from functools import wraps
from rest_framework import status
from core.utils.response import error_response


def admin_required(view_func):
    """
    Decorator to check if user is admin.
    For now, it does nothing and always allows access.
    Logic will be implemented later.
    """
    # Check if it's a class (used as @admin_required on a class)
    if isinstance(view_func, type):
        # For class-based views, just return the class as-is for now
        return view_func
    
    # For function-based views (methods)
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        # TODO: Implement admin check logic here
        # For now, always allow access
        return view_func(*args, **kwargs)
    
    return wrapper
    