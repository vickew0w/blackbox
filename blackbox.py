import smbus
import time
import RPi.GPIO as GPIO
from RPLCD.i2c import CharLCD
import paho.mqtt.client as mqtt

ADC_ADDR = 0x4b
BUS = smbus.SMBus(1)

lcd = CharLCD(
    i2c_expander='PCF8574',
    address=0x27,
    port=1,
    cols=16,
    rows=2,
    auto_linebreaks=True
)

BUTTON_PIN = #pin
BUZZER_PIN = #pin
LED_PIN = #pin

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(BUTTON_PIN, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(LED_PIN, GPIO.OUT)

pos_x, pos_y = 2, 2
game_started = False

def read_adc(channel):
    BUS.write_byte(ADC_ADDR, 0x40 | channel)
    BUS.read_byte(ADC_ADDR)
    return BUS.read_byte(ADC_ADDR)

def hit_wall():
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    GPIO.output(LED_PIN, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    GPIO.output(LED_PIN, GPIO.LOW)

lcd.clear()
lcd.write_string("Presss button")

try:
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW and not game_started:
            game_started = True
            lcd.clear()
            lcd.write_string(f"({pos_x}, {pos_y})")
            time.sleep(0.5)

        if game_started:
            val_x = read_adc(1)
            val_y = read_adc(0)
            moved = False

            if val_x < 50:
                if pos_x > 0:
                    pos_x -= 1
                    moved = True
                else:
                    hit_wall()
            elif val_x > 200:
                if pos_x < 4:
                    pos_x += 1
                    moved = True
                else:
                    hit_wall()

            if val_y < 50:
                if pos_y > 0:
                    pos_y -= 1
                    moved = True
                else:
                    hit_wall()
            elif val_y > 200:
                if pos_y < 4:
                    pos_y += 1
                    moved = True
                else:
                    hit_wall()

            if moved:
                lcd.clear()
                lcd.write_string(f"Pos: ({pos_x}, {pos_y})")
                time.sleep(0.5)

        time.sleep(0.05)

except KeyboardInterrupt:
    GPIO.cleanup()
    lcd.clear()



