#!/usr/bin/env python3

from prometheus_client import start_http_server, Summary, Gauge
from prometheus_client import Gauge
from time import sleep
import random
import time
import logging
import sys

# Create a metric to track time spent and requests made.
# REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
HUMIDITY = Gauge('relative_humidity', 'Relative Humidity')
TEMPERATURE = Gauge('temperature', 'Temperature')

logger = logging.getLogger(sys.argv[0])
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

# Decorate function with metric.
#@HUMIDITY
#def process_request(t):
#  logger.info('HUMIDITY')

#@TEMPERATURE
#def process_request(t):
#  logger.info('HUMIDITY')

def update_gauges():
  logger.info('update_gauges')
  HUMIDITY.set(4.2)
  TEMPERATURE.set(4.2)

if __name__ == '__main__':
  print("initalise gauges")
  update_gauges()
  logger.debug('Startup')
  # Start up the server to expose the metrics.
  start_http_server(8000)
  logger.debug('Prometheus server started')
  
  while True:
    sleep(60)
    update_gauges()

