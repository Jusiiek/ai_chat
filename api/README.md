# 🧠 API

### INFO
#### To set up the API, create a virtual python environment, version 3.12 or later. Also the app requires to use docker compose to run the database

-------

### Run database
```
$ docker-compose run -d
```
-----
### Installation

#### To install requirements use makefile command
```
$ make dev_install
```

#### or with python command:

```
$ pip install -e .
```
------
### Run project

#### Once everything is installed, all you need to do is initiate the creation of the database table with below command:
```
$ make init_db
```

#### then, in two separate terminal windows run api and worker

##### api
```
$ make dev_run
```

##### worker
```
$ make dev_run_worker
```
