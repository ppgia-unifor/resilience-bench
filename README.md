# Resiliency Parterns Benchmark
A benchmark to evaluate resiliency patterns implemented in multiple programming languages.

## Architecture

![Architecture](docs/arch.png)

* **Scheduler** sets up the scenarios and initiates the processing by spawning threads to request configured clients. When threads end up, it aggregates the metrics and generates tests results.

* **Client** implements an HTTP client wrapped by resilience patterns. It should reach a predefined number of successful requests, and measure its performance on this task.

* **Proxy** acts controlling the communication between the clients and the target service. It

* **Target** represents a ...

## Getting Started

This benchmark runs on top of a virtual machine managed by [Vagrant](https://www.vagrantup.com). 


1. Download and install [Vagrant](https://www.vagrantup.com/docs/installation).

2. Sets up the virtual machine by running `vagrant up` in the root folder.

3. The tests will start as soon as the virtual machine ends up its provision. To configure a custom test, see the next section.

## Setting up a custom test

- describe json properties
- describe each component
- describe docker-compose file

## Adding a new programming language

A client should follow a very simple contract to be integrated into this benchmark. 

**Requirements**
- should offer a baseline version of it, that is a version of the operation with no pattern wrapping it;

- should calculate its own metrics;

- should accept timeout configuration via env variable;

- should accept host and resource via env variable;

- should be containerized using Docker

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

