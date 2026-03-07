import logging.config
import logging.handlers

class MyH(logging.handlers.QueueHandler):
    def __init__(self, *args, **kwargs):
        print(f"args length: {len(args)}")
        if args:
            print(f"args[0] type: {type(args[0])}")
        print(f"kwargs: {kwargs}")
        import queue
        super().__init__(queue.Queue(-1))

d = {
    "version": 1,
    "handlers": {
        "con": {"class": "logging.StreamHandler"},
        "q": {
            "class": "test_logging.MyH",
            "handlers": ["con"],
            "respect_handler_level": True
        }
    }
}
logging.config.dictConfig(d)
