#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from urllib2 import urlopen
import re
import time

# переменные, в которые записывается погода
city_name = []       # Город
t_now = []           # Температура сейчас
wind_speed_now = []  # Скорость ветра сейчас
wind_direct_now = [] # Направление ветра сейчас
icon_now = []        # Иконка погоды сейчас
icon_wind_now = []   # Иконка ветра сейчас
time_update = []     # Время обновления погоды на сайте
text_now = []        # Текст погоды сейчас
press_now = []       # Давление сейчас
hum_now = []         # Влажность сейчас
t_water_now = []     # Температура воды сейчас

t_night = []         # Температура ночью
t_night_feel = []    # Температура ночью ощущается
day = []             # День недели
date = []            # Дата
t_day = []           # Температура днем
t_day_feel = []      # Температура днем ощущается
icon = []            # Иконка погоды
icon_wind = []       # Иконка ветра
wind_speed = []      # Скорость ветра
wind_direct = []     # Направление ветра
text = []            # Текст погоды

t_tomorrow = []      # Температура завтра
icon_tomorrow = []   # Иконка погоды завтра
wind_speed_tom = []  # Скорость ветра завтра
wind_direct_tom = [] # Направление ветра завтра

t_today = []         # Температура сегодня
icon_today = []      # Иконка погоды сегодня
wind_speed_tod = []  # Скорость ветра сегодня
wind_direct_tod = [] # Направление ветра сегодня

def get_weather(weather, n, city_id, show_block_tomorrow, show_block_today, timer_bool):
    #global err_connect, splash
    global city_name, t_now, wind_speed_now, wind_direct_now, icon_now, icon_wind_now, time_update, text_now, press_now, hum_now, t_water_now, t_night, t_night_feel, day, date, t_day, t_day_feel, icon, icon_wind, wind_speed, wind_direct, text, t_tomorrow, icon_tomorrow, wind_speed_tom, wind_direct_tom, t_today, icon_today, wind_speed_tod, wind_direct_tod 
    print u'> Получаю погоду на', n, u'дней'
    print u'> Загружаю в переменную страницу', 'http://www.gismeteo.ru/city/weekly/' + str(city_id)
    try:
        source = urlopen('http://www.gismeteo.ru/city/weekly/' + str(city_id), timeout=10).read()
        print u'OK'
    except:
        print u'[!] Невозможно скачать страницу, проверьте интернет соединение'
        if timer_bool:
            print u'[!] Следующая попытка через 10 секунд'
        return False
    #### Текущая погода ####
    w_now = re.findall("type[A-Z].*>вода", source, re.DOTALL)
    
    # Город
    city_name = re.findall('type[A-Z].*\">(.*)<', w_now[0])

    # Температура
    t_now = re.findall('m_temp c.>([&minus;+]*\d+)<', w_now[0])
    for i in range(0, len(t_now)):
        if t_now[i][0] == '&':
            t_now[i] = '-' + t_now[i][7:]

    # Ветер
    wind_speed_now = re.findall('m_wind ms.*>(\d+)<', w_now[0])
    wind_direct_now = re.findall('<dt>([СЮЗВШ]+)</dt>', w_now[0])

    # Иконка
    icon_now = re.findall('url\(.*?new\/(.+)\)', w_now[0])
    
    #Иконка ветра
    icon_wind_now = re.findall('wind(\d)', w_now[0])

    # Время обновления
    time_update = re.findall('data-hr.* (\d?\d:\d\d)\s*</span>', source, re.DOTALL)
    
    # Текст погоды сейчас
    text_now = re.findall('title=\"(.*?)\"', w_now[0])
    
    # Давление сейчас
    press_now = re.findall('m_press torr\'>(\d+)<', w_now[0])
    
    # Влажность сейчас
    hum_now = re.findall('Влажность">(\d+)<', w_now[0])
    
    # Температура воды сейчас
    try:
        t_water_now = t_now[1]
    except:
        pass
    
    #### Погода на неделю ####
    # Погода ночью
    w_night_list = re.findall('Ночь</th>.*?>Утро</th>', source, re.DOTALL)
    w_night = '\n'.join(w_night_list)
    
    # Температура ночью
    t_night = re.findall('m_temp c.>([&minus;+]*\d+)<', w_night)
    for i in range(0, len(t_night)):
        if t_night[i][0] == '&':
            t_night[i] = '-' + t_night[i][7:]
    t_night_feel = t_night[1::2]
    t_night = t_night[::2]
    
    # День недели и дата
    day = re.findall('weekday.>(.*?)<', source)
    date = re.findall('s_date.>(.*?)<', source)
    
    # Погода днем
    w_day_list = re.findall('День</th>.*?>Вечер</th>', source, re.DOTALL)
    w_day = '\n'.join(w_day_list)
    
    # Температура днем
    t_day = re.findall('m_temp c.>([&minus;+]*\d+)<', w_day) 
    for i in range(0, len(t_day)):
        if t_day[i][0] == '&':
            t_day[i] = '-' + t_day[i][7:]
    t_day_feel = t_day[1::2]
    t_day = t_day[::2]
    
    # Иконка погоды днем
    icon = re.findall('src=\".*?new\/(.*?)\"', w_day)
    
    # Иконка ветра
    icon_wind = re.findall('wind(\d)', w_day)
    
    # Ветер
    wind_speed = re.findall('m_wind ms.>(\d+)', w_day)
    wind_direct = re.findall('>([СЮЗВШ]+)<', w_day)

    # Текст погоды
    text = re.findall('cltext.>(.*?)<', w_day)

    if show_block_tomorrow:
        #### Погода завтра ####
        w_tomorrow = re.findall('Ночь</th>.*?>Ночь</div>', source, re.DOTALL)
        
        # Температура
        t_tomorrow = re.findall('m_temp c.>([&minus;+]*\d+)<', w_tomorrow[1])
        for i in range(0, len(t_tomorrow)):
            if t_tomorrow[i][0] == '&':
                t_tomorrow[i] = '-' + t_tomorrow[i][7:]

        # Иконка погоды
        icon_tomorrow = re.findall('src=\".*?new\/(.*?)\"', w_tomorrow[1])

        # Ветер
        wind_speed_tom = re.findall('m_wind ms.>(\d+)', w_tomorrow[1])
        wind_direct_tom = re.findall('>([СЮЗВШ]+)<', w_tomorrow[1])
        
    if show_block_today:
        #### Погода сегодня ####
        if not show_block_tomorrow:
            w_tomorrow = re.findall('Ночь</th>.*?>Ночь</div>', source, re.DOTALL)
        
        # Температура
        t_today = re.findall('m_temp c.>([&minus;+]*\d+)<', w_tomorrow[0])
        for i in range(0, len(t_today)):
            if t_today[i][0] == '&':
                t_today[i] = '-' + t_today[i][7:]
        
        # Иконка погоды
        icon_today = re.findall('src=\".*?new\/(.*?)\"', w_tomorrow[0])

        # Ветер
        wind_speed_tod = re.findall('m_wind ms.>(\d+)', w_tomorrow[0])
        wind_direct_tod = re.findall('>([СЮЗВШ]+)<', w_tomorrow[0])
    ########
    
    if time_update:
        print u'> Обновление на сервере в', time_update[0]
    print u'> Погода получена в', time.strftime('%H:%M', time.localtime())

    # if splash:
    #     splash = False
    # записываем переменные
    for i in weather.keys():
        weather[i] = globals()[i]
    return weather