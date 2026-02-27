import logging
import sys

# create formatter
formatter = logging.Formatter(
    fmt="%(asctime)s.%(msecs)03d [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# get root logger
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

# delete all old handlers
for handler in root_logger.handlers[:]:
    root_logger.removeHandler(handler)

# create new stream handler (stdout)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
root_logger.addHandler(handler)

# create own logger for project
logger = logging.getLogger("ai-assistant-api")
