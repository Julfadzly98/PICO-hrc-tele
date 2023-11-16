import machine
import time
import urequests

# Define GPIO pins for trigger and echo
trigger_pin = machine.Pin(2, machine.Pin.OUT)
echo_pin = machine.Pin(3, machine.Pin.IN)

# Telegram bot settings
TELEGRAM_BOT_TOKEN = "6328941060:AAGmkPxoo900Xf1Z542jcjfoXpajRFljMVc"
YOUR_CHAT_ID = "187740907"


def connect():
    import network
 
    ssid = "Staff KML" 
    password = "stafkml@15" 
 
    station = network.WLAN(network.STA_IF)
 
    if station.isconnected() == True:
        print("Already connected")
        return
 
    station.active(True)
    station.connect(ssid, password)
 
    while station.isconnected() == False:
        pass
 
    print("Connection successful")
    print(station.ifconfig())
    
connect()



def get_distance():
    # Triggering the ultrasonic sensor
    trigger_pin.off()
    time.sleep_us(2)
    trigger_pin.on()
    time.sleep_us(10)
    trigger_pin.off()
    
    # Measuring the time for the echo
    while echo_pin.value() == 0:
        pulse_time = time.ticks_us()
    
    while echo_pin.value() == 1:
        end_time = time.ticks_us()
    
    # Calculating distance in centimeters
    pulse_duration = end_time - pulse_time
    distance_cm = (pulse_duration * 0.0343) / 2
    
    return distance_cm

def send_telegram_message(message):
    base_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": YOUR_CHAT_ID,
        "text": message
    }
    try:
        response = urequests.post(base_url, json=payload)
        if response.status_code == 200:
            print("Message sent successfully!")
        else:
            print("Failed to send message. Status code:", response.status_code)
    except Exception as e:
        print("Error sending message:", e)

try:
    while True:
        distance = get_distance()
        distance_message = f"Distance: {distance} cm"===
        print(distance_message)
        send_telegram_message(distance_message)
        time.sleep(10)  # Adjust the delay as needed
        
except KeyboardInterrupt:
    print("Measurement stopped by user")

