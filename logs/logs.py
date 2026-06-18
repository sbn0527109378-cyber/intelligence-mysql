import logging

logging.basicConfig(filename="logs/app.log",
                    level=logging.DEBUG,
                    format="%(asctime)s | %(levelname)s | %(message)s"
                    )
def get_logger(name):
    return logging.getLogger(name)