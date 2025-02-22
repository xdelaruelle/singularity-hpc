FROM ubuntu:20.04

# build a container with tcl modules for singularity-hpc
# docker build -f Dockerfile.tcl -t singularity-hpc .

LABEL MAINTAINER @vsoch
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt-get install -y build-essential \
    gcc \
    tcl-dev \
    autoconf \
    automake \
    python3 \
    python3-sphinx \
    python3-dev \
    python3-pip \
    curl \
    less

RUN curl -LJO https://github.com/cea-hpc/modules/releases/download/v4.7.0/modules-4.7.0.tar.gz && \
    tar xfz modules-4.7.0.tar.gz  && \
    cd modules-4.7.0 && \
    ./configure && \
    make && \
    make install
    
RUN pip3 install ipython
WORKDIR /code
COPY . /code
RUN pip3 install -e .[all]

# If we don't run shpc through bash entrypoint, module commands not found
ENTRYPOINT ["/code/entrypoint.sh"]
