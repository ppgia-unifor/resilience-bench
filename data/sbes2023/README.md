# SBES 2023 Dataset
The experimental dataset used in the SBES 2023 paper is available in the [dataset.csv](dataset.csv) file.

This file is structured with the set of attributes (or csv columns) described below. The first six attributes correspond to test parameters, while the remaining attributes correspond to performance metrics collected during each test.

### Test parameters
* `pattern` resilience pattern used to invoke the target service (possible values are "Baseline", "Retry", and "CircuitBreaker").
* `succ_rate` the target service's success rate specified as a percentage of the total number of invocations the target service receives (possible values are 50%, 75%, and 100%).
* `timeout` timeout parameter used to configure the Retry and Circui Breaker patterns (possible values are 0ms, 50ms, 75ms, 100ms and 200ms).
* `framework` language/resilience library used to implemente the client application (possible values are "Java", which uses the [Resilience4j](https://github.com/resilience4j/resilience4j) library, and "DotNet", which uses the [Polly](https://github.com/App-vNext/Polly) library). 
* `test` unique identifier for each resilience test.
* `clients` number of clients concurrently invoking the target service in each test (possible values are 1, 25, 50, and 100).
### Metrics
* `ClientTotalTime` total execution time of the client application.
* `ClientAverageTimePerRequest` average response time of the target service measured by the client application.
* `ClientSuccess` number of successful invocations of the target service by the client application.
* `ClientError` number of unsuccessful invocations of the target service by the client application.
* `ClientTotal` total number of invocations of the target service by the client application.
* `ResilienceModuleTotalSuccessTime` total (accumulated) time the resilience module spent waiting for a successful response from the target service. 
* `ResilienceModuleTotalErrorTime` total (accumulated) time the resilience module spent waiting for an unsuccessful response from the target service.
* `ResilienceModuleAverageSuccessTimePerRequest` average response time of the target service measured by the resilience module.
* `ResilienceModuleSuccess` number of successful invocations of the target service by the resilience module.
* `ResilienceModuleError` number of unsuccessful invocations of the target service by the resilience module.
* `ResilienceModuleTotal` total number of invocations of the target service by the resilience module.
* `ResilienceModuleTotalTime` total execution time of the resilience module.
* `ContentionRate` fraction of the client application's total execution time spent waiting for either a successful or an unsuccessful response from the target service.
