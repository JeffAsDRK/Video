import ffmpeg
import numpy as np
import cv2
import subprocess

# Configura el comando ffmpeg
stream_url = "rtsp://admin:asd12345@192.168.0.249/Streaming/Channels/301/"

process = (
    ffmpeg
    .input(stream_url)
    .output('pipe:', format='rawvideo', pix_fmt='bgr24')
    .run_async(pipe_stdout=True, pipe_stderr=True)
)

width, height = 1920, 1080  # Ajusta al tamaño de tu cámara

while True:
    in_bytes = process.stdout.read(width * height * 3)
    if not in_bytes:
        print("No se pudieron leer más bytes del stream.")
        break

    frame = np.frombuffer(in_bytes, np.uint8).reshape([height, width, 3])
    cv2.imshow('RTSP stream via ffmpeg', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

process.stdout.close()
process.wait()
cv2.destroyAllWindows()
