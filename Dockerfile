FROM ubuntu
RUN apt-get update && apt-get install -y git python python-pip
RUN git clone https://github.com/redsoxfantom/automation-utilities.git
RUN git clone https://github.com/redsoxfantom/python-lifx-sdk.git
ADD . /python_lifx_server
RUN cd python_lifx_server &&  pip install -r requirements.txt
EXPOSE 5000
ENV ZK_HOST 192.168.1.133
ENV ZK_PORT 2181
CMD ["/bin/ifconfig"]
CMD ["/usr/local/bin/gunicorn", "-b", "0.0.0.0:5000", "app:app"]
