# OfficeInk Project

The finished product: 
![alt text](https://github.com/noonasGit/OfficeInk/blob/main/IMG_8304.jpeg "The Frame Project")

## Welcome to my little tinker toy project.

I created this project to make a screen for the Office that would share insiprational or funny messages in a simple and approachable way.

It has been made after hours of hacking around with Kobo e-readers as well as making other projects with e-ink screens.

The Graphics are all hand-made by me, the fonts are opensource / free to use

## Hardware for this project

Raspberry Pi Zero W.

Waveshare e-ink screen 7.5inch E-Paper E-Ink Display HAT (B) For Raspberry Pi, 800×480, Red / Black / White, SPI (https://www.waveshare.com/product/displays/e-paper/epaper-1/7.5inch-e-paper-hat-b.htm)

PiSugar 3 (https://www.pisugar.com)

IKEA Frame for the e-ink screen (https://www.ikea.com/ca/en/p/roedalm-frame-birch-effect-70548888/)

I 3D pritned a mask (if you can cut out the paper one - more power to you) :)

## Setup / Installation

Install Raspberry Pi OS on an SD card. (enable SSH and sFTP)

Install Python on the RasPi (https://projects.raspberrypi.org/en/projects/generic-python-install-python3#linux)

Install the waveshare drivers (follow: https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT_(B)_Manual#Working_With_Raspberry_Pi)

Install the PiSugar Drivers (https://github.com/PiSugar/PiSugar/wiki/PiSugar-3-Series)

Create a directory for the OfficeInk Project source code on the RapsPi, I put it in /opt/OfficeInk

Copy (sFTP) all files from this repo in there (including subdirectories)

## Testing

SSH to the Raspi and test it by running #python OfficeInk.py debug

This should run the code and you should see a printout on the screen.

You can now modify the OfficeInk_dashboard.ini file to your preferences.

## Options running the frame

When you are using a PiSugar, I recommend configuring the automatic wakeup once daily (I set mine to 5am, Can be done via the web UI for the PiSugar) 

In the config you can set the dashboard to shutdown the RasPi to shut down after run so that you the battery will last ~ 3 weeks.

## Configure to run at boot
ssh into the RasPi , ensure you are using the startup username

type crontab -e

`insert a row to the top`

@reboot cd /opt/OfficeInk && python3 OfficeInk.py debug > applog.log

save and exit

Ensure that the `shutdown-after-run=TRUE` is set in the `OfficeInk_dashboard.ini` file is set so that it will shut down afer run to save battery.

When `show_quote_live=FALSE` is set, it will not connect to the Internet to get a quote but will use the supplied quotes.txt file to select a random quote.

### To-dos.

As this is just for fun, I will go back to make some still hard coded parts configurable.

For example, the selection on what day what kind of quote is shown is still hard-coded in but I will get to it at one point and update the project.

