import cv2
from collections import deque
import threading
import time
import platform

class VideoBuffer:
    def __init__(self, rtsp_url, fps=20, delay_sec=2):
        self.rtsp_url = rtsp_url
        self.fps = fps
        self.delay_sec = delay_sec
        self.buffer_size = int(fps * delay_sec)
        self.buffer = deque(maxlen=self.buffer_size)
        self.capture = None
        self.thread = None
        self.running = False

        self.is_arm = platform.machine().startswith('arm') or platform.machine().startswith('aarch64')

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def _open_capture(self):
        if self.is_arm:
            print("Abriendo stream sin backend explícito (ARM detected)")
            cap = cv2.VideoCapture(self.rtsp_url)
        else:
            print("Abriendo stream con backend FFmpeg (x86 detected)")
            cap = cv2.VideoCapture(self.rtsp_url, cv2.CAP_FFMPEG)
        return cap

    def _run(self):
        while self.running:
            if self.capture is None or not self.capture.isOpened():
                print("Intentando abrir stream RTSP...")
                self.capture = self._open_capture()
                time.sleep(1)

            ret, frame = self.capture.read()
            if not ret or frame is None:
                print("Error al leer frame, reconectando...")
                if self.capture:
                    self.capture.release()
                self.capture = None
                time.sleep(2)
                continue

            ret2, jpeg = cv2.imencode('.jpg', frame)
            if ret2:
                self.buffer.append(jpeg.tobytes())

            time.sleep(1/self.fps)

    def get_frame(self):
        if len(self.buffer) == 0:
            return None
        # Regresa el frame más viejo, creando un retraso (buffer de 2 segundos)
        return self.buffer[0]

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        if self.capture:
            self.capture.release()
