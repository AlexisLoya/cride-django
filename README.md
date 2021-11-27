# CRide


[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

## Let's start
### Installation

CRide requires [Python](https://www.python.org/downloads/) 3+ to run.

Install the docker file

```sh
$ sudo docker-compose -f local.yml build
```
#### basic commands 

```sh
$ sudo docker-compose -f local.yml up
$ sudo docker-compose -f local.yml down
$ sudo docker-compose -f local.yml ps
```
#### Pro tip 
Export a temporal variable to manage the docker-compose  ```$ export COMPOSE_FILE=local.yml```
```sh
$ sudo docker-compose build
$ sudo docker-compose up
$ sudo docker-compose down
$ sudo docker-compose ps
```
#### Command Admministrator 
The flag  ```--rm``` will kill the container after to finish the command, very useful
```sh
$ sudo docker-compose run --rm django COMMAND
$ sudo docker-compose run --rm django python manage.py createsuperuser
```
#### Enable Debugger
1. ```$ docker-compose up```  to start the containers
2. ```$ docker-compose ps``` to identify the container with django
3. ```$ docker-compose rm -f <ID>``` to kill that container 
4.  Run in another terminal the command below. The flag ```--service-ports``` is to expose the ports and the communicates with the others containers do not be affected
```sh
$ sudo docker-compose run --rm --service-ports django
```
#### Remember!
```sh
$ docker container
$ docker images
$ docker volume
docker network
```
Those commands have the common options 
* **ls** - *list* 
* **rm** - *remove* 
* **prune** - *quit*
* **-a**- *show all*
* **-q**- *show ID*
# Environment
#### config
```
.config
│   README.md
└─── settings
│   └─── base.py
│   └─── local.py
│   └─── production.py
│   └─── test.py
└─── urls.py
└─── wsgi.py
```
#### Requirement
```
.Requirement
└─── base.txt
└─── local.txt
└─── production.txt
```
#### Docker
```
./
└─── compose
│   └─── local
│   │      └─── ...
│   └─── production
│   │      └─── ...
└─── local.yml
└─── ...
└─── production.yml
└─── ...
```
#### Apps
```
./
└─── adkan
│   └─── local
│   └─── __init__.py
│   └─── taskapp
│   └─── celery.py
```

## Services

Dillinger is currently extended with the following plugins.
Instructions on how to use them in your own application are linked below.

| Port | Name | README | 
| ------ | ------ | ------ |
| 8000 | Django | [Docs](https://docs.djangoproject.com/en/3.2/) |
| 5432 | PostgreSQL |  [Docs](https://www.postgresql.org/docs/)|
| 6379 | Reddis |  [Docs](https://redis.io/documentation) |
| 55555 | Celery |  [Docs](https://flower.readthedocs.io/en/latest/) |

**Free Software, Hell Yeah!**
## Authors ✒️
* **Alexis Loya** - *Developer* - [Alexis Loya](https://github.com/AlexisLoya)
