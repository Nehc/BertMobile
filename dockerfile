FROM ubuntu:focal

ENV DEBIAN_FRONTEND noninteractive

LABEL maintainer="Nehcy <cibershaman@gmail.com>"
ARG NB_USER="wald"
ARG NB_UID="1000"
ARG NB_GID="100"

RUN apt-get update --yes && \
    apt-get upgrade --yes && \
    apt-get install --yes --no-install-recommends \
    git \
    python-is-python3 \
    python3-dev \
    build-essential \
    pip \
    nano \
    ffmpeg \
    libsm6 \
    libxext6 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip && \
    pip install torch==1.8.2+cu111 torchvision==0.9.2+cu111 torchaudio===0.8.2 \
    -f https://download.pytorch.org/whl/lts/1.8/torch_lts.html    

WORKDIR /home/telebot 

# Create NB_USER with name NB_USER user with UID=1000 and in the 'users' group
#chmod g+w /etc/passwd && \

RUN useradd -l -m -s /bin/bash -N -u "${NB_UID}" "${NB_USER}" # && \
    #chown "${NB_USER}:${NB_GID}" /home/telebot 
 
USER "${NB_UID}"

COPY requirements.txt ./

USER root 

RUN pip install -r requirements.txt && \
    python -m pip cache purge

#USER "${NB_UID}"

ARG TG_TOKEN=""
ARG MY_CHAT=""

ENV TG_TOKEN="${TG_TOKEN}" 
ENV MY_CHAT="${MY_CHAT}" 

# Configure container startup
ENTRYPOINT ["python", "./telebot.py"]