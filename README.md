# Resiliency Pattern Benchmark
A benchmark to evaluate resiliency patterns implemented in multiple programming languages.

# Documentation

[Getting started](./docs/getting-started.md)

[Architecture](#architecture)

[Input and output files](./docs/input-output-files.md)

[Storage configuration](./docs/storage.md)

[Publications](#publications)

# Architecture

![Architecture](docs/arch-2.jpeg)

**Scheduler** sets up the scenarios and initiates the processing by spawning threads to request configured clients. When threads end up, it aggregates the metrics and generates tests results.

**Client** implements an HTTP client wrapped by resilience patterns. It should reach a predefined number of successful requests, and measure its performance on this task.

**Target** implements the application to be the target of the tested client. This component is a joint of [Httpbin](http://httpbin.org), representing the target service and, [Envoy](https://www.envoyproxy.io) acting as a proxy service, enabling fault injection (e.g., server errors and response delays).

## Publications

**SBRC 2022**

The experimental dataset used in the SBRC 2022 submission is available in the folder [sbrc2022-data](sbrc2022-data/).

