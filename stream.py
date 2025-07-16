 # stream_buffer.py
import cv2
import threading
import time
from collections import deque
from ultralytics import YOLO

class VideoBuffer:
    def __init__(self, source=0, fps=20, delay_sec=2):
        self.cap = cv2.VideoCapture(source)
        self.fps = fps
        self.delay_frames = int(fps * delay_sec)
        self.buffer = deque(maxlen=self.delay_frames)
        self.lock = threading.Lock()
        self.running = False
        self.model = YOLO("yolo11n.pt")

    def start(self):
        self.running = True
        t = threading.Thread(target=self.update, daemon=True)
        t.start()

    def update(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                with self.lock:
                    results=self.model.predict(frame, verbose=False,device='cuda')
                    frame = results[0].plot()
                    self.buffer.append(frame)
            time.sleep(1 / self.fps)

    def get_frame(self):
        with self.lock:
            if self.buffer:
                frame = self.buffer[0]  # Frame más antiguo (2s retraso)
                _, jpeg = cv2.imencode('.jpg', frame)
                return jpeg.tobytes()
            return None

    def stop(self):
        self.running = False
        self.cap.release()
