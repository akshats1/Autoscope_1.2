import serial
from flask import Flask, render_template, request

# Initialize the serial connection to the Arduino
try:
    arduino = serial.Serial('/dev/ttyUSB1', 9600)
except Exception as e:
    print(f"Error opening serial port: {e}")

# Define motor control commands
xcclk =b'xcclk' #b'F1\n'
xclk = b'xclk'#b'B1\n'
yclk = b'yclk'#b'F2\n'
ycclk = b'ycclk'#b'B2\n'
zclk = b'zclk'#b'F3\n'
zcclk = b'zcclk'#b'B3\n'

app = Flask(__name__)

# Define functions to send motor control commands to Arduino
def send_command(command, steps):
    message = command + b',' + str(steps).encode()
    print(f"Sending command: {message}")
    try:
        arduino.write(message)
    except Exception as e:
        print(f"Error writing to serial port: {e}")

def backward_motor1(steps):
    send_command(xcclk, steps)

def forward_motor1(steps):
    send_command(xclk, steps)

def forward_motor2(steps):
    send_command(yclk, steps)

def backward_motor2(steps):
    send_command(ycclk, steps)

def forward_motor3(steps):
    send_command(zclk, steps)

def backward_motor3(steps):
    send_command(zcclk, steps)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/motor1_forward")
def motor1_forward():
    steps = int(request.args.get("steps", 1000))
    forward_motor1(steps)
    return f"Motor 1 Forward {steps} steps"

@app.route("/motor1_backward")
def motor1_backward():
    steps = int(request.args.get("steps", 1000))
    backward_motor1(steps)
    return f"Motor 1 Backward {steps} steps"

@app.route("/motor2_forward")
def motor2_forward():
    steps = int(request.args.get("steps", 1000))
    forward_motor2(steps)
    return f"Motor 2 Forward {steps} steps"

@app.route("/motor2_backward")
def motor2_backward():
    steps = int(request.args.get("steps", 1000))
    backward_motor2(steps)
    return f"Motor 2 Backward {steps} steps"

@app.route("/motor3_forward")
def motor3_forward():
    steps = int(request.args.get("steps", 1000))
    forward_motor3(steps)
    return f"Motor 3 Forward {steps} steps"

@app.route("/motor3_backward")
def motor3_backward():
    steps = int(request.args.get("steps", 1000))
    backward_motor3(steps)
    return f"Motor 3 Backward {steps} steps"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

