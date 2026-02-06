from core.utils.health_response import health_ok_response, health_error_response
import traceback


def check_database():
    try:
        from django.db import connection
        connection.cursor()
        return health_ok_response(name="Database", message="Health OK")
    except Exception as e:
        return health_error_response(
            name="Database", 
            message="Health Error",
            errors=str(e),
            traceback=traceback.format_exc(),
        )
