import serial
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the serial connection to the Arduino
try:
    #arduino = serial.Serial('/dev/ttyUSB1', 9600, timeout=1)
    arduino = serial.Serial('/dev/ttyUSB1', 115200, timeout=1)
    logging.info("Serial port opened successfully")
except Exception as e:
    logging.error(f"Error opening serial port: {e}")
    arduino = None

class Motor:
    def __init__(self):
        self.xcclk = b'xclk'  # Counter-clockwise command for motor 1
        self.xclk = b'xcclk'    # Clockwise command for motor 1
        self.yclk = b'ycclk'    # Clockwise command for motor 2
        self.ycclk = b'yclk'  # Counter-clockwise command for motor 2
        self.zclk = b'zcclk'    # Clockwise command for motor 3
        self.zcclk = b'zclk'  # Counter-clockwise command for motor 3

    def send_command(self, command, steps):
        message = command + b',' + str(steps).encode()
        logging.info(f"Sending command: {message}")
        try:
            if arduino and arduino.is_open:
                arduino.write(message)
                arduino.flush()  # Ensure the command is sent immediately
            else:
                logging.error("Serial port is not open")
        except Exception as e:
            logging.error(f"Error writing to serial port: {e}")

    def backward_motor1(self, steps):
        self.send_command(self.xcclk, steps)

    def forward_motor1(self, steps):
        self.send_command(self.xclk, steps)

    def forward_motor2(self, steps):
        self.send_command(self.yclk, steps)

    def backward_motor2(self, steps):
        self.send_command(self.ycclk, steps)

    def forward_motor3(self, steps):
        self.send_command(self.zclk, steps)

    def backward_motor3(self, steps):
        self.send_command(self.zcclk, steps)
