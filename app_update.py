from flask import Flask, render_template, Response,jsonify,request
import time
import io
import threading
import PIL.Image
#from camera_update_new import Camera 
#from camera_update_nn import Camera 
#from camera_update_new import Camera 
#from camera_update_new_resolution import Camera # Import your Camera class
#from camera_update_nn4 import Camera
from camera_update_nn5 import Camera
import atexit
from datetime import datetime
from motor_move import Motor
import serial
from movement import movexclock, movexanticlock, movey, moveycc,movezclock, movezanticlock
from autofocus import auto, scan
from flask import Flask, render_template, send_from_directory
from gallery import Gallery
import os
import boto3
import os
from werkzeug.utils import secure_filename
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from gallery import Gallery  # Ensure you have this class in a file named gallery.py
import shutil




#app = Flask("Flask Image Gallery")
gallery = Gallery()

mtr=Motor()
try:
    arduino = serial.Serial('/dev/ttyUSB1', 9600)
except Exception as e:
    print(f"Error opening serial port: {e}")


app = Flask(__name__)
# adding save directory
save_dir="/home/pi/Pictures/Saved_videos/"
camera = Camera(save_dir=save_dir)
'''
*****************Motor Control Routes Start************ 
'''

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


############ Motor Control Routes END  ############


########### x y z coordinates Display Start########
 
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
            moveycc(steps)
            update_positions(y=-steps)
        else:
            return jsonify({"error": "Invalid direction"}), 400
    elif axis == 'z':
        if direction == 'clock':
            movezclock(steps)
            update_positions(z=steps)
        elif direction == 'anticlock':
            movezanticlock(steps)
            update_positions(z=-steps)
        else:
            return jsonify({"error": "Invalid direction"}), 400
            
    else:
        return jsonify({"error": "Invalid axis"}), 400

    return jsonify({"x": x_pos, "y": y_pos, "z": z_pos})

 
 
 
########### x y z coordinates Display End##########






@app.route('/')
# 16 May 
def start_page():
    #return render_template('index.html')
    #return render_template('index.html')
    return render_template('start.html')
@app.route('/index')
def index_page():
    return render_template('index.html')
@app.route('/start')
def start_page_alias():
    return render_template('start.html')
    
    
#gallery file with aws need to integrate over here

#################     AWS S3 Configuration##############


#app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# AWS S3 Configuration
S3_BUCKET = 'images-demo1'

def get_s3_client():
    return boto3.client('s3')

def multipart_upload(file_path, bucket, key):
    s3 = get_s3_client()
    try:
        transfer = boto3.s3.transfer.S3Transfer(s3)
        transfer.upload_file(file_path, bucket, key)
    except boto3.exceptions.S3UploadFailedError as e:
        return str(e)





@app.route('/gallery',methods=['GET', 'POST'])
def gallery_page():
    gallery = Gallery()
    image_paths = gallery.get_image_paths()
    
    if request.method == 'POST':
        files = request.form.getlist('files')
        if not files:
            return jsonify({'error': 'No files selected'}), 400

        results = []
        for encoded_path in files:
            filepath = Gallery.decode(encoded_path)
            filename = secure_filename(os.path.basename(filepath))
            
            # Upload to S3 using multipart upload
            upload_result = multipart_upload(filepath, S3_BUCKET, filename)

            if upload_result is None:
                results.append(f'File {filename} uploaded successfully to S3!')
            else:
                results.append(f'Failed to upload file {filename}: {upload_result}')
        
        return jsonify(results)

    # Handle GET request
    return render_template('gallery.html', paths=image_paths)
    
    
    
@app.route('/cdn/<path:filepath>')
def download_file(filepath):
    dir, filename = os.path.split(Gallery.decode(filepath))
    return send_from_directory(dir, filename, as_attachment=False)


def generate_frames():
    while True:
        frame = camera.get_frame()  # Get a frame from the camera
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.5)  # Adjust sleep time as needed

@app.route('/video_record')
def video_record():
    filename=datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+'.mp4'
    # for recording the live video
    camera.start_recording(filename)
    return 'video recording started'

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture')
def capture():
    camera.capture_image()  # Capture an image
    #return 'Image captured!'
    return 'Image Captured'

@app.route('/stop_record')
def stop_capture():
    camera.stop_recording()  # Stop video recording
    return 'Video recording stopped!'
def cleanup():
    camera.close()# After Picamera stop preview close the camera


###########Copy  Files to pendrive############
import os
import time

folder_to_look = '/media/pi/'
disks_avaliable = os.listdir(folder_to_look)
print(disks_avaliable)
ans=''.join(str(x) for x in disks_avaliable)
print(ans)
ans_new=folder_to_look+'/'+ans
print(ans_new)


MOUNT_POINT = ans_new
DEVICE_PATH = "/dev/sda1"  # Change this to the correct device path




def create_mount_point():
    if not os.path.exists(MOUNT_POINT):
        os.makedirs(MOUNT_POINT)

def set_permissions(path):
    os.system(f'sudo chown -R pi:pi {path}')
    os.system(f'sudo chmod -R 777 {path}')


@app.route('/mount_pendrive', methods=['POST'])
def mount_pendrive():
    create_mount_point()
    
    command = f'sudo mount -o uid={os.getuid()},gid={os.getgid()} {DEVICE_PATH} {MOUNT_POINT}'
    result = os.system(command)
    
    if result == 0:
        set_permissions(MOUNT_POINT)
        message = "Pendrive mounted successfully."
    else:
        message = "Failed to mount pendrive."

    return jsonify({"message": message})

@app.route('/copy_to_pendrive', methods=['POST'])
def copy_to_pendrive():
    files = request.json.get('files', [])
    if not files:
        return jsonify({'error': 'No files selected'})

    results = []
    for encoded_path in files:
        filepath = Gallery.decode(encoded_path)
        filename = secure_filename(os.path.basename(filepath))
        destination_path = os.path.join(MOUNT_POINT, filename)
        try:
            shutil.copyfile(filepath, destination_path)
            set_permissions(destination_path)
            results.append(f'File {filename} copied successfully to pendrive!')
        except Exception as e:
            results.append(f'Failed to copy file {filename} to pendrive: {str(e)}')

    return jsonify({"message":results}) 

###############Copy Pendrive Ends#################

##############Delete Selected Files Start#########
@app.route('/delete', methods=['POST'])
def delete_files():
    files = request.form.getlist('files')
    if not files:
        return jsonify({'error': 'No files selected'}), 400

    results = []
    for encoded_path in files:
        filepath = Gallery.decode(encoded_path)
        try:
            os.remove(filepath)
            results.append(f'File {filepath} deleted successfully!')
        except Exception as e:
            results.append(f'Failed to delete file {filepath}: {str(e)}')

    return jsonify(results)

################Delete Selected Files Ends####################




if __name__ == "__main__":
    atexit.register(cleanup)# for releasing the resources of picamera
    app.run(debug=True,use_reloader=False)

