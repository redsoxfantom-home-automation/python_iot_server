import lifx
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
		new_l = lightJsonClass(l)
		retList.append(new_l)	
	return retList

def get_light(light_id):	
	l = client.by_id(light_id)
	new_l = lightJsonClass(l)
	return new_l

def update_light(light_id,attributes):
	l = client.by_id(light_id)
	
	hue = l.color.hue
	brightness = l.color.brightness
	saturation = l.color.saturation
	kelvin = l.color.kelvin

	for key in attributes:
		if(key == 'label'):
			l.label = attributes[key]
		if(key == 'power'):
			l.power = (attributes[key] == 'True')
		if(key == 'brightness'):
			brightness = float(attributes[key])
		if(key == 'hue'):
			hue = float(attributes[key])
		if(key == 'kelvin'):
			kelvin = int(attributes[key])
		if(key == 'saturation'):
			saturation = float(attributes[key])

	new_color = HSBK(hue,saturation,brightness,kelvin)
	l.color = new_color
