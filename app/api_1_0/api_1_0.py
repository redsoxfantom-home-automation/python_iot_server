from flask import Blueprint,json,request
import lifx_helper
import logging
from .. import socketio
import time
import threading

bp = Blueprint('api_1_0_Blueprint',__name__)

@socketio.on('connect')
def handle_connect():
   logging.info("Client connected to websocket")
   lights = lifx_helper.get_all_lights()
   light_data = [light.__dict__ for light in lights]
   socketio.emit('light_update',light_data)

@socketio.on('get_all_lights')
def handle_socket_get_lights():
   light_data = get_lights()
   socketio.emit('get_all_lights_response','%s' % light_data.__dict__)

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

def light_update_thread():
   logging.info("Light update thread active")
   while True:
      lights = lifx_helper.get_all_lights()
      light_data = [light.__dict__ for light in lights]
      socketio.emit('light_update',light_data,broadcast=True)
      time.sleep(5)

t = threading.Thread(target=light_update_thread)
t.daemon = True
t.start()
