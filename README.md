OfficeInk Project
Inline-style: 
![alt text](https://github.com/noonasGit/OfficeInk/blob/main/IMG_8304.jpeg "The Frame Project")




Welcome to my little tinker toy project.

I created this project to make a screen for the Office that would share insiprational or funny messages in a simple and approachable way.

It has been made after hours of hacking around with Kobo e-readers as well as making other projects with e-ink screens.

Hardware for this project

Raspberry Pi Zero W.
Waveshare e-ink screen 7.5inch E-Paper E-Ink Display HAT (B) For Raspberry Pi, 800×480, Red / Black / White, SPI (https://www.waveshare.com/product/displays/e-paper/epaper-1/7.5inch-e-paper-hat-b.htm)
PiSugar 3 (https://www.pisugar.com)
IKEA Frame for the e-ink screen (https://www.ikea.com/ca/en/p/roedalm-frame-birch-effect-70548888/)

I 3D pritned a mask (if you can cut out the paper one - more power to you) :)

Setup / Installation

Install Raspberry Pi OS on an SD card. (enable SSH and sFTP)

Install Python on the RasPi (https://projects.raspberrypi.org/en/projects/generic-python-install-python3#linux)

Install the waveshare drivers (follow: https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT_(B)_Manual#Working_With_Raspberry_Pi)

Install the PiSugar Drivers (https://github.com/PiSugar/PiSugar/wiki/PiSugar-3-Series)

Create a directory for the OfficeInk Project source code on the RapsPi, I put it in /opt/OfficeInk

Copy (sFTP) all files from this repo in there (including subdirectories)

SSH to the Raspi and test it by running #python OfficeInk.py debug

This should run the code and you should see a printout on the screen.

You can now modify the OfficeInk_dashboard.ini file to your preferences.

