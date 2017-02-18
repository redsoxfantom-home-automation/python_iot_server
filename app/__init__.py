from flask import Flask, json
from python_utils.zookeeper import ServiceAccessor
from app.api_1_0 import api_1_0
import logging
import os
import sys

# load configuration to tell us what port to use
root = os.path.realpath(os.path.dirname(__file__))
config_location = os.path.join(root,"config.json")
config_data = json.load(open(config_location))

dns = ServiceAccessor()
dns.connect()
dns.register_service("1.0","lights",str(config_data["port"]))

app = Flask(__name__)
app.register_blueprint(api_1_0.bp, url_prefix='/1.0')
formatter = logging.Formatter("%(levelname)s : [%(module)s] : %(message)s")
stdOutHandler = logging.StreamHandler(sys.stdout)
stdOutHandler.setFormatter(formatter)
app.logger.addHandler(stdOutHandler)
app.logger.setLevel(logging.DEBUG)

