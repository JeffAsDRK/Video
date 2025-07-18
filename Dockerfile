FROM nvcr.io/nvidia/pytorch:24.04-py3

WORKDIR /app

RUN apt-get update && apt-get install -y \
    git \
    curl \
    && pip install --upgrade pip

    ### 
RUN pip install ultralytics
RUN pip install "opencv-python-headless==4.12.0.76"
RUN pip install numpy==1.24.4

# Verificaciones
#RUN python -c 
