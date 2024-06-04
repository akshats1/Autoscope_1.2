import os
import base64

class Gallery:
    IMAGE_EXTS = [".png", ".jpg", ".jpeg", ".gif", ".tiff"]
    ROOT_DIR = '/home/pi/Pictures/Saved_videos'  # Hardcoded root directory

    @staticmethod
    def encode(path):
        return base64.urlsafe_b64encode(path.encode('utf-8')).decode()

    @staticmethod
    def decode(encoded_path):
        return base64.urlsafe_b64decode(encoded_path.encode('utf-8')).decode()

    def get_image_paths(self):
        image_paths = []
        for root, dirs, files in os.walk(self.ROOT_DIR):
            for file in files:
                if any(file.endswith(ext) for ext in self.IMAGE_EXTS):
                    image_paths.append(self.encode(os.path.join(root, file)))
        return image_paths

