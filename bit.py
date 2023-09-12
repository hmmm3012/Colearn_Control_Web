def showLED(key: str):
    if key == "LED_READY":
        robotbit.rgb().set_pixel_color(0, neopixel.colors(NeoPixelColors.YELLOW))
        robotbit.rgb().show()
    if key == "LED_PUB":
        robotbit.rgb().set_pixel_color(0, neopixel.colors(NeoPixelColors.GREEN))
        robotbit.rgb().show()
    if key == "LED_OFF":
        robotbit.rgb().set_pixel_color(0, neopixel.colors(NeoPixelColors.RED))
        robotbit.rgb().show()

def on_uart_data_received():
    global bleReceivedValue
    basic.show_leds("""
        . # . . .
        . # # . .
        . # . # .
        . # # . .
        . # # . .
        """)
    bleReceivedValue = bluetooth.uart_read_until(serial.delimiters(Delimiters.DOLLAR))
    serial.write_line(bleReceivedValue)
bluetooth.on_uart_data_received(serial.delimiters(Delimiters.DOLLAR), on_uart_data_received)

def pub_msg_execution(msg :str):
    bluetooth.uart_write_string(msg)
    if msg == PUB_WIFI_SSID_FAILED or msg == PUB_WIFI_PWD_FAILED:
        basic.show_leds("""
        . . . . .
        . . . . .
        . . # . .
        . . . . .
        . . . . .
        """)
    elif msg == PUB_WIFI_SUCCESS:
        basic.show_leds("""
        . . # . .
        # . # . #
        # # # # #
        # . # . #
        . . # . .
        """)
    elif msg == PUB_WS_CONNECTED:
        basic.show_leds("""
        . . # . .
        # . # . #
        # # # # #
        # . # . #
        . . # . .
        """)
    elif msg == PUB_WS_FAILED or msg == PUB_WS_ERROR:
        basic.show_leds("""
        . . . . .
        . . # . .
        . # # # .
        . . # . .
        . . . . .
        """)

# Mecanum wheel lego robot

def on_data_received():
    global msg2
    direction = ""
    msg2 = serial.read_until(serial.delimiters(Delimiters.DOLLAR))
    if msg2.includes("PUB_"):

    executeMotion(direction, defaultValue)
serial.on_data_received(serial.delimiters(Delimiters.DOLLAR), on_data_received)

def on_bluetooth_connected():
    music.set_volume(255)
    music.ring_tone(988)
    basic.pause(100)
    music.set_volume(0)
    music.stop_all_sounds()
    robotbit.rgb().set_pixel_color(1, neopixel.colors(NeoPixelColors.BLUE))
    robotbit.rgb().show()
bluetooth.on_bluetooth_connected(on_bluetooth_connected)

def on_bluetooth_disconnected():
    music.set_volume(255)
    music.ring_tone(262)
    basic.pause(100)
    music.set_volume(0)
    music.stop_all_sounds()
    robotbit.rgb().set_pixel_color(1, neopixel.colors(NeoPixelColors.BLACK))
    robotbit.rgb().show()
bluetooth.on_bluetooth_disconnected(on_bluetooth_disconnected)

def driveMotors(m1a: number, m1b: number, m2a: number, m2b: number):
    robotbit.motor_run(robotbit.Motors.M1A, m1a)
    robotbit.motor_run(robotbit.Motors.M1B, m1b)
    robotbit.motor_run(robotbit.Motors.M2A, m2a)
    robotbit.motor_run(robotbit.Motors.M2B, m2b)
def get_battery_voltage():
    global adc, vol
    adc = pins.analog_read_pin(AnalogPin.P0)
    vol = 3.7 * adc / 1024
    return vol
def executeMotion(key2: str, value: number):
    if key2 == "N":
        basic.show_leds("""
            . . # . .
            . # # # .
            # . # . #
            . . # . .
            . . # . .
            """)
        driveMotors(0 - value, value, value, 0 - value)
    elif key2 == "S":
        driveMotors(value, 0 - value, 0 - value, value)
        basic.show_leds("""
            . . # . .
            . . # . .
            # . # . #
            . # # # .
            . . # . .
            """)
    elif key2 == "CW":
        driveMotors(0 - value / 4, 0 - value / 4, 0 - value / 4, 0 - value / 4)
    elif key2 == "CCW":
        driveMotors(value / 4, value / 4, value / 4, value / 4)
    elif key2 == "FCC":
        driveMotors(value / -4, value * 1, value * 1, value / -4)
    elif key2 == "FCW":
        driveMotors(value * -1, value / 4, value / 4, value * -1)
    elif key2 == "BCC":
        driveMotors(value * 1, value / -3, value / -3, value * 1)
    elif key2 == "BCW":
        driveMotors(value / 3, value * -1, value * -1, value / 3)
    elif key2 == "FL":
        driveMotors(value * 0, value * 1, value * 0, value * -1)
    elif key2 == "FR":
        driveMotors(value * -1, value * 0, value * 1, value * 0)
    elif key2 == "BL":
        driveMotors(value * 1, value * 0, value * -1, value * 0)
    elif key2 == "BR":
        driveMotors(value * 0, value * -1, value * 0, value * 1)
    elif key2 == "L":
        driveMotors(value, value, 0 - value, 0 - value)
    elif key2 == "R":
        driveMotors(0 - value, 0 - value, value, value)
    elif key2 == "STOP":
        robotbit.motor_stop_all()
    elif key2 == "Get_Bat":
        # if key2.index_of("PUB_WIFI") >= 0:
        # bluetooth.uart_write_string(key2)
        msg = "Voltage: " + ("" + str(get_battery_voltage()))
        serial.write_line(msg)
    if key2 == "a01_on":
        robotbit.geek_servo(robotbit.Servos.S1, 15)
    if key2 == "a01_off":
        robotbit.geek_servo(robotbit.Servos.S1, 35)
    showLED(key2)
vol = 0
adc = 0
msg2 = ""
bleReceivedValue = ""
defaultValue = 0
PUB_WS_CONNECTED = "PUB_WS_CONNECTED"
PUB_WS_ERROR = "PUB_WS_ERROR"
PUB_WS_CLOSE = "PUB_WS_CLOSE"
PUB_CAMERA_FAILED = "PUB_CAMERA_FAILED"
LED_READY = "LED_READY"
LED_PUB = "LED_PUB"
GET_BAT_VOL = "Get_Bat"
PUB_PARSING_FAILED = "PUB_PARSING_FAILED"
PUB_WIFI_SSID_FAILED = "PUB_WIFI_SSID_FAILED"
PUB_WIFI_PWD_FAILED = "PUB_WIFI_PWD_FAILED"
PUB_WIFI_SUCCESS = "PUB_WIFI_SUCCESS"
PUB_WS_FAILED = "PUB_WS_FAILED"
PUB_CAMERA_FAILED = "PUB_CAMERA_FAILED"
LED_PUB = "LED_PUB"
PUB_WS_FAILED = "PUB_WS_FAILED"
basic.show_leds("""
    . . . . .
    . . . . .
    . . . . .
    . . . . .
    . . . . .
    """)
bluetooth.start_uart_service()
serial.redirect(SerialPin.P14, SerialPin.P15, BaudRate.BAUD_RATE115200)
defaultValue = 255
robotbit.motor_stop_all()
showLED("led_off")
#basic.show_icon(IconNames.HEART)
basic.show_leds("""
. . # . .
# . # . #
# # # # #
# . # . #
. . # . .
""")