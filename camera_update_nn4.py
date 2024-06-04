import time
import logging
import io
import threading
import pathlib
from PIL import Image
import ffmpeg
from datetime import datetime
from io import BytesIO
try:
    from picamera import PiCamera
except ModuleNotFoundError:
    from backend.dummy_picam import PiCamera

class Camera:
    def __init__(self, save_dir):
        self.streaming = False
        self.capture_requested = False
        self.thread = None
        self.recording = False
        self.vid_fname = ''
        self.save_dir = pathlib.Path(save_dir)
        self.pic_res = (2000, 2000)
        self.stream_res = (320, 240)
        self.record_res = (1280, 720)
        self.frame_rate = 6
        self.cam = PiCamera()
        self.cam.resolution = self.stream_res
        self.cam.framerate = self.frame_rate

    def start_video_stream(self):
        if not self.streaming:
            self.streaming = True
            self.thread = threading.Thread(target=self._stream_video)
            self.thread.start()

    def stop_video_stream(self):
        self.streaming = False
        if self.thread is not None:
            self.thread.join()

    def capture_image(self):
        self.capture_requested = True
        #self.capture_requested = True
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
        
        #while self.streaming:
         #   stream = self.get_frame()
          #  img = Image.open(stream)
           # img_resized = img #.resize(self.stream_res, Image.ANTIALIAS)
           # stream_resized = BytesIO()
            #img_resized.save(stream_resized, format='jpeg')
            #stream_resized.seek(0)

            # Handle captured image request
            #if self.capture_requested:
             #   self._capture_image(stream)
              #  self.capture_requested = False

    def _capture_image(self, stream):
        stream.seek(0)  # Ensure the stream is at the beginning
        img = Image.open(stream)
        img.save(self.save_dir / f'captured_image_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.jpg')
        logging.info("Image captured!")

    def start_recording(self, filename: str) -> None:
        logging.info("[Camera] Starting video recording")
        self.recording = True
        self.vid_fname = (self.save_dir / filename).with_suffix(".h264")
        self.cam.resolution = self.record_res
        self.cam.framerate = 10
        self.cam.start_recording(str(self.vid_fname))

    def stop_recording(self) -> None:
        logging.info("[Camera] Finishing video recording")
        self.recording = False
        self.cam.stop_recording()
        self.cam.resolution = self.stream_res
        self.cam.framerate = self.frame_rate

        new_f = self.vid_fname.with_suffix(".mp4")
        logging.info("[Camera] Converting H264 video to MP4")
        ffmpeg.input(str(self.vid_fname)).output(str(new_f)).run(overwrite_output=True)
        self.vid_fname.unlink()

    def set_camera(self, resolution=None):
        if resolution is None:
            resolution = self.pic_res
        self.cam.resolution = resolution

    def close(self):
        logging.info("[Camera] Closing camera interface")
        if self.recording:
            self.stop_recording()
        if self.streaming:
            self.stop_video_stream()
        self.cam.close()

