## Requirements

Docker 20.10+ and Docker Compose 1.29+ are required to run this benchmark.

## Installation

```sh
$ git clone git@github.com:ppgia-unifor/resiliency-pattern-benchmark.git
$ cd resiliency-pattern-benchmark
```

Now let's build the components.

```sh
$ docker-compose build
```

The command above will pull third-party images and build the images of the native components of the benchmark.


## Configuration

Choose one sample from samples folder and clone it.

```sh
$ cp ./samples/config-all-delay.json ./config-all-delay.json
```

Prepare the input file according the table XY 

Edit the section `volumes` in the service `scheduler` in the file `docker-compose.yaml` to mount the file created above.

```yaml
volumes:
  - ./config-all-delay.json:/opt/app/conf/conf.json
```



## Running in your environment


<!-- 



You now have the source files copied into your local directory, lets edit the input file.

Choose one sample in the sample folder and clone it


Next, we need to make sure we get all the required docker images, including the third-party images and the images of the benchmark.

```sh
docker-compose pull
```

 -->

<!-- - download repository

- edit configuration file

- show clients and 

- configurar aws  -->