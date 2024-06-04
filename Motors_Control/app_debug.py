import serial
from flask import Flask, render_template, request

# Initialize the serial connection to the Arduino
try:
    arduino = serial.Serial('/dev/ttyUSB1', 9600)
except Exception as e:
    print(f"Error opening serial port: {e}")

# Define motor control commands
xcclk = b'x_backward_command'
xclk = b'x_forward_command'
yclk = b'y_forward_command'
ycclk = b'y_backward_command'
zclk = b'z_forward_command'
zcclk = b'z_backward_command'

app = Flask(__name__)

# Define functions to send motor control commands to Arduino
def send_command(command, steps):
    message = command + b' ' + str(steps).encode()
    print(f"Sending command: {message}")
    try:
        arduino.write(message)
    except Exception as e:
        print(f"Error writing to serial port: {e}")

def backward_motor1(steps):
    send_command(xcclk, steps)  # Replace with your Arduino command for motor 1 backward

def forward_motor1(steps):
    send_command(xclk, steps)  # Replace with your Arduino command for motor 1 forward

def forward_motor2(steps):
    send_command(yclk, steps)  # Replace with your Arduino command for motor 2 forward

def backward_motor2(steps):
    send_command(ycclk, steps)  # Replace with your Arduino command for motor 2 backward

def forward_motor3(steps):
    send_command(zclk, steps)  # Replace with your Arduino command for motor 3 forward

def backward_motor3(steps):
    send_command(zcclk, steps)  # Replace with your Arduino command for motor 3 backward

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/motor1_forward")
def motor1_forward():
    steps = int(request.args.get("steps", 1000))  # Default to 1000 steps if not provided
    forward_motor1(steps)
    return f"Motor 1 Forward {steps} steps"  # Placeholder response

@app.route("/motor1_backward")
def motor1_backward():
    steps = int(request.args.get("steps", 1000))  # Default to 1000 steps if not provided
    backward_motor1(steps)
    return f"Motor 1 Backward {steps} steps"  # Placeholder response

@app.route("/motor2_forward")
def motor2_forward():
    steps = int(request.args.get("steps", 1000))  # Default to 1000 steps if not provided
    forward_motor2(steps)
    return f"Motor 2 Forward {steps} steps"  # Placeholder response

@app.route("/motor2_backward")
def motor2_backward():
    steps = int(request.args.get("steps", 1000))  # Default to 1000 steps if not provided
    backward_motor2(steps)
    return f"Motor 2 Backward {steps} steps"  # Placeholder response

@app.route("/motor3_forward")
def motor3_forward():
    steps = int(request.args.get("steps", 1000))  # Default to 1000 steps if not provided
    forward_motor3(steps)
    return f"Motor 3 Forward {steps} steps"  # Placeholder response

@app.route("/motor3_backward")
def motor3_backward():
    steps = int(request.args.get("steps", 1000))  # Default to 1000 steps if not provided
    backward_motor3(steps)
    return f"Motor 3 Backward {steps} steps"  # Placeholder response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)

