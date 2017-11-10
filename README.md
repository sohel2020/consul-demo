# Docker Service Discovery with the help of consul

## Prerequisite
- docker-engine >= 1.12
- docker-compose >= 1.11.2
- docker-py >= 2.1.0

## Deployment Steps
```bash
$ git clone https://github.com/sohel2020/consul-demo.git
$ cd consul-demo
$ docker-compose build --no-cache
$ docker-compose up -d
```

## Show all application logs

```bash
$ docker-compose logs -f
```

## Open Your favorite browser and hit `http://127.0.0.1:8080`


## Author
- [Tarikur Rahaman](https://github.com/sohel2020)