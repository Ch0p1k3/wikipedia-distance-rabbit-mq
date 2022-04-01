# Wikipedia distance. Rabbit MQ

This is RabbitMQ practice. Using python3.9.

## Install python3.9(Ubuntu/Debian)
```bash
make install_python3.9
```

## Requirements
For installing requirements:
```bash
make requirements
```

## Worker
To run RabbitMQ worker
```bash
RUN_ARGS="--host localhost --port 5672 --queue rabbitmqqueue" make worker
```

## Server
To run gRPC server
```bash
RUN_ARGS="--host 0.0.0.0 --port 50051 --rabbitmq_host localhost --rabbitmq_port 5672 --rabbitmq_queue rabbitmqqueue" make server
```

## Client
To run client
```bash
RUN_ARGS="--host 0.0.0.0 --port 50051" make client
```

## Docker image
To start the RabbitMQ, gRPC server and one worker you can use Docker image:
```bash
docker run --rm -it -p 15672:15672 -p 5672:5672 -p 50051:50051 ch0p1k/rabbit-mq:latest
```
To run in backend process - add `-d` flag

### Account for Rabbit MQ monitoring
Rabbit MQ monitoring: `http://localhost:15672/`
```
login: username
password: username
```
