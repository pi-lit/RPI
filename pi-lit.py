import time
from rpi_ws281x import *
import argparse
import asyncio
import websockets

# LED strip configuration:
LED_COUNT      = 30      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

#async def hello():
    #async with websockets.connect('http://192.168.1.223:3000') as websocket:
        
    

def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def colorWholeStrip(strip, r, g, b):
    for x in range(strip.numPixels()):
        strip.setPixelColorRGB(x, r, g, b) 
    strip.show()
    
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

        while True:
            color = input("Enter a color to change the strip to or 'color'wipe to wipe that color or segment to color a segment: ")
            if (color == "red"):
                colorWholeStrip(strip, 255, 0, 0)
            elif (color == "green"):
                colorWholeStrip(strip, 0, 255, 0)
            elif (color == "blue"):
                colorWholeStrip(strip, 0, 0, 255)
            elif (color == "wipered"):
                colorWipe(strip, Color(255, 0, 0))
            elif (color == "wipegreen"):
                colorWipe(strip, Color(0, 255, 0))
            elif (color == "wipeblue"):
                colorWipe(strip, Color(0, 0, 255))
            elif (color == "segment"):
                segmentLower = int(input("first index: "))
                segmentUpper = int(input("second index: "))
                r = int(input("Red value: "))
                g = int(input("Green value: "))
                b = int(input("Blue value: "))
                colorRange(strip, segmentLower, segmentUpper, r, g, b)
            else:
                colorWholeStrip(strip, 255, 255, 255)
            
                
          
           
    except KeyboardInterrupt:
            if args.clear:
                colorWipe(strip, Color(0,0,0), 10)