import time
import logging
import io
import threading
import pathlib
import PIL.Image
import ffmpeg
import typing
import nptyping
import sys
from datetime import datetime
from io import BytesIO
#from cStringIO import StringIO
try:
    from picamera import PiCamera
except ModuleNotFoundError:
    from backend.dummy_picam import PiCamera
# 13 May adding Resolution to highest 

class Camera:
    def __init__(self,resolution=(640,480)):
        self.streaming = False
        self.capture_requested = False
        self.thread = None
        self.resolution=resolution
        self.cam = PiCamera(resolution=self.resolution)  # Initialize PiCamera instance

    def start_video_stream(self):
        if not self.streaming:
            self.streaming = True
            self.thread = threading.Thread(target=self._stream_video)
            self.thread.start()

    def stop_video_stream(self):
        self.streaming = False

    def capture_image(self):
        self.capture_requested = True
        stream = io.BytesIO()
        self.cam.capture(stream, format='jpeg', use_video_port=True)
        stream.seek(0)

            # Check if image capture is requested
        if self.capture_requested:
            self._capture_image(stream)
            self.capture_requested = False
        
    def get_frame(self):
        stream = io.BytesIO()
        self.cam.capture(stream, format='jpeg', use_video_port=True)
        stream.seek(0)
        return(stream.read())
        

    def _stream_video(self):
        while self.streaming:
            # Capture video frame and stream it
            frame=self.get_frame()
            

            # Check if image capture is requested
            if self.capture_requested:
                #self._capture_image(stream)
                self._capture_image(frame)
                self.capture_requested = False

            # Here, you can handle streaming the frame to your desired output

    def _capture_image(self, stream):
        # Save the captured frame as an image
        img = PIL.Image.open(stream)
        #img.save('captured_image.jpg'+'%datetime.now().strftime('%Y-%m-%d')) ## adding timestamp to image
        #img.save('captured_image_' + datetime.now().strftime('%Y-%m-%d') + '.jpg')
        img.save('captured_image_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.jpg')


        logging.info("Image captured!")

    def close(self):
        self.cam.close()  # Close the PiCamera instance
