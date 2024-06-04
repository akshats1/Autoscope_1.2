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
        self.pic_res = (4056, 3040)
        self.stream_res = (320, 240)
        self.record_res = (1920, 1080)
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
        stream = io.BytesIO()
        
        # Temporarily change resolution for capturing high-resolution image
        self.cam.resolution = self.pic_res
        self.cam.capture(stream, format='jpeg', use_video_port=False)
        self.cam.resolution = self.stream_res
        
        stream.seek(0)
        
        if self.capture_requested:
            self._capture_image(stream)
            self.capture_requested = False

    def get_frame(self):
        stream = io.BytesIO()
        self.cam.capture(stream, format='jpeg', use_video_port=True)
        stream.seek(0)
        return stream.read()

    def _stream_video(self):
        while self.streaming:
            frame = self.get_frame()
            if self.capture_requested:
                self._capture_image(io.BytesIO(frame))
                self.capture_requested = False

    def _capture_image(self, stream):
        stream.seek(0)  # Ensure the stream is at the beginning
        img = Image.open(stream)
        img.save(self.save_dir / f'captured_image_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.jpg','JPEG',quality=100)
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
        # 30 May Not converting .H264 to mp4
         
        new_f = self.vid_fname.with_suffix(".mp4")
        logging.info("[Camera] Converting H264 video to MP4")
        ffmpeg.input(str(self.vid_fname)).output(str(new_f)).run(overwrite_output=True)
        #ffmpeg.input(str(self.vid_fname)).run(overwrite_output=True)
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

