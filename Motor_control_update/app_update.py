import serial
from flask import Flask, render_template, request
from motor_move import Motor
mtr=Motor()
# Initialize the serial connection to the Arduino
try:
    arduino = serial.Serial('/dev/ttyUSB1', 9600)
except Exception as e:
    print(f"Error opening serial port: {e}")



app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/motor1_forward")
def motor1_forward():
    steps = int(request.args.get("steps", 1000))
    mtr.forward_motor1(steps)
    return f"Motor 1 Forward {steps} steps"

@app.route("/motor1_backward")
def motor1_backward():
    steps = int(request.args.get("steps", 1000))
    mtr.backward_motor1(steps)
    return f"Motor 1 Backward {steps} steps"

@app.route("/motor2_forward")
def motor2_forward():
    steps = int(request.args.get("steps", 1000))
    mtr.forward_motor2(steps)
    return f"Motor 2 Forward {steps} steps"

@app.route("/motor2_backward")
def motor2_backward():
    steps = int(request.args.get("steps", 1000))
    mtr.backward_motor2(steps)
    return f"Motor 2 Backward {steps} steps"

@app.route("/motor3_forward")
def motor3_forward():
    steps = int(request.args.get("steps", 1000))
    mtr.forward_motor3(steps)
    return f"Motor 3 Forward {steps} steps"

@app.route("/motor3_backward")
def motor3_backward():
    steps = int(request.args.get("steps", 1000))
    mtr.backward_motor3(steps)
    return f"Motor 3 Backward {steps} steps"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,threaded=True)

