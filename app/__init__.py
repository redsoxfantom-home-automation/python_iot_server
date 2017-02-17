from flask import Flask, json
from python_utils.zookeeper import ServiceAccessor
from app.api_1_0 import api_1_0
import logging
import os

# load configuration to tell us what port to use
root = os.path.realpath(os.path.dirname(__file__))
config_location = os.path.join(root,"config.json")
config_data = json.load(open(config_location))

dns = ServiceAccessor()
dns.connect()
dns.register_service("1.0","lights",str(config_data["port"]))

app = Flask(__name__)
app.register_blueprint(api_1_0.bp, url_prefix='/1.0')
