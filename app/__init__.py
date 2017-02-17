from flask import Flask
from python_utils.zookeeper import ServiceAccessor
from app.api_1_0 import api_1_0
import logging

dns = ServiceAccessor()
dns.connect()
dns.register_service("1.0","lights","5000")

app = Flask(__name__)
app.register_blueprint(api_1_0.bp, url_prefix='/1.0')
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)
