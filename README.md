# Resiliency Parterns Benchmark
A benchmark to evaluate resiliency patterns implemented in multiple programming languages.

## Architecture

![Architecture](docs/arch.png)

* **Scheduler** sets up the scenarios and initiates the processing by spawning threads to request previously configured clients. When threads end up, it aggregates the metrics and generate tests results.

* **Client** implements an http client wrapped by resilience patterns. It should reach a predefined number of succefully requests, and measures its own performance on this task.

* **Proxy** acts controlling the communication between the clients and the target service. It

* **Target** represents a ...

## Getting Started

This benchmark runs on top of a virtual machine managed by [Vagrant](https://www.vagrantup.com). 
