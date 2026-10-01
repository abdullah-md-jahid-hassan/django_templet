
# entrypoint.sh

#!/bin/sh
set -e

# Ensure virtualenv is active
export PATH="/venv/bin:$PATH"

# Only web container should run migrations
if [ "$RUN_MIGRATIONS" = "true" ]; then
    echo "Applying database migrations..."
    python manage.py migrate --noinput
fi

# Execute passed command (gunicorn / celery)
exec "$@"
