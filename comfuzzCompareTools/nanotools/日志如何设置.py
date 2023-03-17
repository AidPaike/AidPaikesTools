import logging

logger = logging.getLogger()

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Setup file handler
fhandler = logging.FileHandler('my.log')
fhandler.setLevel(logging.DEBUG)
fhandler.setFormatter(formatter)

# Configure stream handler for the cells
chandler = logging.StreamHandler()
chandler.setLevel(logging.DEBUG)
chandler.setFormatter(formatter)

# Add both handlers
logger.addHandler(fhandler)
# logger.addHandler(chandler)
logger.setLevel(logging.DEBUG)

# Show the handlers
# print(logger.handlers)

# Log Something
logger.info("Test info")
logger.debug("Test debug")
logger.error("Test error")