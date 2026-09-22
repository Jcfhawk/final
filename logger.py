import logging

logging.basicConfig(
    filename="errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def error_log(error):
    logging.exception("Error while processing %s", error)