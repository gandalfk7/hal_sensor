#!/usr/bin/python
#prerequisites: ablib (https://github.com/tanzilli/ablib), python 2.x

import argparse
from ablib import Pin
import subprocess

tab_ablib = ['J4.1', 'J4.2', 'J4.3', 'J4.4', 'J4.5', 'J4.6', 'J4.7', 'J4.8', 'J4.9', 'J4.10', 'J4.11', 'J4.12', 'J4.13', 'J4.14', 'J4.15', 'J4.16', 'J4.17', 'J4.18', 'J4.19', 'J4.20', 'J4.21', 'J4.22', 'J4.23', 'J4.24', 'J4.25', 'J4.26', 'J4.27', 'J4.28', 'J4.29', 'J4.30', 'J4.31', 'J4.32', 'J4.33', 'J4.34', 'J4.35', 'J4.36', 'J4.37', 'J4.38', 'J4.39', 'J4.40']
tab_kernel = ['RES_5V', 'RES_VBAT', 'RES_NRST', 'RES_UsbAD-', 'RES_3V3', 'RES_UsbAD+', 'A23', 'A22', 'RES_GND', 'A21', 'A24', 'A31', 'A25', 'A30', 'A26', 'RES_UsbBD+', 'A27', 'RES_UsbBD-', 'A28', 'RES_UsbCD-', 'A29', 'RES_UsbCD+', 'A0', 'A1', 'A8', 'A7', 'A6', 'A5', 'C28', 'C27', 'C4', 'C31', 'C3', 'ADC_AD0', 'RES_1W', 'ADC_AD1', 'C1', 'ADC_AD2', 'C0', 'ADC_AD3']

parser = argparse.ArgumentParser(description='This is a test.')
parser.add_argument('-s','--sensor', help='Sensor you want to modify',required=True)
parser.add_argument('-a','--action',help='Action to apply to the sensor', required=True)
args = parser.parse_args()
 
## show values ##
print ("Sensor: %s" % args.sensor )
print ("Action: %s" % args.action )

#match between ablib pin numbering and kernel pin numbering
pos_ablib = tab_ablib.index(args.sensor)
pin_kernel_ = tab_kernel[pos_ablib]	
pin_kernel = pin_kernel_.strip()		#pin_kernel_ has spaces that needs to be stripped

#print ("pos_ablib: "), pos_ablib
#print ("pin_kernel" ),pin_kernel


def on():
	led = Pin(args.sensor,'OUTPUT')
	print ("on-ing %s" % args.sensor)
	led.on()
	pin_status = subprocess.check_output(["cat", "/sys/class/gpio/pio"+ pin_kernel +"/value"])
	if pin_status.strip() != "1" : 
		print ("ERROR! Action failed, pin status = %s" % pin_status.strip()) 
	else:
		print ("Action complete, pin status: %s" % pin_status.strip())
	
def off():
	led = Pin(args.sensor,'OUTPUT')
	print ("off-ing %s" % args.sensor)
	led.off()
	pin_status = subprocess.check_output(["cat", "/sys/class/gpio/pio"+ pin_kernel +"/value"])
        if pin_status.strip() != "0" :
                print ("ERROR! Action failed, pin status = %s" % pin_status.strip())
        else:
                print ("Action complete, pin status: %s" % pin_status.strip())	

def status():
	if "RES" in pin_kernel or "ADC" in pin_kernel: 
		print "Reserved pin: ",pin_kernel
	else:
		pin_status = subprocess.check_output(["cat", "/sys/class/gpio/pio"+ pin_kernel +"/value"])
		print ("Pin status: %s" % pin_status.strip())

options = {"off" : off,
	   "on" : on,
	   "status" : status,}

try:
	options[args.action]()
except KeyError:
    print "Unrecognized action ", args.action

