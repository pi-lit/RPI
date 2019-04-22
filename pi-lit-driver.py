# python inports
import time
import argparse
import json
import threading
import os
import math

# rpi library import
from rpi_ws281x import *

# strip variables
LED_COUNT = 30
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL = 0


#states
OFF = '0#0#0'
WHITE = '255#255#255'

# globals
LED_STATE_CACHE = []
COMMAND_BUFFER = {}

#Listen for JSON input
def listenForJson():
	commandObjString = input()
	commandObjParsed = json.loads(commandObjString)
	configObj = commandObjParsed['config']
	commandArray = commandObjParsed['config']['commandArray']
	print(commandArray)
	for i in range(len(commandArray)):
		if commandArray[i]['effect'] == 'custom':
			populateBufferFromCustomCommand(commandArray[i])
		elif commandArray[i]['effect'] == 'solid':
			colorSolid(commandArray[i]['range'], commandArray[i]['range']['color']['r'], commandArray[i]['range']['color']['g'], commandArray[i]['range']['color']['b'])
		else:
			return 1

def listenForJsonNew():
	while True:
		commandObjStr = input()
		command = json.loads(commandObjStr)
		print(command)
		if command['effect'] == "solid":
			colorSolid(command['range'],command['color']['r'], command['color']['g'], command['color']['b'])
		elif command['effect'] == "custom":
			populateBufferFromCustomCommand(command)
			loadCacheFromBuffer()
		else:
			print(1)

#color solid
def colorSolid(rangeFromCommand, r, g, b):
	for i in range(150):
		for pixel in rangeFromCommand:
			LED_STATE_CACHE[i][pixel] = str(r) + '#' + str(g) + '#' + str(b)
		


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
		

def runStrip(strip):
	while True:
		print('Start loop')
		for refreshCounter in range(150):
			ledrep = ''
			#print('Refresh: ', refreshCounter)
			for pixel in range(30):
				ledrep += LED_STATE_CACHE[refreshCounter][pixel]
				rgbVals = LED_STATE_CACHE[refreshCounter][pixel].split('#')
				#using ws281x
				strip.setPixelColorRGB(pixel,int(rgbVals[0]), int(rgbVals[1]), int(rgbVals[2]))
				strip.show()
			#print(ledrep)
		time.sleep(0.062)


if __name__ == '__main__':
	sampleFileLink = open('sample.JSON', 'r')
	sampleFile = sampleFileLink.read()
	parsedJson = json.loads(sampleFile)
	
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
	strip.begin()
	
	initStateCache()
	populateBufferFromCustomCommand(parsedJson[2])
	loadCacheFromBuffer()

	t1 = threading.Thread(target=listenForJsonNew)
	t2 = threading.Thread(target=runStrip, args=(strip, ))
	#testThread = threading.Thread(target=colorSolid, args=([0,1,2,3,4,5,6,7,8,9,10], 255, 0, 0))

	t1.start()
	t2.start()
	#testThread.start()

