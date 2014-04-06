#!/usr/bin/env python3

# A simple script to gradually fade in a LIFx bulb
# Made using Sharph's LIFx python library, located at https://github.com/sharph/lifx-python

import lifx
import argparse
import time

## METHODS
def ensure_light_on(light):
	if light.power == False:
		print("turning on %s" % (light.get_addr(),) )
		light.set_power(True)
	else:
		print("light already on")

def fade(light):
	brightness = start_bright
	intervals = int(round(fade_time / interval_time))
	brightness_increment = int(round((end_bright - start_bright) / intervals))

	for i in range(1, intervals):
		brightness = int(round(brightness + brightness_increment))
		print('Setting %s to hue:%s, saturation:%s, brightness:%s, kelvin:%s' % (bulb_name, hue, saturation, brightness, kelvin))
		light.set_color(light.hue, light.saturation, brightness, kelvin, interval_time*1000)
		time.sleep(interval_time)

	light.set_color(hue, saturation, end_bright, kelvin, 1)

## MAIN SCRIPT
# get args
parser = argparse.ArgumentParser(description='Fade lifx bulb in over time')
parser.add_argument('--name', 					help='Name of bulb to fade in')
parser.add_argument('--time', 	type=int, 			help='Time in seconds to take to fade in')
parser.add_argument('--start', 	type=int, 	default=0, 	help='Starting brightness (between 0 and 65535)')
parser.add_argument('--end', 	type=int, 	default=65535, 	help='End brightness (between 0 and 65535)')
parser.add_argument('--hue', 	type=int, 			help='Hue (between 0 and 65535)')
parser.add_argument('--sat', 	type=int, 			help='Saturation (between 0 and 65535)')
parser.add_argument('--kelvin',	type=int, 			help='Kelvin (between 0 and 65535)')
parser.add_argument('--int', 	type=int, 	default=5,	help='Update interval in seconds. Lower numbers are smoother but may cause glitches')

# parge args
args = parser.parse_args()
#TODO Check that arguments are all present
fade_time 	= args.time
bulb_name 	= args.name
start_bright 	= args.start
end_bright 	= args.end
interval_time 	= args.int
hue 		= args.hue
saturation	= args.sat
kelvin		= args.kelvin

light_list = lifx.get_lights()
for light in light_list:
	if light.bulb_label == args.name:
		#If hue/saturation/kelvin not set, keep the bulbs current setting
		if not hue:
			hue = light.hue
		if not saturation:
			saturation = light.saturation
		if not kelvin:
			kelvin = light.kelvin

		print('Fading in bulb %s over %i seconds' % (bulb_name, fade_time))
		light.set_color(hue, saturation, start_bright, kelvin, 10)
		ensure_light_on(light)
		fade(light)
