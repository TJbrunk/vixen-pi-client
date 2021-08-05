
# Overview
This app is designed to be a ~christmas~ light controller.  
It receives control commands using sACN 1.31 protocol (Primarily from [Vixen](http://www.vixenlights.com/) and controls the lights connected to the RPi gpio.  
Designed to work with standard lights via electrical relay control, or 'smart' neopixel style lights

# Dependencies
  - python 3.6 (or newer)
  - RPI.GPIO
  - rpi_ws281x
  - Adafruit Neopixel
  - [sacn](https://github.com/Hundemeier/sacn)
*pip packages need to be installed as sudo because the app needs to access hardware*
~~~~ sudo pip3 install RPI.GPIO rpi_ws281x adafruit-circuitpython-neopixel sacn ~~~~
