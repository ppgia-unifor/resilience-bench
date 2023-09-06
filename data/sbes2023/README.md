# SBES 2023 Configuration File and Dataset

This data is related to the paper published in SBES 2023.

> Carlos M. Aderaldo and Nabor C. Mendonça. 2023. How The Retry Pattern Impacts Application Performance: A Controlled Experiment. In XXXVII Brazilian Symposium on Software Engineering (SBES 2023), September 25–29, 2023, Campo Grande, Brazil. ACM, New York, NY, USA, 10 pages. [https://doi.org/10.1145/3613372.3613409](https://doi.org/10.1145/3613372.3613409)
---

The Resilience Bench configurion file used to run the experiments described in the SBES 2023 paper is available as a [JSON file](https://github.com/ppgia-unifor/resilience-bench/tree/main/samples/config-retry.json) in the [samples folder](https://github.com/ppgia-unifor/resilience-bench/tree/main/samples/).

The experimental dataset produced after running these experiments is available at Zenodo in the [retry-polly-r4j-dataset.zip](https://zenodo.org/record/7938926/files/retry-polly-r4j-dataset.zip?download=1) file.

This zip file includes two csv files, named "results-polly.csv" and "results-r4j.csv", containing the experimental data obtained with the [Polly](https://github.com/App-vNext/Polly) and [Resilience4j](https://github.com/resilience4j/resilience4j) resilience libraries, respectively. Each csv file is structured with two sets of attributes (columns): the first set corresponds to the performance metrics collected during each test, while the second set corresponds to the test parameters.

### Performance Metrics
* `successfulCalls` number of successful invocations of the target service by the client application.
* `unsuccessfulCalls` number of unsuccessful invocations of the target service by the client application.
* `totalCalls` total number of invocations of the target service by the client application.
* `successfulRequests` number of successful invocations of the target service by the resilience library.
* `unsuccessfulRequests` number of unsuccessful invocations of the target service by the resilience library.
* `totalRequests` total number of invocations of the target service by the resilience library.
* `successTime` total (accumulated) time the resilience library spent waiting for a successful response from the target service.
* `successTimePerRequest` average response time of the target service measured by the resilience library.
* `errorTime` total (accumulated) time the resilience library spent waiting for an unsuccessful response from the target service.
* `errorTimePerRequest` average error time of the target service measured by the resilience library.
* `totalContentionTime` total time the client application spent waiting for either a successful or an unsuccessful response from the target service..
* `contentionRate` fraction of the client application's total execution time spent waiting for either a successful or an unsuccessful response from the target service.
* `totalExecutionTime` total execution time of the client application.
* `throughput` average number of successful requests handled by the target service per second.

### Test parameters
* `userId` ID of the client application's virtual user.
* `startTime` start time of the test.
* `endTime` end time of the test.
* `users` total number of client application's virtual users. 
* `round` test ID.
* `lib` resilience library used to invoke the target service.
* `pattern` resilience pattern used to invoke the target service.
* `faultPercentage` percentage of fauts injected into the target service's invocation stream.
* `faultType` type of faut injected into the target service's invocation stream.
* `faultStatus` faut status injected into the target service's invocation stream.
* `count` maximum number of retries allowed (including the first invocation attempt).
* `sleepDurationType` backoff delay increment type.
* `exponentialBackoffPow` float value to multiply the initial backoff delay before a new retry.
* `sleepDuration` initial backoff delay.
