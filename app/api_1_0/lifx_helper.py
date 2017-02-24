import lifx
import logging
from lifx.color import HSBK

client = lifx.Client()

known_bulbs = [
   {
      'vid':1,
      'name':'LIFX',
      'products':[
         {
            'pid':1,
            'name':'Original 1000',
            'features': {
               'color':True
            }
         }
      ]
   }
]

class lightJsonClass(object):
   def __init__(self,light):
      self.label = light.label
      self.id = light.id
      self.power = light.power
      self.hue = light.hue
      self.saturation = light.saturation
      self.brightness = light.brightness
      self.kelvin = light.kelvin
      self.name = "UNKNOWN"
      self.vendor = "UNKNOWN"
      self.features = {}

      properties = light.properties
      bulb_data = [o for o in known_bulbs if o['vid'] == properties.vendor]
      if bulb_data:
         bulb_data = bulb_data[0]
         self.vendor = bulb_data['name']
         bulb_data = [o for o in bulb_data['products'] if o['pid'] == properties.product]
         if bulb_data:
            bulb_data = bulb_data[0]
            self.name = bulb_data['name']
            self.features = bulb_data['features']

def get_all_lights():
   retList = []
   for l in client.get_devices():
      try:
         new_l = lightJsonClass(l)
         retList.append(new_l)
      except Exception as err:
         logging.error("Error occured while getting light: {0}".format(err))
   return retList

def get_light(light_id):   
   l = client.by_id(light_id)
   new_l = lightJsonClass(l)
   return new_l

def update_light(light_id,attributes):
   l = client.by_id(light_id)
   logging.info("Got request to update light with attributes %s" % attributes)
   hue = l.color.hue
   brightness = l.color.brightness
   saturation = l.color.saturation
   kelvin = l.color.kelvin

   for key in attributes:
      if(key == 'label'):
         logging.info("Updating light label to %s" % attributes[key])
         l.label = attributes[key]
      if(key == 'power'):
         logging.info("Updating light power to %s" % attributes[key])
         l.power = attributes[key]
      if(key == 'brightness'):
         logging.info("Updating light brightness to %s" % attributes[key])
         brightness = float(attributes[key])
      if(key == 'hue'):
         logging.info("Updating light hue to %s" % attributes[key])
         hue = float(attributes[key])
      if(key == 'kelvin'):
         logging.info("Updating light kelvin to %s" % attributes[key])
         kelvin = int(attributes[key])
      if(key == 'saturation'):
         logging.info("Updating light saturation to %s" % attributes[key])
         saturation = float(attributes[key])

   new_color = HSBK(hue,saturation,brightness,kelvin)
   l.color = new_color
