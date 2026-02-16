import traceback
from celery import current_app
from core.utils.health_response import health_ok_response, health_error_response


def check_celery_worker():
    try:
        inspect = current_app.control.inspect()
        response = inspect.ping()

        if not response:
            raise Exception("No active Celery workers detected")

        return health_ok_response(
            name="Celery Worker",
            message=f"{len(response)} worker(s) active"
        )

    except Exception as e:
        return health_error_response(
            name="Celery Worker",
            message="Health Error",
            errors=e,
        )

def check_celery_beat():
    try:
        # Safely read beat_schedule; treat missing/None as empty
        schedule = getattr(current_app.conf, 'beat_schedule', None)
        if schedule is None:
            schedule = {}

        # Some configurations may use non-mapping types; guard len()
        try:
            count = len(schedule)
        except Exception:
            count = 0

        # Return a healthy response even if there are zero configured tasks
        return health_ok_response(
            name="Celery Beat",
            message=f"{count} scheduled task(s) configured"
        )

    except Exception as e:
        return health_error_response(
            name="Celery Beat",
            message="Health Error",
            errors=traceback.format_exc(),
        )
