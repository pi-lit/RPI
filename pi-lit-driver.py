# python inports
import time
import argparse
import json
import threading
import os
import math

# rpi library import
# from rpi_ws281x import *

#states
OFF = '0#0#0'
WHITE = '255#255#255'

# globals
LED_STATE_CACHE = []
COMMAND_BUFFER = {}

#initialize the led strip refresh cache with all white LED's
def initStateCache():
	for i in range(150):
		LED_STATE_CACHE.append([])
		for j in range(30):
			LED_STATE_CACHE[i].append(OFF)


#takes a single command and populates the command buffer
def populateBufferFromCustomCommand(customCommand):
	ledRange = []
	for ledNum in customCommand['range']:
		ledRange.append(ledNum)
	for timeStamp in customCommand['timestamps']:
		colorStr = ''
		r = timeStamp['color']['r']
		g = timeStamp['color']['g']
		b = timeStamp['color']['b']
		colorStr = str(r) + '#' + str(g) + '#' + str(b)
		refreshForCache = int(math.floor(timeStamp['time'] * 15) / 1000)
		COMMAND_BUFFER[refreshForCache] = {"LED_RANGE" : ledRange, "COLOR" : colorStr}

	
def loadCacheFromBuffer():
	ledRange = []
	currentColor = OFF
	for refresh in range(150):
		if COMMAND_BUFFER.get(refresh) != None:
			currentColor = COMMAND_BUFFER[refresh]['COLOR']
			ledRange = COMMAND_BUFFER[refresh]['LED_RANGE']
		for i in ledRange:
			LED_STATE_CACHE[refresh][i] = currentColor
		

def runStrip():
	while True:
		print('Start loop')
		for refreshCounter in range(150):
			ledrep = ''
			print('Refresh: ', refreshCounter)
			for pixel in range(30):
				ledrep += LED_STATE_CACHE[refreshCounter][pixel]
				rgbVals = LED_STATE_CACHE[refreshCounter][pixel].split('#')
				#using ws281x
				#strip.setPixelColorRGB(pixel, rgbVals[0], rgbVals[1], rgbVals[2])
				#strip.show()
			print(ledrep)
		time.sleep(0.062)


if __name__ == '__main__':
	sampleFileLink = open('sample.JSON', 'r')
	sampleFile = sampleFileLink.read()
	parsedJson = json.loads(sampleFile)
	initStateCache()
	populateBufferFromCustomCommand(parsedJson[2])
	loadCacheFromBuffer()
	runStrip()

