from flask import Flask, jsonify, request, render_template
import logging
from movement import movexclock, movexanticlock, movey, movezclock, movezanticlock
from autofocus import auto, scan

app = Flask(__name__)

# Global variables to store the current positions
x_pos = 0
y_pos = 0
z_pos = 0

def update_positions(x=None, y=None, z=None):
    global x_pos, y_pos, z_pos
    if x is not None:
        x_pos += x
    if y is not None:
        y_pos += y
    if z is not None:
        z_pos += z

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calibrate', methods=['POST'])
def calibrate():
    magnification = request.args.get('magnification')
    if magnification == '4x':
        distance = 200  # Example distance for 4x calibration
    elif magnification == '10x':
        distance = 350  # Example distance for 10x calibration
    elif magnification == '40x':
        distance = 395  # Example distance for 40x calibration
    else:
        return jsonify({"error": "Invalid magnification"}), 400
    
    # Perform calibration logic here
    # For example, we can move the Z axis for calibration
    movezclock(distance)
    update_positions(z=-distance)

    return jsonify({"x": x_pos, "y": y_pos, "z": z_pos})

@app.route('/initialize', methods=['POST'])
def initialize():
    global x_pos, y_pos, z_pos

    # Move X axis to 0
    if x_pos > 0:
        movexanticlock(x_pos)
    elif x_pos < 0:
        movexclock(-x_pos)
    x_pos = 0

    # Move Y axis to 0
    if y_pos > 0:
        movey(-y_pos)
    y_pos = 0

    # Move Z axis to 0
    if z_pos > 0:
        movezanticlock(z_pos)
    elif z_pos < 0:
        movezclock(-z_pos)
    z_pos = 0

    return jsonify({"x": x_pos, "y": y_pos, "z": z_pos})

@app.route('/move', methods=['POST'])
def move():
    axis = request.args.get('axis')
    direction = request.args.get('direction')
    steps = int(request.args.get('steps', 0))

    if axis == 'x':
        if direction == 'clock':
            movexclock(steps)
            update_positions(x=steps)
        elif direction == 'anticlock':
            movexanticlock(steps)
            update_positions(x=-steps)
        else:
            return jsonify({"error": "Invalid direction"}), 400
    elif axis == 'y':
        if direction == 'clock':
            movey(steps)
            update_positions(y=steps)
        elif direction == 'anticlock':
            movey(-steps)
            update_positions(y=-steps)
        else:
            return jsonify({"error": "Invalid direction"}), 400
    else:
        return jsonify({"error": "Invalid axis"}), 400

    return jsonify({"x": x_pos, "y": y_pos, "z": z_pos})

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(host='0.0.0.0', port=5000)

