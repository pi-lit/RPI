import time
from rpi_ws281x import *
import argparse
import json
import threading
import os

# LED strip configuration:
LED_COUNT      = 30      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
CURRENT_EFFECT = "OFF"
BUFFERED_IN

#0 - solid color
#1 - rainbow
#2 - flashing
#4 - custom

#sample encoding num1,num2,num3...,numk#effect#coloroption
        
BUFFER_STRIP = []

#initialize buffer list and sync with firmware
#strip runs indicies 0-(length-1) initialized as all white
def initBuffer(buffer, strip)
    for i in range(strip.numPixels()):
        buffer.append([255,255,255])
        strip.setPixelColorRGB(i, 255, 255, 255)

#update all of the strip pixels by iterating through the buffer
#shows strip after buffer copy
def renderStrip(strip, buffer)
    for i in range(strip.numPixels):
        strip.setPixelColorRGB(i, buffer[i][0], buffer[i][1], buffer[i][2])
    strip.show()

#returns json parsed
def parseInput(jsonText) 
    return json.loads(jsonText)



def getInput()
    command = input()
    newJson = parseInput(command)
    resolveEffect(newJson)

def threadFileInput()
    #get input
    #parse input
    #


#
def resolveEffect(jsonText) 
    if jsonText['effect'].lower() == "rainbow":
        CURRENT_EFFECT = "rainbow"
    if jsonText['effect'].lower() == "solid":
        CURRENT_EFFECT = "solid"
    if jsonText['effect'].lower() == "custom":
        CURRENT_EFFECT = "custom"
#wipe effect over low to high
def colorWipe(strip, color, wait_ms=50, low, high):
    """Wipe color across display a pixel at a time."""
    for i in range(low, high):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)


#color whole strip indicated color
def colorWholeStrip(strip, r, g, b):
    for x in range(strip.numPixels()):
        strip.setPixelColorRGB(x, r, g, b) 
    strip.show()
    

#solid color over range low to high
def colorRange(strip, low, high, r, g, b):
    for x in range(low, high):
        strip.setPixelColorRGB(x, r, g, b)
    strip.show()


    
    
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    

    
    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')
        

    try:
        # renderStrip(strip, buffer)
        testJsonFile = open("sample.JSON", "r")
        testJson = testJsonFile.read()
        testJsonParsed = json.loads(testJson)
        rangeArr = testJsonParsed[0]['range']
        for i in range(len(rangeArr)):
            print(rangeArr[i])
        print(testJsonParsed[0]['range'][0])

        testJsonFile.close()

        while true:
            #10000ms
            for msec in range(10000)
                checkEffect()
                if (msec%30 == 0):
                    


    except KeyboardInterrupt:
            if args.clear:
                colorWipe(strip, Color(0,0,0), 10)