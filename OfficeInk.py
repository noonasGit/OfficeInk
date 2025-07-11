#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import socket
import random
from subprocess import call
from datetime import datetime, date, timedelta
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'icons')
imgdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'image')
weatherdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'icons/weather')
fontdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd7in5b_V2
import time
from PIL import Image,ImageDraw,ImageFont
from PIL.ImageFont import FreeTypeFont
import traceback
from openweather import current_weather, tomorrow_weather
from aqidata import current_aqi, get_aqi_status_data, aqi_trend, write_aqi_stats
from getquote import quoteoftheday, addquotetofile, quotefromfile
from dadjoke import getdadjoke, dadjokefromfile
from garbage_schedule import get_garbage_status, get_garbage_config_data
from pi_info import getRAMinfo, getDiskSpace, getCPUtemperature, getCPUuse

from pisugar import *

import configparser

from dataclasses import dataclass

# Made By Jonas Johansson
# Opensource project, based on bits and pieces from various sources.

@dataclass
class screen:
    width : int
    height : int
    middle_w : int
    middle_h : int
    quote_max : int
    reminder_max : int
    use_red : int
    refresh_rate_min : int
    clean_screen : int
    sleep_hour :int
    wake_hour : int

@dataclass
class dashboard:
    show_messages : int
    message_state : int
    show_date : int
    show_quote : int
    show_quote_live : int
    quote_length : int
    show_comic : int
    show_dadjoke : int
    show_dadjoke_live : int
    quote : str
    dadjoke : str
    show_power : int
    delay_start_sec : int
    shutdown_after_run : int
    shutdown_at_hour : int
    shutdown_hour : int

@dataclass
class hourglass:
    day : int
    hour : int
    hourly : int
    curenttime : int
    currentday : int
    live_cutin_hour : int
    live_cutout_hour : int
    last_refresh : str
    evening_hour : str

@dataclass
class performance:
    usedram : int
    freeram : int
    ramincrease : int
    previousram : int
    cli : str
    debug : str
    ip_address : str
    host_name : str
    countr : int
    keepalive : int

@dataclass
class battery:
    level : int
    state : str

@dataclass
class font:
    DayTitle :FreeTypeFont
    SFMonth :FreeTypeFont
    SFDate :FreeTypeFont

    SFQuote :FreeTypeFont
    SFQuoteAuthor :FreeTypeFont
    SFJoke :FreeTypeFont
    SFReminder :FreeTypeFont
    SFReminder_sub :FreeTypeFont

    SleepFont  :FreeTypeFont
    SleepFont_foot :FreeTypeFont

def get_dashboard_config_data(file_path:str):

    applog("Dashboard","Loading fonts...")
    ####################
    ###################
    #######
    #######
    ############
    ############
    #######
    #######
    #######


    font.DayTitle = ImageFont.truetype("fonts/SF-Compact-Rounded-Bold.ttf", 62)
    font.SFMonth = ImageFont.truetype("fonts/SF-Compact-Rounded-Bold.ttf", 14)
    font.SFDate = ImageFont.truetype("fonts/SF-Compact-Rounded-Bold.ttf", 42)

    font.SFToday_temp = ImageFont.truetype("fonts/SF-Compact-Rounded-Bold.ttf",64)
    font.SFToday_cond = ImageFont.truetype("fonts/SF-Compact-Rounded-Semibold.otf",32)
    font.SFToday_hl = ImageFont.truetype("fonts/SF-Compact-Rounded-Medium.otf",26)
    font.SFWdetails = ImageFont.truetype("fonts/SF-Compact-Rounded-Medium.otf",22)
    font.SFWdetails_bold = ImageFont.truetype("fonts/SF-Compact-Rounded-Bold.ttf",22)
    font.SFWdetails_semibold = ImageFont.truetype("fonts/SF-Compact-Rounded-Semibold.otf",22)
    font.SFWdetails_sub = ImageFont.truetype("fonts/SF-Compact-Rounded-Semibold.otf",16)
    font.SFWdetails_sub_bold = ImageFont.truetype("fonts/SF-Compact-Rounded-Bold.ttf",16)
    font.SFWAQI_bold = ImageFont.truetype("fonts/SF-Compact-Rounded-Bold.ttf",22)
    font.SFWAQI_bold_small = ImageFont.truetype("fonts/SF-Compact-Rounded-Bold.ttf",14)

    font.SFToDo = ImageFont.truetype("fonts/SF-Compact-Rounded-Medium.otf",24)
    font.SFToDo_sub = ImageFont.truetype("fonts/SF-Compact-Rounded-Medium.otf",16)

    font.SFQuote = ImageFont.truetype("fonts/SF-Compact-Rounded-Semibold.otf",46)
    font.SFQuoteAuthor = ImageFont.truetype("fonts/SF-Compact-Rounded-Medium.otf",30)
    font.SFJoke = ImageFont.truetype("fonts/SF-Compact-Rounded-Semibold.otf",26)
    font.SFReminder = ImageFont.truetype("fonts/SF-Compact-Rounded-Semibold.otf",24)
    font.SFReminder_sub = ImageFont.truetype("fonts/SF-Compact-Rounded-Semibold.otf",20)

    font.SleepFont = ImageFont.truetype("fonts/SF-Compact-Rounded-Semibold.otf",32)
    font.SleepFont_foot = ImageFont.truetype("fonts/SF-Compact-Rounded-Semibold.otf",24)

    applog("Dashboard","Fonts loaded...")
    applog("Dashboard","Loading dashboard.ini")
    parser = configparser.ConfigParser()
    parser.read(file_path)
    data = dict()
    
    


    data['screen_type-id'] = parser.get("screen-config", "screen_type")
    data['use_red-id'] = parser.get("screen-config", "use_red")
    data['refresh-rate-min-id'] = parser.get("screen-config", "refresh-rate-min")
    data['screen_sleep_hour-id'] = parser.get("screen-config", "screen_sleep_hour")
    data['screen_wake_hour-id'] = parser.get("screen-config", "screen_wake_hour")
    data['evening_hour-id'] = parser.get("screen-config", "evening_hour")
    data['delay_start_sec-id'] = parser.get("screen-config", "delay_start_sec")
    
    data['show_quote-id'] = parser.get("feature-config", "show_quote")
    data['show_quote_live-id'] = parser.get("feature-config", "show_quote_live")
    data['show_comic-id'] = parser.get("feature-config", "show_comic")
    data['show_messages-id'] = parser.get("feature-config", "show_messages")
    data['show_dadjoke-id'] = parser.get("feature-config", "show_dadjoke")
    data['live_dadjoke-id'] = parser.get("feature-config", "live_dadjoke")
    data['show-power-id'] = parser.get("feature-config", "show-power")
    data['shutdown-after-run-id'] = parser.get("feature-config", "shutdown-after-run")
    
    data['shutdown-at-hour-id'] = parser.get("feature-config", "shutdown-at-hour")
    data['shutdown-hour-id'] = parser.get("feature-config", "shutdown-hour")
    

    hourglass.evening_hour = int(data['evening_hour-id'])


    screen.refresh_rate_min = int(data['refresh-rate-min-id'])
    screen.sleep_hour = int(data['screen_sleep_hour-id'])
    screen.wake_hour = int(data['screen_wake_hour-id'])


    if data['use_red-id'] == "TRUE":
        screen.use_red = 1
        applog("System settings" ,"Red pigment is enabled")

    else:
        screen.use_red = 0

    if data['show_messages-id'] == "TRUE":
        dashboard.show_messages = 1
    else : 
        dashboard.show_messages = 0


    if data['show_quote-id'] == "TRUE":
        dashboard.show_quote = 1
    else : 
        dashboard.show_quote = 0
    
    if data['show_quote_live-id'] == "TRUE":
        dashboard.show_quote_live = 1
    else : 
        dashboard.show_quote_live = 0


    if data['show_comic-id'] == "TRUE":
        dashboard.show_comic = 1
    else : 
        dashboard.show_comic = 0

    if data['show_dadjoke-id'] == "TRUE":
        dashboard.show_dadjoke = 1
    else : 
        dashboard.show_dadjoke = 0

    if data['live_dadjoke-id'] == "TRUE":
        dashboard.show_dadjoke_live = 1
    else : 
        dashboard.show_dadjoke_live = 0

    if data['show-power-id'] == "TRUE":
        dashboard.show_power = 1
    else : 
        dashboard.show_power  = 0

    if data['shutdown-after-run-id'] == "TRUE":
        dashboard.shutdown_after_run = 1
    else : 
        dashboard.shutdown_after_run  = 0

    if data['shutdown-at-hour-id'] == "TRUE":
        dashboard.shutdown_at_hour = 1
    else : 
        dashboard.shutdown_at_hour  = 0

    dashboard.shutdown_hour = data['shutdown-hour-id']
    
    dashboard.message_state = 0
    dashboard.quote_length = 175

    dashboard.delay_start_sec = int(data['delay_start_sec-id'])

    applog("Dashboard","Completed dashboard.ini")

    return data

def get_ip():
    network_status = False
    performance.ip_address = "no_ip"
    for I in range(0, 5):
        applog("Waiting for network","attempt "+str(I))
        try:
            performance.host_name = socket.gethostname()
        except:
            performance.host_name = "Unknown"
        try:
            applog("Waiting for network","standby...")
            testIP = "8.8.8.8"
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect((testIP, 0))       
            performance.ip_address = s.getsockname()[0]
            performance.host_name = socket.gethostname()
            applog("System Hostname is",performance.host_name)
            applog("System IP Address is",performance.ip_address)
            network_status = True
        except Exception as e:
            print("exc. ignored {}".format(e))
            performance.ip_address = "no_ip"
            applog("System IP Address is","NO IP FOUND")
        if network_status:
            applog("Network found","Exiting after "+str(I)+" times")
            break
        time.sleep(5)
    applog("System","Network : "+performance.ip_address+"@"+performance.host_name)


def welcome_screen(delay_time_in_sec):
    font.SleepFont = ImageFont.truetype("fonts/SF-Compact-Rounded-Semibold.otf",32)
    font.SleepFont_foot = ImageFont.truetype("fonts/SF-Compact-Rounded-Semibold.otf",24)

    applog("Welcome Screen" ,"Welcome screen initiated")

    black = 'rgb(0,0,0)'
    white = 'rgb(255,255,255)'

    try:
        applog("Welcome Screen" ,"Setting screen")
        epd = epd7in5b_V2.EPD()
        epd.init()
        applog("Welcome Screen" ,"INIT screen")
        if performance.cli == "noclean":
            applog("Welcome Screen" ,"Screen cleaning skipped")
        else:
            applog("Welcome Screen" ,"Time to clean the screen")
            epd.Clear()
        screen.height = epd.height
        screen.width = epd.width
        screen.middle_w = screen.width/2
        screen.middle_h = screen.height/2
    except IOError as e:
        applog("Welcome Screen" ,"error"+str(e)) 

    except KeyboardInterrupt:
        applog("Welcome Screen" ,"ctrl + c received") 
        epd7in5b_V2.epdconfig.module_exit()
        exit()
    imageB = Image.new('L', (epd.width, epd.height), 255)  # 255: clear the frame
    imageR = Image.new('L', (epd.width, epd.height), 255)  # 255: clear the frame
    draw_black = ImageDraw.Draw(imageB)

    if performance.ip_address == "no_ip":
        applog("Welcome Screen" ,"loading no-wifi icon") 
        net_icon = Image.open(os.path.join(picdir, 'wifi_off.png'))
        gx = 20
        gy = 20
        imageB.paste(net_icon, (gx,gy), net_icon)

    else:
        applog("Welcome Screen" ,"loading wifi icon") 
        if "wifi-off" in performance.cli:
            net_icon = Image.open(os.path.join(picdir, 'wifi_off_option.png'))
        else:
            net_icon = Image.open(os.path.join(picdir, 'wifi_on.png'))
        
        gx = 20
        gy = 20
        imageB.paste(net_icon, (gx,gy), net_icon)
        tx = int(gx + (net_icon.size[0] + 4))
        ty = gy
        if "wifi-off" in performance.cli:
            draw_black.text((tx, ty), performance.ip_address+" WiFi Will shut off after this screen", font = font.SleepFont_foot, fill = 'rgb(0,0,0)')
        else:
            draw_black.text((tx, ty), performance.ip_address, font = font.SleepFont_foot, fill = 'rgb(0,0,0)')

    welome_icon = Image.open(os.path.join(picdir, 'welcome.png'))

    welcome_string = "Welcome to InkScreen @"+performance.host_name+"..."
    t_g, t_g, test_t_w, test_t_h = draw_black.textbbox((0,0),welcome_string, font=font.SleepFont)

    sX = int(screen.middle_w) - int(welome_icon.size[0]/2)
    sY = int(screen.middle_h) - int(welome_icon.size[1]/2)
    sY = sY - int(test_t_h)
    imageB.paste(welome_icon, (sX,sY), welome_icon)



    sX = int(screen.middle_w) - int(test_t_w/2)
    sY = int(sY + welome_icon.size[1]) + 4
    draw_black.text((sX, sY), welcome_string, font = font.SleepFont, fill = 'rgb(0,0,0)')

    header_Month_Date = datetime.now().strftime("%b %-d")


    wakeup_string = "System time is "+header_Month_Date+", "+datetime.now().strftime("%H:%M")
    t_g, t_g, test_t_w, test_t_h = draw_black.textbbox((0,0),wakeup_string, font=font.SleepFont_foot)
    sX = int(screen.middle_w) - int(test_t_w/2)
    sY = sY + 40
    draw_black.text((sX, sY), wakeup_string, font = font.SleepFont_foot, fill = 'rgb(0,0,0)')

    wakeup_string = "Shutwown after run: "+str(dashboard.shutdown_after_run)

    if dashboard.shutdown_at_hour == 1:
        wakeup_string = wakeup_string+" Shutdown @"+str(dashboard.shutdown_hour)
    if performance.keepalive == 1:
        wakeup_string = wakeup_string + " Keepalive ON"
    t_g, t_g, test_t_w, test_t_h = draw_black.textbbox((0,0),wakeup_string, font=font.SleepFont_foot)
    sX = int(screen.middle_w) - int(test_t_w/2)
    sY = sY + 40
    draw_black.text((sX, sY), wakeup_string, font = font.SleepFont_foot, fill = 'rgb(0,0,0)')


    if dashboard.show_power == 1:
        # DEBUG BATTERY
        #battlevel.state = "Not Charging"
        #battlevel.level = 10
    
        applog("Dashoard","Getting battery status and level...")
        battlevel = get_pibatt()

        if battlevel.level !=-1: #Checking if battery level can be goten -1 means error
            applog("Dashoard","Loading battery icon and drawing status bottom left")
            applog("Dashboard","Battery state: "+battlevel.state+" @ "+str(battlevel.level)+"%")
            if battlevel.state == "Charging":
                if battlevel.level <100:
                    batt_icon = Image.open(os.path.join(picdir, 'Battery_chrg.png'))
                else:
                    batt_icon = Image.open(os.path.join(picdir, 'Battery_chrg_full.png'))
                btx = 5
                bty = (screen.height - 5) - int(batt_icon.height)
                imageB.paste(batt_icon, (btx,bty), batt_icon)
            else:
                if battlevel.level > 20:
                    if battlevel.level == 100:
                        batt_icon = Image.open(os.path.join(picdir, 'Battery_full.png'))
                    else:
                        batt_icon = Image.open(os.path.join(picdir, 'Battery.png'))
                        batt_load_txt = str(battlevel.level)
                    btx = 5
                    bty = (screen.height - 5) - int(batt_icon.height)
                    imageB.paste(batt_icon, (btx,bty), batt_icon)
                    if battlevel.level < 100:
                        t_G, t_G, batt_t_w, batt_t_h = draw_black.textbbox((0,0),batt_load_txt, font=font.SFMonth)
                        btx = btx + int(batt_icon.width/2)
                        btx = btx - int(batt_t_w/2)
                        bty = bty + int(batt_t_h/2)
                        draw_black.text((btx, bty), batt_load_txt, font=font.SFMonth, fill = black)
                else:
                    if screen.use_red == 1:
                        batt_iconB = Image.open(os.path.join(picdir, 'Battery_low_B.png'))
                        batt_iconR = Image.open(os.path.join(picdir, 'Battery_low_R.png'))
                        btx = 5
                        bty = (screen.height - 5) - int(batt_iconB.height)
                        imageB.paste(batt_iconB, (btx,bty), batt_iconB)
                        imageR.paste(batt_iconR, (btx,bty), batt_iconR)
                    else:
                        batt_icon = Image.open(os.path.join(picdir, 'Battery_low.png'))
                        btx = 5
                        bty = (screen.height - 5) - int(batt_icon.height)
                        bty = bty - 4
                        imageB.paste(batt_icon, (btx,bty), batt_icon)
        else:
            applog("Dashboard","Battery not found!")
            batt_icon = Image.open(os.path.join(picdir, 'Battery_no_batt.png'))
            btx = 5
            bty = (screen.height - 5) - int(batt_icon.height)
            imageB.paste(batt_icon, (btx,bty), batt_icon)
    else:
        applog("Dasboard","Show Power is OFF")




    wakeup_string = "OfficeInk will start in "+str(delay_time_in_sec)+" seconds, press ctrl + c to exit."
    t_g, t_g, test_t_w, test_t_h = draw_black.textbbox((0,0),wakeup_string, font=font.SleepFont_foot)
    sX = int(screen.middle_w) - int(test_t_w/2)
    sY = int(screen.height - (int(test_t_h) + 5))
    draw_black.text((sX, sY), wakeup_string, font = font.SleepFont_foot, fill = 'rgb(0,0,0)')
    
    epd.display(epd.getbuffer(imageB),epd.getbuffer(imageR))
    epd.sleep()
    applog("OfficeInk" ,"Starting up in "+str(delay_time_in_sec)+" seconds...")
    time.sleep(delay_time_in_sec)

def daily_quotes():

    applog("OfficeInk" ,"Daily Message screen initiated")

    black = 'rgb(0,0,0)'
    white = 'rgb(255,255,255)'

    try:
        applog("OfficeInk" ,"Setting Daily Message screen variables")
        epd = epd7in5b_V2.EPD()
        epd.init()
        applog("OfficeInk" ,"INIT screen")
        epd.Clear()
        screen.height = epd.height
        screen.width = epd.width
        screen.middle_w = screen.width/2
        screen.middle_h = screen.height/2
    except IOError as e:
        applog("OfficeInk" ,"error"+str(e)) 

    except KeyboardInterrupt:
        applog("OfficeInk" ,"ctrl + c received") 
        epd7in5b_V2.epdconfig.module_exit()
        exit()
    imageB = Image.new('L', (epd.width, epd.height), 255)  # 255: clear the frame
    imageR = Image.new('L', (epd.width, epd.height), 255)  # 255: clear the frame
    draw_black = ImageDraw.Draw(imageB)
    draw_red = ImageDraw.Draw(imageR)

    
    x_master = 10
    y_master = 10

    x = x_master
    y = y_master
    screen_y = 0
    # Find out how many characters per line of screen for Quotes
    screen.quote_max = screen.width - (85 + (x_master*2))
    # Quotes Section

        #######    #######
        ####   ####   ####
        ####   ####   ####
        ####   ####   ####
        ####   ####   ####
        ####   ####   ####


    if dashboard.show_messages == 1:
        
        applog("Dashboard","Daily Messages : ON")
            

        quote_icon = Image.open(os.path.join(picdir, "quote_icon.png"))
        quote_iconB = Image.open(os.path.join(picdir, "quote_b.png"))
        quote_iconR = Image.open(os.path.join(picdir, "quote_r.png"))
    

        x = x_master
        if screen_y == 0:
            y = y_master
        else:
            y = screen_y
        qx = x
        qy = y
      
    
        qml = dashboard.quote_length
        qll = qml+1
        qmaxtries = 0
        applog("Message of the day" ,"Time to get a new message...")

        applog("Message of the day" ,"Getting a message under "+str(qml)+" lenght")

        while qll >= qml :
            applog("Message state","Getting a quote")
            applog("Message of the day" ,"Getting random quote from local database...")
            dashboard.quote = quotefromfile("quotes.txt")
            qll = len(dashboard.quote.quote_text)
            qmaxtries +=1
            if qmaxtries > 10:
                break

            if qll >  qml:
                applog("Message of the day" ,"Message Feature : Attempt: "+str(qmaxtries))
            else:
                applog("Message of the day" ,"Message lenght is "+str(qll))



        if qll == 0 or qll > qml:
            applog("Quote of the day" ,"Max attempts to get a short enough quote exhausted.")
            #Just in case we could not find a short enough quote in 10 attempts.
            dashboard.quote.quote_text = "Somethings looking for a quote becomes the quote itself..."
            dashboard.quote.quote_author = "Dashboard Ai Error ;("
            hourglass.day = -1

        daily_message = dashboard.quote.quote_text
        
        #print("Now trying to slice the text in chunks")
        text_g, text_g, test_t_w, test_t_h = draw_black.textbbox((0,0),daily_message, font=font.SFQuote)
        text_max = test_t_w
        toff = x + int(quote_icon.size[0]+2)
        screen.offset = int( quote_icon.size[0] + (x_master * 2) )
        text_line_max = screen.quote_max - (toff + screen.offset)

        text_line = []
        textbuffer = ""

        #Show the quote icon status
        if screen.use_red == 1:
            imageB.paste(quote_iconB,(qx,qy),quote_iconB)
            imageR.paste(quote_iconR,(qx,qy),quote_iconR)
        else:
            imageB.paste(quote_icon,(qx,qy),quote_icon)

        #Split the quote into words in an array

        quote_words = daily_message.split()
        wl = len(quote_words)

        #See if the total is larger than the text_line_max value set.
        applog("Message of the day" ,"Max pixels per line is "+str(text_line_max))
        t_g, t_g, test_t_w, test_t_h = draw_black.textbbox((0,0),daily_message, font=font.SFQuote)

        if test_t_w > text_line_max:
            l = 0
            ql = len(quote_words)
            while l < ql:
                textbuffer = textbuffer + quote_words[l] + " "
                l += 1
                t_g, t_g, test_t_w, test_t_h = draw_black.textbbox((0,0),textbuffer, font=font.SFQuote)
                #print(textbuffer)
                if test_t_w >= text_line_max:
                    text_line.append(textbuffer)
                    textbuffer = ""
                    #print(l)
            if (len(textbuffer)):
                text_line.append(textbuffer)
        else :
            applog("Message of the day" ,"Message fits in one row...")
            if len(daily_message):
                applog("Message of the day" ,"Using only one row here.")
                text_line.append(daily_message)
                t_g, t_g, test_t_w, test_t_h = draw_black.textbbox((0,0),daily_message, font=font.SFQuote)
            else :
                text_line = "Oops there is a bug here..."
                dashboard.quote.quote_author = "Dashboard Ai Error ;("
                t_g, t_g, test_t_w, test_t_h = draw_black.textbbox((0,0),daily_message, font=font.SFQuote)
                applog("Message of the day" ,"QUOTE IS EMPTY!.")


        # Get number of arrays generated
        qs = len(text_line)
        qc = 0
        #qx = 20
    
        g_w = 0
        q_h = 0
        q_w = 0
    
        #Getting the widest line of text
        tq_g, tq_g, tq_w, tq_h = draw_black.textbbox((0,0),text_line[qc], font=font.SFQuote)
        for i in text_line:
            tq_g, tq_g, tq_w, tq_h = draw_black.textbbox((0,0),i, font=font.SFQuote)
            q_h = tq_h
            if tq_w > q_w :
                q_w = tq_w
            qc +=1

        quote_total_height = int(tq_h * qs)
        
        aqG, aqG, aq_w, aq_h = draw_black.textbbox((0,0),"- "+dashboard.quote.quote_author, font=font.SFQuoteAuthor)

        quote_total_height = int(quote_total_height + aq_h)

        applog("Message of the day","Total message height is "+str(quote_total_height))

        #Writing the quote line by line.
        qc = 0
        gTy = qy

        # Setting gTy to be in the middle

        gTy = screen.middle_h - int(quote_total_height/2)

        # Setting gTy to be in the middle

        gTx = x + int(quote_icon.size[0]+2)


        while qc < qs:
            tq_g, tq_g, tq_ww, tq_g = draw_black.textbbox((0,0),text_line[qc], font=font.SFQuote)
            gTx = screen.middle_w - int(tq_ww/2)
            draw_black.text((gTx, gTy), text_line[qc], font=font.SFQuote, fill=black)
            #print(text_line[qc])
            qc += 1
            gTy = gTy + int(q_h)
            #if qc == 1:
            #    gTx = gTx + 20
        
        qG, qG, q_w, q_h = draw_black.textbbox((0,0),"- "+dashboard.quote.quote_author, font=font.SFQuoteAuthor)
        gTx = int(screen.middle_w - q_w/2)
        gTy = gTy -2
        if screen.use_red == 1:
            draw_red.text((gTx, gTy), "- "+dashboard.quote.quote_author, font=font.SFQuoteAuthor, fill=black)
        else :
            draw_black.text((gTx, gTy), "- "+dashboard.quote.quote_author, font=font.SFQuoteAuthor, fill=black)
    
        gTy = gTy + int(q_h) + 2
        screen_y = gTy

        ###########################
        # End of Message of the day
        ###########################
    else:
        applog("Dashboard","Message of the day feature : OFF")
    
    nextrefreshtime = datetime.now() + timedelta(minutes=int(screen.refresh_rate_min))
    hourglass.last_refresh = "Daily Quote, "+hourglass.last_refresh
    #hourglass.last_refresh = hourglass.last_refresh + " next @ " + nextrefreshtime.strftime("%H:%M")
    #hourglass.last_refresh = "Counter @ "+str(performance.countr)
    applog("Dashoard","Show the last refresh text at the bottom, centered "+hourglass.last_refresh)
    t_G, t_G, test_t_w, test_t_h = draw_black.textbbox((0,0),hourglass.last_refresh, font=font.SFMonth)
    gTx = int(screen.middle_w) - int(test_t_w/2)
    gTy = screen.height - int(test_t_h + 4)
    draw_black.text((gTx, gTy), hourglass.last_refresh, font=font.SFMonth, fill=black)

    if dashboard.show_power == 1:
        # DEBUG BATTERY
        #battlevel.state = "Not Charging"
        #battlevel.level = 10
    
        applog("Dashoard","Getting battery status and level...")
        battlevel = get_pibatt()

        if battlevel.level !=-1: #Checking if battery level can be goten -1 means error
            applog("Dashoard","Loading battery icon and drawing status bottom left")
            applog("Dashboard","Battery state: "+battlevel.state+" @ "+str(battlevel.level)+"%")
            if battlevel.state == "Charging":
                if battlevel.level <100:
                    batt_icon = Image.open(os.path.join(picdir, 'Battery_chrg.png'))
                else:
                    batt_icon = Image.open(os.path.join(picdir, 'Battery_chrg_full.png'))
                btx = 5
                bty = (screen.height - 5) - int(batt_icon.height)
                imageB.paste(batt_icon, (btx,bty), batt_icon)
            else:
                if battlevel.level > 20:
                    if battlevel.level == 100:
                        batt_icon = Image.open(os.path.join(picdir, 'Battery_full.png'))
                    else:
                        batt_icon = Image.open(os.path.join(picdir, 'Battery.png'))
                        batt_load_txt = str(battlevel.level)
                    btx = 5
                    bty = (screen.height - 5) - int(batt_icon.height)
                    imageB.paste(batt_icon, (btx,bty), batt_icon)
                    if battlevel.level < 100:
                        t_G, t_G, batt_t_w, batt_t_h = draw_black.textbbox((0,0),batt_load_txt, font=font.SFMonth)
                        btx = btx + int(batt_icon.width/2)
                        btx = btx - int(batt_t_w/2)
                        bty = bty + int(batt_t_h/2)
                        draw_black.text((btx, bty), batt_load_txt, font=font.SFMonth, fill = black)
                else:
                    if screen.use_red == 1:
                        batt_iconB = Image.open(os.path.join(picdir, 'Battery_low_B.png'))
                        batt_iconR = Image.open(os.path.join(picdir, 'Battery_low_R.png'))
                        btx = 5
                        bty = (screen.height - 5) - int(batt_iconB.height)
                        imageB.paste(batt_iconB, (btx,bty), batt_iconB)
                        imageR.paste(batt_iconR, (btx,bty), batt_iconR)
                    else:
                        batt_icon = Image.open(os.path.join(picdir, 'Battery_low.png'))
                        btx = 5
                        bty = (screen.height - 5) - int(batt_icon.height)
                        bty = bty - 4
                        imageB.paste(batt_icon, (btx,bty), batt_icon)
        else:
            applog("Dashboard","Battery not found!")
            batt_icon = Image.open(os.path.join(picdir, 'Battery_no_batt.png'))
            btx = 5
            bty = (screen.height - 5) - int(batt_icon.height)
            imageB.paste(batt_icon, (btx,bty), batt_icon)
    else:
        applog("Dasboard","Show Power is OFF")
        dashboard.message_state+=1
    epd.display(epd.getbuffer(imageB),epd.getbuffer(imageR))
    epd.sleep()


def daily_agile_quotes():

    applog("OfficeInk" ,"Daily Agile Quotes screen initiated")

    black = 'rgb(0,0,0)'
    white = 'rgb(255,255,255)'

    try:
        applog("OfficeInk" ,"Setting Daily Agile Quotes screen variables")
        epd = epd7in5b_V2.EPD()
        epd.init()
        applog("OfficeInk" ,"INIT screen")
        epd.Clear()
        screen.height = epd.height
        screen.width = epd.width
        screen.middle_w = screen.width/2
        screen.middle_h = screen.height/2
    except IOError as e:
        applog("OfficeInk" ,"error"+str(e)) 

    except KeyboardInterrupt:
        applog("OfficeInk" ,"ctrl + c received") 
        epd7in5b_V2.epdconfig.module_exit()
        exit()
    imageB = Image.new('L', (epd.width, epd.height), 255)  # 255: clear the frame
    imageR = Image.new('L', (epd.width, epd.height), 255)  # 255: clear the frame
    draw_black = ImageDraw.Draw(imageB)
    draw_red = ImageDraw.Draw(imageR)

    
    x_master = 10
    y_master = 10

    x = x_master
    y = y_master
    screen_y = 0
    # Find out how many characters per line of screen for Quotes
    screen.quote_max = screen.width - (85 + (x_master*2))
    # Quotes Section

        #######    #######
        ####   ####   ####
        ####   ####   ####
        ####   ####   ####
        ####   ####   ####
        ####   ####   ####


    if dashboard.show_messages == 1:
        
        applog("Dashboard","Daily Agile Quotes : ON")
            

        quote_icon = Image.open(os.path.join(picdir, "quote_icon.png"))
        quote_iconB = Image.open(os.path.join(picdir, "quote_b.png"))
        quote_iconR = Image.open(os.path.join(picdir, "quote_r.png"))
    

        x = x_master
        if screen_y == 0:
            y = y_master
        else:
            y = screen_y
        qx = x
        qy = y
      
    
        qml = dashboard.quote_length
        qll = qml+1
        qmaxtries = 0
        applog("Message of the day" ,"Time to get a Agile Quote...")

        applog("Message of the day" ,"Getting a message under "+str(qml)+" lenght")

        while qll >= qml :
            applog("Message state","Getting a quote")
            applog("Agile Quotes of the day" ,"Getting random quote from local database...")
            dashboard.quote = quotefromfile("agile_quotes.txt")
            qll = len(dashboard.quote.quote_text)
            qmaxtries +=1
            if qmaxtries > 10:
                break

            if qll >  qml:
                applog("Agile Quotes of the day" ,"Message Feature : Attempt: "+str(qmaxtries))
            else:
                applog("Agile Quotes of the day" ,"Message lenght is "+str(qll))



        if qll == 0 or qll > qml:
            applog("Agile Quotes of the day" ,"Max attempts to get a short enough quote exhausted.")
            #Just in case we could not find a short enough quote in 10 attempts.
            dashboard.quote.quote_text = "Somethings looking for a quote becomes the quote itself..."
            dashboard.quote.quote_author = "Dashboard Ai Error ;("
            hourglass.day = -1

        daily_message = dashboard.quote.quote_text
        
        #print("Now trying to slice the text in chunks")
        text_g, text_g, test_t_w, test_t_h = draw_black.textbbox((0,0),daily_message, font=font.SFQuote)
        text_max = test_t_w
        toff = x + int(quote_icon.size[0]+2)
        screen.offset = int( quote_icon.size[0] + (x_master * 2) )
        text_line_max = screen.quote_max - (toff + screen.offset)

        text_line = []
        textbuffer = ""

        #Show the quote icon status
        if screen.use_red == 1:
            imageB.paste(quote_iconB,(qx,qy),quote_iconB)
            imageR.paste(quote_iconR,(qx,qy),quote_iconR)
        else:
            imageB.paste(quote_icon,(qx,qy),quote_icon)

        #Split the quote into words in an array

        quote_words = daily_message.split()
        wl = len(quote_words)

        #See if the total is larger than the text_line_max value set.
        applog("Agile Quotes of the day" ,"Max pixels per line is "+str(text_line_max))
        t_g, t_g, test_t_w, test_t_h = draw_black.textbbox((0,0),daily_message, font=font.SFQuote)

        if test_t_w > text_line_max:
            l = 0
            ql = len(quote_words)
            while l < ql:
                textbuffer = textbuffer + quote_words[l] + " "
                l += 1
                t_g, t_g, test_t_w, test_t_h = draw_black.textbbox((0,0),textbuffer, font=font.SFQuote)
                #print(textbuffer)
                if test_t_w >= text_line_max:
                    text_line.append(textbuffer)
                    textbuffer = ""
                    #print(l)
            if (len(textbuffer)):
                text_line.append(textbuffer)
        else :
            applog("Agile Quotes of the day" ,"Message fits in one row...")
            if len(daily_message):
                applog("Agile Quotes of the day" ,"Using only one row here.")
                text_line.append(daily_message)
                t_g, t_g, test_t_w, test_t_h = draw_black.textbbox((0,0),daily_message, font=font.SFQuote)
            else :
                text_line = "Oops there is a bug here..."
                dashboard.quote.quote_author = "Dashboard Ai Error ;("
                t_g, t_g, test_t_w, test_t_h = draw_black.textbbox((0,0),daily_message, font=font.SFQuote)
                applog("Agile Quotes of the day" ,"QUOTE IS EMPTY!.")


        # Get number of arrays generated
        qs = len(text_line)
        qc = 0
        #qx = 20
    
        g_w = 0
        q_h = 0
        q_w = 0
    
        #Getting the widest line of text
        tq_g, tq_g, tq_w, tq_h = draw_black.textbbox((0,0),text_line[qc], font=font.SFQuote)
        for i in text_line:
            tq_g, tq_g, tq_w, tq_h = draw_black.textbbox((0,0),i, font=font.SFQuote)
            q_h = tq_h
            if tq_w > q_w :
                q_w = tq_w
            qc +=1

        quote_total_height = int(tq_h * qs)
        
        aqG, aqG, aq_w, aq_h = draw_black.textbbox((0,0),"- "+dashboard.quote.quote_author, font=font.SFQuoteAuthor)

        quote_total_height = int(quote_total_height + aq_h)

        applog("Agile Quotes of the day","Total message height is "+str(quote_total_height))

        #Writing the quote line by line.
        qc = 0
        gTy = qy

        # Setting gTy to be in the middle

        gTy = screen.middle_h - int(quote_total_height/2)

        # Setting gTy to be in the middle

        gTx = x + int(quote_icon.size[0]+2)


        while qc < qs:
            tq_g, tq_g, tq_ww, tq_g = draw_black.textbbox((0,0),text_line[qc], font=font.SFQuote)
            gTx = screen.middle_w - int(tq_ww/2)
            draw_black.text((gTx, gTy), text_line[qc], font=font.SFQuote, fill=black)
            #print(text_line[qc])
            qc += 1
            gTy = gTy + int(q_h)
            #if qc == 1:
            #    gTx = gTx + 20
        
        qG, qG, q_w, q_h = draw_black.textbbox((0,0),"- "+dashboard.quote.quote_author, font=font.SFQuoteAuthor)
        gTx = int(screen.middle_w - q_w/2)
        gTy = gTy -2
        if screen.use_red == 1:
            draw_red.text((gTx, gTy), "- "+dashboard.quote.quote_author, font=font.SFQuoteAuthor, fill=black)
        else :
            draw_black.text((gTx, gTy), "- "+dashboard.quote.quote_author, font=font.SFQuoteAuthor, fill=black)
    
        gTy = gTy + int(q_h) + 2
        screen_y = gTy

        ###########################
        # End of Message of the day
        ###########################
    else:
        applog("Dashboard","Agile Quotes of the day feature : OFF")
    
    nextrefreshtime = datetime.now() + timedelta(minutes=int(screen.refresh_rate_min))
    hourglass.last_refresh = "Daily Quote, "+hourglass.last_refresh
    #hourglass.last_refresh = hourglass.last_refresh + " next @ " + nextrefreshtime.strftime("%H:%M")
    #hourglass.last_refresh = "Counter @ "+str(performance.countr)
    applog("Dashoard","Show the last refresh text at the bottom, centered "+hourglass.last_refresh)
    t_G, t_G, test_t_w, test_t_h = draw_black.textbbox((0,0),hourglass.last_refresh, font=font.SFMonth)
    gTx = int(screen.middle_w) - int(test_t_w/2)
    gTy = screen.height - int(test_t_h + 4)
    draw_black.text((gTx, gTy), hourglass.last_refresh, font=font.SFMonth, fill=black)

    if dashboard.show_power == 1:
        # DEBUG BATTERY
        #battlevel.state = "Not Charging"
        #battlevel.level = 10
    
        applog("Dashoard","Getting battery status and level...")
        battlevel = get_pibatt()

        if battlevel.level !=-1: #Checking if battery level can be goten -1 means error
            applog("Dashoard","Loading battery icon and drawing status bottom left")
            applog("Dashboard","Battery state: "+battlevel.state+" @ "+str(battlevel.level)+"%")
            if battlevel.state == "Charging":
                if battlevel.level <100:
                    batt_icon = Image.open(os.path.join(picdir, 'Battery_chrg.png'))
                else:
                    batt_icon = Image.open(os.path.join(picdir, 'Battery_chrg_full.png'))
                btx = 5
                bty = (screen.height - 5) - int(batt_icon.height)
                imageB.paste(batt_icon, (btx,bty), batt_icon)
            else:
                if battlevel.level > 20:
                    if battlevel.level == 100:
                        batt_icon = Image.open(os.path.join(picdir, 'Battery_full.png'))
                    else:
                        batt_icon = Image.open(os.path.join(picdir, 'Battery.png'))
                        batt_load_txt = str(battlevel.level)
                    btx = 5
                    bty = (screen.height - 5) - int(batt_icon.height)
                    imageB.paste(batt_icon, (btx,bty), batt_icon)
                    if battlevel.level < 100:
                        t_G, t_G, batt_t_w, batt_t_h = draw_black.textbbox((0,0),batt_load_txt, font=font.SFMonth)
                        btx = btx + int(batt_icon.width/2)
                        btx = btx - int(batt_t_w/2)
                        bty = bty + int(batt_t_h/2)
                        draw_black.text((btx, bty), batt_load_txt, font=font.SFMonth, fill = black)
                else:
                    if screen.use_red == 1:
                        batt_iconB = Image.open(os.path.join(picdir, 'Battery_low_B.png'))
                        batt_iconR = Image.open(os.path.join(picdir, 'Battery_low_R.png'))
                        btx = 5
                        bty = (screen.height - 5) - int(batt_iconB.height)
                        imageB.paste(batt_iconB, (btx,bty), batt_iconB)
                        imageR.paste(batt_iconR, (btx,bty), batt_iconR)
                    else:
                        batt_icon = Image.open(os.path.join(picdir, 'Battery_low.png'))
                        btx = 5
                        bty = (screen.height - 5) - int(batt_icon.height)
                        bty = bty - 4
                        imageB.paste(batt_icon, (btx,bty), batt_icon)
        else:
            applog("Dashboard","Battery not found!")
            batt_icon = Image.open(os.path.join(picdir, 'Battery_no_batt.png'))
            btx = 5
            bty = (screen.height - 5) - int(batt_icon.height)
            imageB.paste(batt_icon, (btx,bty), batt_icon)
    else:
        applog("Dasboard","Show Power is OFF")
        dashboard.message_state+=1
    epd.display(epd.getbuffer(imageB),epd.getbuffer(imageR))
    epd.sleep()


def daily_dadjokes():

    applog("OfficeInk" ,"Daily Message screen initiated")

    black = 'rgb(0,0,0)'
    white = 'rgb(255,255,255)'

    try:
        applog("OfficeInk" ,"Setting Daily Message screen variables")
        epd = epd7in5b_V2.EPD()
        epd.init()
        applog("OfficeInk" ,"INIT screen")
        epd.Clear()
        screen.height = epd.height
        screen.width = epd.width
        screen.middle_w = screen.width/2
        screen.middle_h = screen.height/2
    except IOError as e:
        applog("OfficeInk" ,"error"+str(e)) 

    except KeyboardInterrupt:
        applog("OfficeInk" ,"ctrl + c received") 
        epd7in5b_V2.epdconfig.module_exit()
        exit()
    imageB = Image.new('L', (epd.width, epd.height), 255)  # 255: clear the frame
    imageR = Image.new('L', (epd.width, epd.height), 255)  # 255: clear the frame
    draw_black = ImageDraw.Draw(imageB)
    draw_red = ImageDraw.Draw(imageR)

    
    x_master = 10
    y_master = 10

    x = x_master
    y = y_master
    screen_y = 0
    # Find out how many characters per line of screen for Quotes
    screen.quote_max = screen.width - (85 + (x_master*2))
    #screen.offset = 95
    #applog("debug","screen.quote_max = "+str(screen.quote_max))
    #applog("debug","screen.offset = "+str(screen.offset))
    #applog("debug","message state = "+str(dashboard.message_state))

    # Message Section

        #######    #######
        ####   ####   ####
        ####   ####   ####
        ####   ####   ####
        ####   ####   ####
        ####   ####   ####


    if dashboard.show_messages == 1 :
        
        applog("Dashboard","Daily Messages : ON")
            

        if dashboard.show_dadjoke_live == 0:
            applog("Message of the day" ,"File Joke db selected ")
            dad_joke_icon = Image.open(os.path.join(picdir, "dad_quote.png"))
            dad_joke_iconB = Image.open(os.path.join(picdir, "dad_quote_bf.png"))
            dad_joke_iconR = Image.open(os.path.join(picdir, "dad_quote_r.png"))
        else:
            applog("Message of the day" ,"LIVE Joke selected ")
            dad_joke_icon = Image.open(os.path.join(picdir, "dad_quotef.png"))
            dad_joke_iconB = Image.open(os.path.join(picdir, "dad_quote_b.png"))
            dad_joke_iconR = Image.open(os.path.join(picdir, "dad_quote_r.png"))


        x = x_master
        if screen_y == 0:
            y = y_master
        else:
            y = screen_y
        qx = x
        qy = y
      
    
        qml = dashboard.quote_length
        qll = qml+1
        qmaxtries = 0

        applog("Message state","Getting a Dad-Joke ...")
        qml = dashboard.quote_length
        qll = qml+1
        qmaxtries = 0

        while qll >= qml :
            applog("Message state","Getting a Dad-Joke from local DB")
            dashboard.dadjoke = dadjokefromfile("dadjokes.txt").replace('\n', ' ' )
            qll = len(dashboard.dadjoke)
            qmaxtries +=1
            if qmaxtries > 10:
                break
            if qll >  qml:
                applog("Message of the day" ,"Message Feature : Attempt: "+str(qmaxtries))
            else:
                applog("Message of the day" ,"Joke lenght is "+str(qll))
        if qll == 0 or qll > qml:
            applog("Quote of the day" ,"Max attempts to get a short enough quote exhausted.")
            #Just in case we could not find a short enough quote in 10 attempts.
            dashboard.dadjoke = "Sorry, No Dad Joke Quote found, I would wait for another..."
            hourglass.day = -1

        daily_message = dashboard.dadjoke
        
        #print("Now trying to slice the text in chunks")
        text_g, text_g, test_t_w, test_t_h = draw_black.textbbox((0,0),daily_message, font=font.SFQuote)
        text_max = test_t_w
        toff = x + int(dad_joke_icon.size[0]+2)
        screen.offset = int( dad_joke_icon.size[0] + (x_master * 2) )
        text_line_max = screen.quote_max - (toff + screen.offset)

        text_line = []
        textbuffer = ""

        #Show the Joke icon status
        if screen.use_red == 1:
            imageB.paste(dad_joke_iconB,(qx,qy),dad_joke_iconB)
            imageR.paste(dad_joke_iconR,(qx,qy),dad_joke_iconR)
        else:
            imageB.paste(dad_joke_icon,(qx,qy),dad_joke_icon)

        #Split the quote into words in an array

        quote_words = daily_message.split()
        wl = len(quote_words)

        #See if the total is larger than the text_line_max value set.
        applog("Message of the day" ,"Max pixels per line is "+str(text_line_max))
        t_g, t_g, test_t_w, test_t_h = draw_black.textbbox((0,0),daily_message, font=font.SFQuote)

        if test_t_w > text_line_max:
            l = 0
            ql = len(quote_words)
            while l < ql:
                textbuffer = textbuffer + quote_words[l] + " "
                l += 1
                t_g, t_g, test_t_w, test_t_h = draw_black.textbbox((0,0),textbuffer, font=font.SFQuote)
                #print(textbuffer)
                if test_t_w >= text_line_max:
                    text_line.append(textbuffer)
                    textbuffer = ""
                    #print(l)
            if (len(textbuffer)):
                text_line.append(textbuffer)
        else :
            applog("Message of the day" ,"Message fits in one row...")
            if len(daily_message):
                applog("Message of the day" ,"Using only one row here.")
                text_line.append(daily_message)
                t_g, t_g, test_t_w, test_t_h = draw_black.textbbox((0,0),daily_message, font=font.SFQuote)
            else :
                text_line = "Oops there is a bug here..."
                t_g, t_g, test_t_w, test_t_h = draw_black.textbbox((0,0),daily_message, font=font.SFQuote)
                applog("Message of the day" ,"QUOTE IS EMPTY!.")

        applog("Message of the day" ,"DEBUG********* Measured pixels per line is "+str(test_t_w))

        # Get number of arrays generated
        qs = len(text_line)
        qc = 0
        #qx = 20
    
        g_w = 0
        q_h = 0
        q_w = 0
    
        #Getting the widest line of text
        tq_g, tq_g, tq_w, tq_h = draw_black.textbbox((0,0),text_line[qc], font=font.SFQuote)
        for i in text_line:
            tq_g, tq_g, tq_w, tq_h = draw_black.textbbox((0,0),i, font=font.SFQuote)
            q_h = tq_h
            if tq_w > q_w :
                q_w = tq_w
            qc +=1

        quote_total_height = int(tq_h * (qc+1))
        applog("Message of the day","Total message height is "+str(quote_total_height))
        applog("Message ",daily_message)



        #Writing the quote line by line.
        qc = 0
        gTy = qy

        # Setting gTy to be in the middle

        gTy = screen.middle_h - int(quote_total_height/2)

        # Setting gTy to be in the middle

        gTx = x + int(dad_joke_icon.size[0]+2)


        while qc < qs:
            tq_g, tq_g, tq_ww, tq_g = draw_black.textbbox((0,0),text_line[qc], font=font.SFQuote)
            gTx = screen.middle_w - int(tq_ww/2)
            draw_black.text((gTx, gTy), text_line[qc], font=font.SFQuote, fill=black)
            #print(text_line[qc])
            qc += 1
            gTy = gTy + int(q_h)
            #if qc == 1:
            #    gTx = gTx + 20
        
        screen_y = gTy

        ###########################
        # End of Message of the day
        ###########################
    else:
        applog("Dashboard","Message of the day feature : OFF")

    nextrefreshtime = datetime.now() + timedelta(minutes=int(screen.refresh_rate_min))
    #hourglass.last_refresh = hourglass.last_refresh + " next @ " + nextrefreshtime.strftime("%H:%M")
    hourglass.last_refresh = "Dad Joke of the day, "+ hourglass.last_refresh
    applog("Dashoard","Show the last refresh text at the bottom, centered "+hourglass.last_refresh)
    t_G, t_G, test_t_w, test_t_h = draw_black.textbbox((0,0),hourglass.last_refresh, font=font.SFMonth)
    gTx = int(screen.middle_w) - int(test_t_w/2)
    gTy = screen.height - int(test_t_h + 4)
    draw_black.text((gTx, gTy), hourglass.last_refresh, font=font.SFMonth, fill=black)

    if dashboard.show_power == 1:
        # DEBUG BATTERY
        #battlevel.state = "Not Charging"
        #battlevel.level = 10
    
        applog("Dashoard","Getting battery status and level...")
        battlevel = get_pibatt()

        if battlevel.level !=-1: #Checking if battery level can be goten -1 means error
            applog("Dashoard","Loading battery icon and drawing status bottom left")
            applog("Dashboard","Battery state: "+battlevel.state+" @ "+str(battlevel.level)+"%")
            if battlevel.state == "Charging":
                if battlevel.level <100:
                    batt_icon = Image.open(os.path.join(picdir, 'Battery_chrg.png'))
                else:
                    batt_icon = Image.open(os.path.join(picdir, 'Battery_chrg_full.png'))
                btx = 5
                bty = (screen.height - 5) - int(batt_icon.height)
                imageB.paste(batt_icon, (btx,bty), batt_icon)
            else:
                if battlevel.level > 20:
                    if battlevel.level == 100:
                        batt_icon = Image.open(os.path.join(picdir, 'Battery_full.png'))
                    else:
                        batt_icon = Image.open(os.path.join(picdir, 'Battery.png'))
                        batt_load_txt = str(battlevel.level)
                    btx = 5
                    bty = (screen.height - 5) - int(batt_icon.height)
                    imageB.paste(batt_icon, (btx,bty), batt_icon)
                    if battlevel.level < 100:
                        t_G, t_G, batt_t_w, batt_t_h = draw_black.textbbox((0,0),batt_load_txt, font=font.SFMonth)
                        btx = btx + int(batt_icon.width/2)
                        btx = btx - int(batt_t_w/2)
                        bty = bty + int(batt_t_h/2)
                        draw_black.text((btx, bty), batt_load_txt, font=font.SFMonth, fill = black)
                else:
                    if screen.use_red == 1:
                        batt_iconB = Image.open(os.path.join(picdir, 'Battery_low_B.png'))
                        batt_iconR = Image.open(os.path.join(picdir, 'Battery_low_R.png'))
                        btx = 5
                        bty = (screen.height - 5) - int(batt_iconB.height)
                        imageB.paste(batt_iconB, (btx,bty), batt_iconB)
                        imageR.paste(batt_iconR, (btx,bty), batt_iconR)
                    else:
                        batt_icon = Image.open(os.path.join(picdir, 'Battery_low.png'))
                        btx = 5
                        bty = (screen.height - 5) - int(batt_icon.height)
                        bty = bty - 4
                        imageB.paste(batt_icon, (btx,bty), batt_icon)
        else:
            applog("Dashboard","Battery not found!")
            batt_icon = Image.open(os.path.join(picdir, 'Battery_no_batt.png'))
            btx = 5
            bty = (screen.height - 5) - int(batt_icon.height)
            imageB.paste(batt_icon, (btx,bty), batt_icon)
    else:
        applog("Dasboard","Show Power is OFF")
        dashboard.message_state+=1

    epd.display(epd.getbuffer(imageB),epd.getbuffer(imageR))
    epd.sleep()

def daily_comic():

    applog("OfficeInk" ,"Daily Message screen initiated")

    black = 'rgb(0,0,0)'
    white = 'rgb(255,255,255)'

    try:
        applog("OfficeInk" ,"Setting Daily Message screen variables")
        epd = epd7in5b_V2.EPD()
        epd.init()
        applog("OfficeInk" ,"INIT screen")
        epd.Clear()
        screen.height = epd.height
        screen.width = epd.width
        screen.middle_w = screen.width/2
        screen.middle_h = screen.height/2
    except IOError as e:
        applog("OfficeInk" ,"error"+str(e)) 

    except KeyboardInterrupt:
        applog("OfficeInk" ,"ctrl + c received") 
        epd7in5b_V2.epdconfig.module_exit()
        exit()
    imageB = Image.new('L', (epd.width, epd.height), 255)  # 255: clear the frame
    imageR = Image.new('L', (epd.width, epd.height), 255)  # 255: clear the frame
    draw_black = ImageDraw.Draw(imageB)
    draw_red = ImageDraw.Draw(imageR)

    
    x_master = 10
    y_master = 10

    x = x_master
    y = y_master
    screen_y = 0
    # Find out how many characters per line of screen for Quotes
    screen.quote_max = screen.width - (85 + (x_master*2))

    # Message Section

        #######    #######
        ####   ####   ####
        ####   ####   ####
        ####   ####   ####
        ####   ####   ####
        ####   ####   ####

        ####################### COMIC ###############################
        
    if dashboard.show_comic == 1:
        applog("Dashboard","Comic of the day feature : ON")
        shape = [(0, 0), (screen.width, screen.height)] 
  
  
        # create rectangle image 
        draw_black.rectangle(shape, fill =white) 
        draw_red.rectangle(shape, fill =white) 


        comic_file = getcomic(imgdir+"/agile")
        comic_image = Image.open(os.path.join(imgdir+"/agile", comic_file))
        if comic_image.size[0] > screen.width:
            comic_scale_factor = (screen.width - 10) / comic_image.size[0]
            applog("Comic Feature","Scaling the comic down to "+str(comic_scale_factor))
            comic_image = comic_image.resize((int(comic_image.size[0] * comic_scale_factor), int(comic_image.size[1] * comic_scale_factor)))
            applog("Comic Feature","Comic size is now "+str(comic_image.size[0])+" by "+str(comic_image.size[1]))
        elif comic_image.size[0] < screen.width:
            comic_scale_factor = comic_image.size[0] / (screen.width - 10)
            applog("Comic Feature","Scaling the comic up to "+str(comic_scale_factor))
            comic_image = comic_image.resize((int(comic_image.size[0] / comic_scale_factor), int(comic_image.size[1] / comic_scale_factor)))
            applog("Comic Feature","Comic size is now "+str(comic_image.size[0])+" by "+str(comic_image.size[1]))

        if comic_image.size[1] > screen.height:
            comic_scale_factor = (screen.height - 10) / comic_image.size[1]
            applog("Comic Feature","Scaling the comic down to "+str(comic_scale_factor))
            comic_image = comic_image.resize((int(comic_image.size[1] * comic_scale_factor), int(comic_image.size[1] * comic_scale_factor)))
            applog("Comic Feature","Comic size is now "+str(comic_image.size[0])+" by "+str(comic_image.size[0]))
        elif comic_image.size[1] < screen.height:
            comic_scale_factor = comic_image.size[1] / (screen.height - 10)
            applog("Comic Feature","Scaling the comic up to "+str(comic_scale_factor))
            comic_image = comic_image.resize((int(comic_image.size[1] / comic_scale_factor), int(comic_image.size[1] / comic_scale_factor)))
            applog("Comic Feature","Comic size is now "+str(comic_image.size[0])+" by "+str(comic_image.size[0]))


        Cx = int((screen.width/2)) - int((comic_image.size[0])/2)
        Cy = int(y)

        imageB.paste(comic_image,(Cx,Cy))
        screen_y = screen_y + comic_image.size[1]
    else:
        applog("Dashboard","Comic of the day feature : OFF")

        ###########################
        # End of Message of the day
        ###########################
    
    nextrefreshtime = datetime.now() + timedelta(minutes=int(screen.refresh_rate_min))
    #hourglass.last_refresh = hourglass.last_refresh + " next @ " + nextrefreshtime.strftime("%H:%M")
    hourglass.last_refresh = "Dad Joke of the day"
    applog("Dashoard","Show the last refresh text at the bottom, centered "+hourglass.last_refresh)
    t_G, t_G, test_t_w, test_t_h = draw_black.textbbox((0,0),hourglass.last_refresh, font=font.SFMonth)
    gTx = int(screen.middle_w) - int(test_t_w/2)
    gTy = screen.height - int(test_t_h + 4)
    draw_black.text((gTx, gTy), hourglass.last_refresh, font=font.SFMonth, fill=black)

    if dashboard.show_power == 1:
        # DEBUG BATTERY
        #battlevel.state = "Not Charging"
        #battlevel.level = 10
    
        applog("Dashoard","Getting battery status and level...")
        battlevel = get_pibatt()

        if battlevel.level !=-1: #Checking if battery level can be goten -1 means error
            applog("Dashoard","Loading battery icon and drawing status bottom left")
            applog("Dashboard","Battery state: "+battlevel.state+" @ "+str(battlevel.level)+"%")
            if battlevel.state == "Charging":
                if battlevel.level <100:
                    batt_icon = Image.open(os.path.join(picdir, 'Battery_chrg.png'))
                else:
                    batt_icon = Image.open(os.path.join(picdir, 'Battery_chrg_full.png'))
                btx = 5
                bty = (screen.height - 5) - int(batt_icon.height)
                imageB.paste(batt_icon, (btx,bty), batt_icon)
            else:
                if battlevel.level > 20:
                    if battlevel.level == 100:
                        batt_icon = Image.open(os.path.join(picdir, 'Battery_full.png'))
                    else:
                        batt_icon = Image.open(os.path.join(picdir, 'Battery.png'))
                        batt_load_txt = str(battlevel.level)
                    btx = 5
                    bty = (screen.height - 5) - int(batt_icon.height)
                    imageB.paste(batt_icon, (btx,bty), batt_icon)
                    if battlevel.level < 100:
                        t_G, t_G, batt_t_w, batt_t_h = draw_black.textbbox((0,0),batt_load_txt, font=font.SFMonth)
                        btx = btx + int(batt_icon.width/2)
                        btx = btx - int(batt_t_w/2)
                        bty = bty + int(batt_t_h/2)
                        draw_black.text((btx, bty), batt_load_txt, font=font.SFMonth, fill = black)
                else:
                    if screen.use_red == 1:
                        batt_iconB = Image.open(os.path.join(picdir, 'Battery_low_B.png'))
                        batt_iconR = Image.open(os.path.join(picdir, 'Battery_low_R.png'))
                        btx = 5
                        bty = (screen.height - 5) - int(batt_iconB.height)
                        imageB.paste(batt_iconB, (btx,bty), batt_iconB)
                        imageR.paste(batt_iconR, (btx,bty), batt_iconR)
                    else:
                        batt_icon = Image.open(os.path.join(picdir, 'Battery_low.png'))
                        btx = 5
                        bty = (screen.height - 5) - int(batt_icon.height)
                        bty = bty - 4
                        imageB.paste(batt_icon, (btx,bty), batt_icon)
        else:
            applog("Dashboard","Battery not found!")
            batt_icon = Image.open(os.path.join(picdir, 'Battery_no_batt.png'))
            btx = 5
            bty = (screen.height - 5) - int(batt_icon.height)
            imageB.paste(batt_icon, (btx,bty), batt_icon)
    else:
        applog("Dasboard","Show Power is OFF")
        dashboard.message_state+=1

    epd.display(epd.getbuffer(imageB),epd.getbuffer(imageR))
    epd.sleep()


def get_pibatt():
    try:
        conn, event_conn = connect_tcp('127.0.0.1')
        s = PiSugarServer(conn, event_conn)

        s.register_single_tap_handler(lambda: print('single'))
        s.register_double_tap_handler(lambda: print('double'))
        battery.level = int(s.get_battery_level())
        bstate = s.get_battery_charging()
        if bstate == True:
            battery.state = "Charging"
        else:
            battery.state = "Not Charging"

        return_data = battery(level=battery.level,state=battery.state)
    except:
        return_data = battery(level=-1,
                            state="Unknown")
        applog("System","Getting battery state error")
    
    try:
        applog("Battery subsystem","Force a time sync...")
        picmd ="echo 'rtc_rtc2pi' | nc -q 0 127.0.0.1 8423"
        os.system(picmd)
    except:
        applog("Battery subsystem","Force a time sync - FAILED")

    return return_data

def crashlog(file_path:str, crash_message: str):
    subdir = os.path.dirname(file_path)
    #print(subdir)
    if os.path.exists(subdir) == False:
        os.mkdir(subdir)
    aqi_array = []
    date_time_stamp = datetime.now().strftime("%d.%b.%Y, %H:%M:%S")
    my_file = open(file_path, 'a')
    applog("Inkscreen" ,"Logging crash message")
    my_file.write(date_time_stamp+" | "+crash_message+'\n')
    my_file.close

def applog(app_section: str ,app_message: str):
    if performance.debug == 1:
        date_time_stamp = datetime.now().strftime("%d.%b.%Y, %H:%M:%S")
        print(date_time_stamp+" | "+app_section+" | "+app_message)

def sleep_screen(wake_date:date):
    applog("Inkframe" ,"Sleeping screen initiated")

    black = 'rgb(0,0,0)'
    white = 'rgb(255,255,255)'
    try:

        epd = epd7in5b_V2.EPD()
        epd.init()
        epd.Clear()
        screen.height = epd.height
        screen.width = epd.width
        screen.middle_w = screen.width/2
        screen.middle_h = screen.height/2
    except IOError as e:
        applog("Inkframe" ,"error"+str(e)) 

    except KeyboardInterrupt:
        applog("Inkframe" ,"ctrl + c received") 
        epd7in5b_V2.epdconfig.module_exit()
        exit()
    imageB = Image.new('L', (epd.width, epd.height), 255)  # 255: clear the frame
    imageR = Image.new('L', (epd.width, epd.height), 255)  # 255: clear the frame
    draw_black = ImageDraw.Draw(imageB)

    sleep_icon = Image.open(os.path.join(picdir, 'sleep_icon.png'))

    sleep_string = "Good Night..."
    t_g, t_g, test_t_w, test_t_h = draw_black.textbbox((0,0),sleep_string, font=font.SleepFont)

    sX = int(screen.middle_w) - int(sleep_icon.size[0]/2)
    sY = int(screen.middle_h) - int(sleep_icon.size[1]/2)
    sY = sY - int(test_t_h)
    imageB.paste(sleep_icon, (sX,sY), sleep_icon)

    sX = int(screen.middle_w) - int(test_t_w/2)
    sY = int(sY + sleep_icon.size[1]) + 4
    draw_black.text((sX, sY), sleep_string, font = font.SleepFont, fill = 'rgb(0,0,0)')

    sleep_string = "Screen will wakeup tomorrow at "+str(screen.wake_hour)+", sleep well!"
    t_g, t_g, test_t_w, test_t_h = draw_black.textbbox((0,0),sleep_string, font=font.SleepFont_foot)
    sX = int(screen.width - (int(test_t_w) + 5))
    sY = int(screen.height - (int(test_t_h) + 5))
    draw_black.text((sX, sY), sleep_string, font = font.SleepFont_foot, fill = 'rgb(0,0,0)')

    epd.display(epd.getbuffer(imageB),epd.getbuffer(imageR))
    epd.sleep()
    wakeup_day = wake_date.strftime("%d")
    applog("Sleep screen" ,"Set to wake up on the "+wakeup_day)
    while True:
        applog("Sleep screen" ,"Entring deep sleep...")
        if datetime.now().strftime("%d") == wakeup_day:
            if int(datetime.now().strftime("%H")) >= screen.wake_hour:
                break
        applog("Sleep screen" ,"Sleeping for one hour")
        time.sleep(3600)

def weekend_screen():
    applog("Inkframe" ,"Weekend screen initiated")

    black = 'rgb(0,0,0)'
    white = 'rgb(255,255,255)'
    try:

        epd = epd7in5b_V2.EPD()
        epd.init()
        epd.Clear()
        screen.height = epd.height
        screen.width = epd.width
        screen.middle_w = screen.width/2
        screen.middle_h = screen.height/2
    except IOError as e:
        applog("Inkframe" ,"error"+str(e)) 

    except KeyboardInterrupt:
        applog("Inkframe" ,"ctrl + c received") 
        epd7in5b_V2.epdconfig.module_exit()
        exit()
    imageB = Image.new('L', (epd.width, epd.height), 255)  # 255: clear the frame
    imageR = Image.new('L', (epd.width, epd.height), 255)  # 255: clear the frame
    draw_black = ImageDraw.Draw(imageB)

    sleep_icon = Image.open(os.path.join(picdir, 'weekend_icon.png'))
    sleep_iconB = Image.open(os.path.join(picdir, 'weekend_icon_B.png'))
    sleep_iconR = Image.open(os.path.join(picdir, 'weekend_icon_R.png'))


    sleep_string = "Have a great weekend!"
    t_g, t_g, test_t_w, test_t_h = draw_black.textbbox((0,0),sleep_string, font=font.SleepFont)

    sX = int(screen.middle_w) - int(sleep_icon.size[0]/2)
    sY = int(screen.middle_h) - int(sleep_icon.size[1]/2)
    sY = sY - int(test_t_h)
    if screen.use_red == 1:
        imageB.paste(sleep_iconB, (sX,sY), sleep_iconB)
        imageR
        .paste(sleep_iconR, (sX,sY), sleep_iconR)
    else:
        imageB.paste(sleep_icon, (sX,sY), sleep_icon)

    sX = int(screen.middle_w) - int(test_t_w/2)
    sY = int(sY + sleep_icon.size[1]) + 4
    draw_black.text((sX, sY), sleep_string, font = font.SleepFont, fill = 'rgb(0,0,0)')

    sleep_string = "Screen will wakeup Monday"
    t_g, t_g, test_t_w, test_t_h = draw_black.textbbox((0,0),sleep_string, font=font.SleepFont_foot)
    sX = int(screen.width - (int(test_t_w) + 5))
    sY = int(screen.height - (int(test_t_h) + 5))
    draw_black.text((sX, sY), sleep_string, font = font.SleepFont_foot, fill = 'rgb(0,0,0)')

    epd.display(epd.getbuffer(imageB),epd.getbuffer(imageR))
    epd.sleep()



def cu2morrow():
    applog("Inkframe" ,"See you tomorrow. screen initiated")

    black = 'rgb(0,0,0)'
    white = 'rgb(255,255,255)'
    try:

        epd = epd7in5b_V2.EPD()
        epd.init()
        epd.Clear()
        screen.height = epd.height
        screen.width = epd.width
        screen.middle_w = screen.width/2
        screen.middle_h = screen.height/2
    except IOError as e:
        applog("Inkframe" ,"error"+str(e)) 

    except KeyboardInterrupt:
        applog("Inkframe" ,"ctrl + c received") 
        epd7in5b_V2.epdconfig.module_exit()
        exit()
    imageB = Image.new('L', (epd.width, epd.height), 255)  # 255: clear the frame
    imageR = Image.new('L', (epd.width, epd.height), 255)  # 255: clear the frame
    draw_black = ImageDraw.Draw(imageB)

    sleep_icon = Image.open(os.path.join(picdir, 'sleep_icon.png'))

    sleep_string = "Have a good evening..."
    t_g, t_g, test_t_w, test_t_h = draw_black.textbbox((0,0),sleep_string, font=font.SleepFont)

    sX = int(screen.middle_w) - int(sleep_icon.size[0]/2)
    sY = int(screen.middle_h) - int(sleep_icon.size[1]/2)
    sY = sY - int(test_t_h)
    imageB.paste(sleep_icon, (sX,sY), sleep_icon)

    sX = int(screen.middle_w) - int(test_t_w/2)
    sY = int(sY + sleep_icon.size[1]) + 4
    draw_black.text((sX, sY), sleep_string, font = font.SleepFont, fill = 'rgb(0,0,0)')

    sleep_string = "Screen will wakeup tomorrow at "+str(screen.wake_hour)+", sleep well!"
    t_g, t_g, test_t_w, test_t_h = draw_black.textbbox((0,0),sleep_string, font=font.SleepFont_foot)
    sX = int(screen.width - (int(test_t_w) + 5))
    sY = int(screen.height - (int(test_t_h) + 5))
    draw_black.text((sX, sY), sleep_string, font = font.SleepFont_foot, fill = 'rgb(0,0,0)')

    epd.display(epd.getbuffer(imageB),epd.getbuffer(imageR))
    epd.sleep()
    time.sleep(10)
    gotosleep()



def getcomic(comicdir):
    file_list = os.listdir(comicdir)
    file_count = len(file_list)
    print("Found ",file_count," files")
    qr_n = random.randint(0,(file_count-1))
    return file_list[qr_n]


def wifi_off():
    applog("System","Turning off WiFi now...")
    cmd = 'sudo ifconfig wlan0 down'
    os.system(cmd)


def gotosleep():
    applog("Inkscreen","Shutting down the host...")
    time.sleep(20)
    call("sudo shutdown -h now", shell=True)


def main():
    performance.debug = 0
    performance.keepalive = 0
    date_time_stamp = datetime.now().strftime("%d.%b.%Y, %H:%M:%S")
    try:
        performance.cli = sys.argv
        if "debug" in sys.argv:
            performance.debug = 1
            print(date_time_stamp+" | DEBUG ON")
        if "keepalive" in sys.argv:
            performance.keepalive = 1
            print(date_time_stamp+" | Keep alive ON")
        if "help" in sys.argv:
            print(date_time_stamp+" | HELP")
            print("Commands: Office_ink.py nowelcome noclean debug wifi-off/wifi-on keepalive")
            print("nowelcome : Skips the welcome screen with system information")

            print("noclean : Skips the welcome screen with system information")
            print("nowelcome : Skips the initial screen screen cleaning")
            print("debug : shows all debug messages")
            print("wifi-off : turns wifi off")
            print("wifi-on : leaves wifi on")
            print("keepalive : overrides automatic shutdown")
            return
    except:
        performance.cli = ""
    applog("Dashboard","Checking network status...")
    get_ip()
    applog("Dashboard","Cecking for battery...")  
    battery.is_charging = False
    get_pibatt()
    applog("Dashboard","Initializing config parameters...")
    get_dashboard_config_data("OfficeInk_dashboard.ini")

    
    hourglass.day = 0
    hourglass.hourly = -1
    screen.clean_screen = 0
    dashboard.show_date = 0
    performance.countr = 0
    trend = 0
    ram = getRAMinfo()
    performance.usedram = int(ram[2])
    performance.previousram = performance.usedram
    applog("Inkscreen","Evening hour is set to: "+str(hourglass.evening_hour))
    applog("Inkscreen","Initial used RAM is: "+str(performance.usedram))
    if "nowelcome" in performance.cli:
        applog("Inkscreen","Skipping welcome screen...")
    else:
        welcome_screen(dashboard.delay_start_sec)

    if "wifi-off" in performance.cli:
        applog("Inkscreen","Turning WIFI OFF")
        wifi_off()
    elif "wifi-on" in performance.cli:
        applog("Inkscreen","WIFI Stays ON")

    while True :

        applog("Inkscreen","Screen sleep at: "+str(screen.sleep_hour))
        applog("Inkscreen","Wake up at: "+str(screen.wake_hour))
        min = 0
        hourglass.currentday = int(datetime.now().strftime("%d"))
        hourglass.last_refresh = datetime.now().strftime("Last Refresh @ %A %b %-d, %H:%M")
        hourglass.curenttime = int(datetime.now().strftime("%H"))
        hourglass.hour = int(datetime.now().strftime("%H"))
        performance.countr +=1
        applog("Inkscreen","it is now "+datetime.now().strftime("%H"))
        if datetime.now().strftime("%A") == "Monday" or datetime.now().strftime("%A") == "Tuesday" or datetime.now().strftime("%A") == "Wednesday":
            applog("Inkscreen","Time to draw the quote screen...")
            daily_agile_quotes()
        elif datetime.now().strftime("%A") == "Wednesday":
            applog("Inkscreen","Time to draw the quote screen...")
            daily_quotes()
        elif datetime.now().strftime("%A") == "Thursday" or datetime.now().strftime("%A") == "Friday":
            applog("Inkscreen","Time to draw the dad-joke screen...")
            daily_dadjokes()
        else:
            applog("Inkscreen","Its not a workday...")
            applog("Inkscreen","Time to go to sleep...")
            weekend_screen()
            gotosleep()
        ram = getRAMinfo()
        performance.usedram = int(ram[2])
        if performance.previousram > performance.usedram :
            trend = -1
            performance.ramincrease = performance.previousram - performance.usedram
        if performance.previousram < performance.usedram :
            trend = 1
            performance.ramincrease = performance.usedram - performance.previousram

        if performance.previousram == performance.usedram :
            trend = 0
            performance.ramincrease = performance.usedram - performance.previousram
            
        performance.freeram = int(ram[1])
        
        cpuT = getCPUtemperature()
        cpuU = getCPUuse()
        applog("System Performance","********************************")
        applog("System Performance","RAM: "+str(performance.usedram)+" used, and "+str(performance.freeram)+" free")
        applog("System Performance","RAM Previous was: "+str(performance.previousram))
        applog("System Performance","Battery Lewvel: "+str(battery.level))
        if trend == 1:
            applog("System Performance","Used RAM Increase by: "+str(performance.ramincrease))
        if trend == -1 :
            applog("System Performance","Used RAM Decresed by: "+str(performance.ramincrease))
        if trend == 0 :
            applog("System Performance","Used RAM unchanged")


        applog("System Performance","CPU Usage: "+cpuU)
        applog("System Performance","********************************")
        performance.previousram = performance.usedram

        if performance.keepalive == 0:

            applog("System startup","Keepalive set to OFF")
            if dashboard.shutdown_at_hour == 1 and datetime.now().hour >= int(dashboard.shutdown_hour):
                applog("Inkscreen","Passed my bedtime ("+str(dashboard.shutdown_hour)+" - Shutting down...")
                cu2morrow()
            elif dashboard.shutdown_after_run == 1 and datetime.now().hour < int(dashboard.shutdown_hour):
                    applog("Inkscreen","Running only once daily - Shutting down...")
                    gotosleep()
        else:

            applog("System startup","Keepalive set to ON")
        applog("Inkscreen","Refresh in "+str(screen.refresh_rate_min)+" minutes")
        time.sleep((screen.refresh_rate_min*60))

if __name__ == "__main__":
    main()
