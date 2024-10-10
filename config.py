import logging

logger = logging.getLogger("ReelTalk")
# Set the level of the logger (DEBUG, INFO, WARNING, ERROR, CRITICAL)
logger.setLevel(logging.DEBUG)


# Create a console handler
console_handler = logging.StreamHandler()

# Create a formatter to include timestamp, logger name, level, function name, line number, and the message
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s:%(lineno)d] - %(message)s"
)
console_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(console_handler)
