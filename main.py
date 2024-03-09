#Pico W ile telegram bot kontrolü yapıyoruz.
from machine import Pin
import time, network, utelegram

# telegram API key
telegram_api_key = "-------"

# Onboard LED'in bağlı oldu pini belirliyoruz.
led = Pin("LED", Pin.OUT)
led.off()

#Pico'nun üzerindeki sıcaklık sensörünü tanımlıyoruz.
sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)

# Wifi Credentials and Wifi Conenctions
ssid = '****'
pswd = '****'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, pswd)

print("Connecting Wifi.", end='')

while not wlan.isconnected() and wlan.status() >= 0:
    print('.', end='')
    time.sleep(0.5)

print('')
print(wlan.ifconfig())

# Telegram default callback
def get_message(message):
    bot.send(message['message']['chat']['id'], "'/ping' " + " '/temp' " + " '/led 1 0' " + " '/led 1 1' ")

# send PONG text as ping reply
def reply_ping(message):
    print(message)
    bot.send(message['message']['chat']['id'], 'pong')
    
# send temp value as answer
def temp_cb(message):
    reading = sensor_temp.read_u16() * conversion_factor 
    sicaklik = round(27 - (reading - 0.706)/0.001721,2)
    # print(message)
    bot.send(message['message']['chat']['id'], sicaklik)
    
# change led status with given parameters in message text
def led_cb(message):
    msg = message['message']['text']
    msg_sp = msg.split(' ')
    print(msg_sp)
    if len(msg_sp) != 3:
        bot.send(message['message']['chat']['id'], "Yanlış Format /led 1 1")
        return
    
    if msg_sp[1] == '1':
        if msg_sp[2] == '1':
            led.on()
            bot.send(message['message']['chat']['id'], "LED YANDI")
        else:
            led.off()
            bot.send(message['message']['chat']['id'], "LED SÖNDÜ")

# start telegram bot 
bot = utelegram.ubot(telegram_api_key)

bot.register('/ping', reply_ping)       # ping message callback
bot.register('/led', led_cb)            # led message callback
bot.register('/temp', temp_cb)          # temp message callback
bot.set_default_handler(get_message)    # default message callback

print('BOT LISTENING')

bot.listen()
