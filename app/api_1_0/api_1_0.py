from flask import Blueprint,json,request
import lifx_helper
import logging

bp = Blueprint('api_1_0_Blueprint',__name__)

@bp.route('/lights')
def get_lights():
  logging.info("Received request to get all lights")
  lights = lifx_helper.get_all_lights()
  light_data = json.jsonify([light.__dict__ for light in lights])
  logging.debug("Will return the following lights: %s" % light_data.__dict__)
  return light_data

@bp.route('/lights/<int:light_id>', methods = ['GET','POST'])
def individual_light(light_id):
   logging.info("Got request for light id %s with method %s" % (light_id, request.methog))
   if request.method == 'GET':
      return handle_get_light(light_id)
   if request.method == 'POST':
      print request.form.__dict__
      return handle_post_light(light_id,request.form)

def handle_get_light(light_id):
   light = lifx_helper.get_light(light_id)
   return json.jsonify(light.__dict__)

def handle_post_light(light_id,post_data):
   logging.info("Got Post with data: %s" % post_data.__dict__)
   lifx_helper.update_light(light_id,post_data)
   return "",202
