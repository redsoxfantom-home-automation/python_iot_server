FROM ubuntu
RUN apt-get update && apt-get install -y python python-pip
ADD . /python_lifx_server
RUN cd python_lifx_server &&  pip install -r requirements.txt
EXPOSE 5000
ENV ZK_HOST localhost
ENV ZK_PORT 2181
CMD ["/usr/local/bin/gunicorn", "-b", "0.0.0.0:5000", "app:app"]
