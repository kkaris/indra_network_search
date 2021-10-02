FROM ubuntu:latest

ENV DIRPATH /sw
WORKDIR $DIRPATH
ENV NETWORK_CACHE /sw/indra_network_search/indra_network_search/_cache

RUN apt-get update && \
    DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata && \
    apt-get install -y git wget gcc pkg-config python3 python3-pip \
        graphviz graphviz-dev libpq-dev && \
    ln -s /usr/bin/python3 /usr/bin/python

RUN git clone -b package https://github.com/indralab/indra_network_search.git && \
    cd indra_network_search && \
    pip install -e . && \
    cd .. && \
    mkdir -p $NETWORK_CACHE && \
    pip install gunicorn uvicorn termcolor cachetools && \
    git clone https://github.com/indralab/depmap_analysis.git && \
    python -m indra.ontology.bio build

ADD indranet_dir_graph.pkl $NETWORK_CACHE
ADD indranet_sign_edge_graph.pkl $NETWORK_CACHE
ADD indranet_sign_node_graph.pkl $NETWORK_CACHE

ENV PYTHONPATH /sw/depmap_analysis
ENV USE_CACHE 1

ENTRYPOINT ["gunicorn", "-w", "1", "-b", "0.0.0.0:8000", "-t", "600", "-k", "uvicorn.workers.UvicornWorker", "indra_network_search.rest_api:app"]
