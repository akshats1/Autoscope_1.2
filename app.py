from flask import Flask, render_template, Response
import time
import io
import threading
import PIL.Image
#from camera_update_new import Camera  # Import your Camera class
from camera_update_new_resolution import Camera
import atexit

app = Flask(__name__)
camera = Camera()

@app.route('/')
def index():
    return render_template('index.html')

def generate_frames():
    while True:
        frame = camera.get_frame()  # Get a frame from the camera
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.5)  # Adjust sleep time as needed

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture')
def capture():
    camera.capture_image()  # Capture an image
    return 'Image captured!'

@app.route('/stop_capture')
def stop_capture():
    camera.stop_capture()  # Stop image capture
    return 'Image capture stopped!'
def cleanup():
    camera.close()# After Picamera stop preview close the camera

if __name__ == "__main__":
    atexit.register(cleanup)# for releasing the resources of picamera
    app.run(debug=True,use_reloader=False)
