from flask import Flask, json
from python_utils.zookeeper import ServiceAccessor
from app.api_1_0 import api_1_0
import logging
import os
import sys

def determineLogLevel(levelStr):
   return {
      'error': logging.ERROR,
      'warning': logging.WARNING,
      'info': logging.INFO,
      'debug': logging.DEBUG
   }[levelStr]

# load configuration to tell us what port to use
root = os.path.realpath(os.path.dirname(__file__))
config_location = os.path.join(root,"config.json")
config_data = json.load(open(config_location))

# setup logger
logLevel = determineLogLevel(config_data["logLevel"])
logging.basicConfig(format="%(levelname)s [%(module)s] : %(message)s", level=logLevel)
logging.info("Successfully loaded config")

dns = ServiceAccessor()
dns.connect()
dns.register_service("1.0","lights",str(config_data["port"]))
dns.register_service("1.0","switches",str(config_data["port"]))
logging.info("Successfully registered with service accessor. Port number: %s" % config_data['port'])

app = Flask(__name__)
app.register_blueprint(api_1_0.bp, url_prefix='/1.0')
logging.info("Successfully registered api_1_0 at /1.0")
