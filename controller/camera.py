import cv2
import threading
import time


class VideoCamera(threading.Thread):

    def __init__(self, index):
        super().__init__()
        self._stop_event = threading.Event()
        self.video = cv2.VideoCapture(index)
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 250)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 200)
        (self.grabbed, self.frame) = self.video.read()

    def stop(self):
        self._stop_event.set()
        self.video.release()

    def get_frame(self):
        time.sleep(150)
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def run(self):
        while not self._stop_event.is_set():
            (self.grabbed, self.frame) = self.video.read()


def gen(cam):
    while not cam._stop_event.is_set():
        try:
            success, frame = cam.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            cam.stop()
