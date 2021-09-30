FROM ubuntu:latest

ENV DIRPATH /sw
WORKDIR $DIRPATH

RUN apt-get update && \
    DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata
RUN apt-get install -y git wget gcc pkg-config python3 python3-pip \
        graphviz graphviz-dev libpq-dev && \
    ln -s /usr/bin/python3 /usr/bin/python

RUN pip install git+https://github.com/indralab/indra_network_search.git@package && \
    pip install gunicorn && \
    git clone https://github.com/indralab/depmap_analysis.git && \
    export PYTHONPATH=$PYTHONPATH:depmap_analysis


ENTRYPOINT ["gunicorn", "-w", "1", "-b", ":8000", "-t", "600", "indra_network_search.api:app"]
