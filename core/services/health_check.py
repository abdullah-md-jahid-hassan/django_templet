from core.health import (
    check_email_service,
    check_database,
)

def health_report():
    health = [
        check_email_service(),
        check_database(),
    ]

    success_count = 0
    fail_count = 0
    for service in health:
        if service["success"]:
            success_count += 1
        else:
            fail_count += 1

    return {
        "success_count": success_count,
        "fail_count": fail_count,
        "services": health,
    }
