import os
import queue
import atexit
import logging
from logging.handlers import QueueHandler, QueueListener

class CustomQueueHandler(QueueHandler):
    """
    Wraps standard QueueHandler to dynamically resolve and load handler dependencies
    when Django executes logging dictConfig, preventing initialization order issues.
    """
    def __init__(self, handlers, respect_handler_level=False, queue_obj=None):
        if queue_obj is None:
             queue_obj = queue.Queue(-1) # Infinite queue
        super().__init__(queue_obj)
        
        self.handler_names = handlers
        self.respect_handler_level = respect_handler_level
        self._listener = None
        
    def _resolve_handlers(self):
         resolved = []
         for name in self.handler_names:
            h = logging._handlers.get(name)
            if h:
                resolved.append(h)
         return resolved

    def emit(self, record):
        if not self._listener:
            # Lazy initialize the listener thread to ensure all other formatted are loaded
            resolved_handlers = self._resolve_handlers()
            if resolved_handlers:
                self._listener = QueueListener(
                    self.queue, 
                    *resolved_handlers, 
                    respect_handler_level=self.respect_handler_level
                )
                self._listener.start()
                # Stop listener safely when Django shuts down
                atexit.register(self._listener.stop) 
            
        return super().emit(record)


def get_logging_config(service_name="web", logs_dir=None, log_level="INFO"):
    """
    Exportable logging configuration for settings.py.
    Usage: LOGGING = get_logging_config()
    """
    if not logs_dir:
        from django.conf import settings
        logs_dir = os.path.join(getattr(settings, "BASE_DIR", "."), "logs_output")
        
    os.makedirs(logs_dir, exist_ok=True)

    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "()": "logs.formatters.JSONFormatter",
            },
            "console": {
                "format": "[{levelname}] {asctime} {name} | {message}",
                "style": "{",
            },
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "console",
            },
            # File Rotation
            "file_app": {
                "level": "INFO",
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": os.path.join(logs_dir, "app.json"),
                "when": "midnight",
                "interval": 1,
                "backupCount": 30, # Keep last 30 days
                "formatter": "json",
            },
            "file_error": {
                "level": "ERROR",
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": os.path.join(logs_dir, "error.json"),
                "when": "midnight",
                "interval": 1,
                "backupCount": 30,
                "formatter": "json",
            },
            # Custom DB Logging Handler
            "database": {
                "level": "INFO",
                "class": "logs.handlers.DatabaseHandler",
                # Output to Django standard DB (SystemLog)
            },
            
            # Non-blocking Async Queue Handler
            "queue_listener": {
                "class": "logs.logging_config.CustomQueueHandler",
                "handlers": ["file_app", "file_error", "database", "console"],
                "respect_handler_level": True,
            },
        },
        "loggers": {
            "django": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            },
            "django.logs.app": {  # Dedicated logger for our app's helper functions
                "handlers": ["queue_listener"],
                "level": log_level,
                "propagate": False,
            },
        },
    }
    
    return config
