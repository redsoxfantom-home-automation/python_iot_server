from flask import Blueprint,json,request
import lifx_helper

bp = Blueprint('api_1_0_Blueprint',__name__)

@bp.route('/lights')
def get_lights():
  lights = lifx_helper.get_all_lights()
  return json.jsonify([light.__dict__ for light in lights])

@bp.route('/lights/<int:light_id>', methods = ['GET','POST'])
def individual_light(light_id):
   if request.method == 'GET':
      return handle_get_light(light_id)
   if request.method == 'POST':
      print request.form.__dict__
      return handle_post_light(light_id,request.form)

def handle_get_light(light_id):
   light = lifx_helper.get_light(light_id)
   return json.jsonify(light.__dict__)

def handle_post_light(light_id,post_data):
   lifx_helper.update_light(light_id,post_data)
   return "",202
