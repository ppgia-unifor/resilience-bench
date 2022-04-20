# SBRC 2022 Submission Dataset
The experimental dataset used in the SBRC 2022 submission is available in the folder [sbrc2022-data](sbrc2022-data/).

# Resiliency Pattern Benchmark
A benchmark to evaluate resiliency patterns implemented in multiple programming languages.

## Architecture

![Architecture](docs/arch-2.jpeg)

* **Scheduler** sets up the scenarios and initiates the processing by spawning threads to request configured clients. When threads end up, it aggregates the metrics and generates tests results.

* **Client** implements an HTTP client wrapped by resilience patterns. It should reach a predefined number of successful requests, and measure its performance on this task.

* **Target** implements the application to be the target of the tested client. This component is a joint of [Httpbin](http://httpbin.org), representing the target service and, [Envoy](https://www.envoyproxy.io) acting as a proxy service, enabling fault injection (e.g., server errors and response delays).

<!-- ## Getting Started -->

## Requirements

The benchmark is a set of containers orchestrated by a Docker Compose description file. 

- Docker
- Docker Compose

## Setting up a test

A test scenario consists of a set parameters specified as a JSON file passed to the scheduler application to start a testing session.

The code below represents the schema of an input file and the following tables contains the description of each property.

```json
{
    "testId": "string",
    "concurrentUsers": "array",
    "rounds": "number",
    "maxRequestsAllowed": "number",
    "targetSuccessfulRequests": "number",
    "fault": {
        "type": "abort|delay",
        "percentage": "array",
        "status": "number",
        "duration": "number"
    },
    "patterns": [
        {
            "pattern": "string",
            "platform": "string",
            "lib": "string",
            "url": "string",
            "configTemplate": { }
        }
    ]
}
```

#### Control parameters

Set of parameters to control the general features of each test.

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `testId` | `string` | no | Identifier of test. If not set, a timespam will be generated. |
| `concurrentUsers` | `number` |  yes | Number of concurrent virtual users to invoke the HTTP server during each test. |
| `rounds` | `number` | yes | Number of test executions per scenario. |
| `targetSuccessfulRequests` | `number` | yes | Minimum number of successful invocations from the client to the server application. |
| `maxRequestsAllowed` | `number` | yes | Maximum number of invocations the client application is allowed to perform overall. |

The latter parameter is useful to prevent the client application from never reaching the required number of successful invocations in a reasonable window of time, which may happen under high server failure rates.


#### Fault injection

Rate with which the proxy server will inject failures into the request stream the target service receives from the client application.

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `type` | `string` | yes | Type of fault. Accepted values: delay or fault. |
| `percentage` | `array` | yes | Rate which the proxy server will inject failures into the request stream. |
| `duration` | `number` | no | Time in miliseconds the server will delay. Required when type is delay. |
| `status` | `number` | no | HTTP status code the server will return. Required when type is abort. |


#### Pattern

Resilience strategy the client application will use to invoke the target service. It's an array where is possible to define several clients and their patterns. Each pattern (e.g: retry, circuit breaker and baseline) is an object of this array. To group them in the result dataset, use `lib` and `platform` properties. 

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `pattern` | `string` | yes | The name of pattern. |
| `platform` | `string` | yes | The name of plataform. |
| `lib` | `string` | yes | The name of library. |
| `url` | `string` | yes | The url that process the tasks wrapped in pattern |
| `configTemplate` | `object` | yes | The library's pattern configuration. It's a dynamic object and the value will be processed and passed to the `url`. |


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

## Environment configuration

... docker-compose ...

... vagrantfile ...


## Running tests

1. Download and install [Vagrant](https://www.vagrantup.com/docs/installation).

2. Sets up the virtual machine by running `vagrant up` in the root folder.

3. The tests will start as soon as the virtual machine ends up its provision. To configure a custom test, see the next section.

## Test results

...


## Adding a new programming language

A client should follow a very simple contract to be integrated into this benchmark. 

<!-- **Requirements**

types: technical / conceptual

- (conceptual) should offer a baseline version of it, that is a version of the operation with no pattern wrapping it;

- (conceptual) should calculate its own metrics;

- should accept timeout configuration via env variable;

- should accept host and resource via env variable;

- (technical) should be containerized using Docker. The container should be multi-stage in order to build itself without the need to install dependencies in host machine. (https://docs.docker.com/develop/develop-images/multistage-build/)[Click here] to learn about multi-stage build.

- The request body should accept this payload. 
```json
{
    "maxRequestsAllowed": 1,
    "targetSuccessfulRequests": 1,
    "params": {}
}
```

- The response boby should follow this format:

```json
{

}
```
 -->
