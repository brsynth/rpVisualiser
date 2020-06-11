ARG IMAGE
FROM ${IMAGE}

RUN apt-get update \
 && apt-get install -y \
      libsbml5 \
      python3-pip \
      libxrender1 \
      libsm6 \
      libxext6

WORKDIR /home

COPY src src
