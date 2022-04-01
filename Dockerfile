FROM rabbitmq:3.8-management

WORKDIR /rabbit_mq
COPY . .

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install -y make curl
RUN make install_python3.9
RUN make requirements

EXPOSE 15672 5672 50051

ENTRYPOINT [ "make", "run_rabbit_mq_worker_and_server" ]
