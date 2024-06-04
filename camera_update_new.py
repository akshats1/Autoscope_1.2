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

class Camera:
    def __init__(self,save_dir):
        self.streaming = False
        self.capture_requested = False
        self.thread = None
        ## whether the camera is currently recording a video
        self.recording = False

        ## video output file name
        self.vid_fname = ''
        self.save_dir=pathlib.Path(save_dir)
        self.resolution=(4000,3000)
        #25 May 
        self.pic_res=(4000,3000)
        self.stream_res=(320,240)
        

        self.cam = PiCamera()  # Initialize PiCamera instance

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
    
    def start_recording(self, filename: str) -> None:
        """
        @brief Start recording video into the given location

        This function initializes recording a video and saves it
        with the given file name
        @param filename name of saved video file
        """
        logging.info("[Camera] Starting video recording")
        # switch the flag
        self.recording = True
        logging.info("{}".format((self.save_dir/filename).with_suffix(".h264")))
        self.vid_fname = (self.save_dir/filename).with_suffix(".h264")

        # start recording
      #  self.cam.resolution=self.resolution
        #25 May
        self.cam.resolution=self.stream_res
        self.cam.start_recording(str(self.vid_fname))

    def stop_recording(self) -> None:
        """
        @brief Stop recording video into the given location

        This function initializes recording a video and saves it
        with the given file name
        """
        logging.info("[Camera] Finishing video recording")
        # switch the flag
        self.recording = False

        # stop recording
        self.cam.stop_recording()

        # convert h264 to mp4
        new_f = self.vid_fname.with_suffix(".mp4")

        logging.info("[Camera] Converting H264 video to MP4")
        #convert=ffmpeg.FFmpeg()
        #convert.option('y').input(
         #                         self.vid_fname ).output(
        #                                            new_f ).convert.execute()
        ffmpeg.input(str(self.vid_fname)).output(str(new_f)).run(overwrite_output=True)
        

        # delete the h264 version
        self.vid_fname.unlink()
        
    
    def set_camera(self,resolution=(4000,3000)):
    #def set_camera(self,resolution=(self.pic_res)):
            #This function Update Camera Resolution
            self.resolution=resolution
            self.cam.resolution=resolution
    

    def close(self):
        # self.cam.close()  # Close the PiCamera instance
        
        """
        @brief Close camera

        This function closes the backend camera and stops streaming thread.
        """
        logging.info("[Camera] Closing camera interface")

        # stop any ongoing processes
        if self.recording:
            self.stop_recording()
        #if self.capturer:
         #   self.stop_thread()

        # Existing close method code..

