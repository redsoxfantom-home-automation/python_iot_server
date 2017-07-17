from flask import Blueprint,json,request
import lifx_helper
import logging
from .. import socketio

bp = Blueprint('api_1_0_Blueprint',__name__)

@socketio.on('connect')
def handle_connect():
   logging.info("connection")

@bp.route('/lights')
def get_lights():
  logging.info("Received request to get all lights")
  lights = lifx_helper.get_all_lights()
  light_data = json.jsonify([light.__dict__ for light in lights])
  logging.debug("Will return the following lights: %s" % light_data.__dict__)
  return light_data

@bp.route('/lights/<int:light_id>', methods = ['GET','POST'])
def individual_light(light_id):
   logging.info("Got request for light id %s with method %s and data %s" % (light_id, request.method, request.data))
   if request.method == 'GET':
      return handle_get_light(light_id)
   if request.method == 'POST':
      return handle_post_light(light_id,request.get_json(force=True))

def handle_get_light(light_id):
   light = lifx_helper.get_light(light_id)
   return json.jsonify(light.__dict__)

def handle_post_light(light_id,post_data):
   lifx_helper.update_light(light_id,post_data)
   return "",202
