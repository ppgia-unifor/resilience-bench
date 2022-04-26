# Resiliency Pattern Benchmark
A benchmark to evaluate resiliency patterns implemented in multiple programming languages.

# Documentation

[Architecture](#architecture)

[Getting started](#getting-started)

[Input file](#input-file)

[Output files](#output-file)

[Storage configuration](#storage-configuration)

[Publications](#publications)

## Architecture

![Architecture](docs/arch-2.jpeg)

**Scheduler** sets up the scenarios and initiates the processing by spawning threads to request configured clients. When threads end up, it aggregates the metrics and generates tests results.

**Client** implements an HTTP client wrapped by resilience patterns. It should reach a predefined number of successful requests, and measure its performance on this task.

**Target** implements the application to be the target of the tested client. This component is a joint of [Httpbin](http://httpbin.org), representing the target service and, [Envoy](https://www.envoyproxy.io) acting as a proxy service, enabling fault injection (e.g., server errors and response delays).


## Getting started

### Requirements

Docker 20.10+ and Docker Compose 1.29+ are required to run this benchmark.

### Installation

```sh
$ git clone git@github.com:ppgia-unifor/resiliency-pattern-benchmark.git
$ cd resiliency-pattern-benchmark
```

Now let's build the components.

```sh
$ docker-compose build
```

The command above will pull third-party images and build the images of the native components of the benchmark.


### Configuration

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



### Running in your environment


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

## Input file


## Output file

## Storage configuration

It supports two strategies to save the results dataset: remote and local. The remote strategy use Amazon S3. Open `docker-compose.yaml` file and find the definition of `scheduler` container, in the `environment`

#### Remote (Amazon S3) configuration

1. Configure the AWS credentials file on host machine by follow the steps available [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html).
2. Set the bucket name to `AWS_BUCKET_NAME` variable.
3. Set the path inside the bucket to `AWS_OUTPUT_PATH` variable.
4. Make sure the variable `DISK_PATH` do not exist.

#### Local configuration

1. Make sure `AWS_BUCKET_NAME` and `AWS_OUTPUT_PATH` do not exist;
2. Set `DISK_PATH` to a path inside the container;
3. Mount a volume binding `DISK_PATH` and a path in the host;

## Publications

**SBRC 2022**

The experimental dataset used in the SBRC 2022 submission is available in the folder [sbrc2022-data](sbrc2022-data/).

