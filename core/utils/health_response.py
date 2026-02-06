

def health_ok_response(
    name='Unknown',
    message="Health OK",
):
    return {
        "success": True,
        "name": name,
        "message": message,
    }


def health_error_response(
    name='Unknown',
    message="Health Error",
    errors=None,
    traceback=None,
):
    return {
        "success": False,
        "name": name,
        "message": message,
        "errors": errors,
        "traceback": traceback.splitlines(),
    }