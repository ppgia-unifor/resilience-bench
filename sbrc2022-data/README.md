# SBRC 2022 Dataset
The experimental dataset used in the SBRC 2022 submission is available in the [dataset.csv](dataset.csv) file.

This file is structured with the following set of attributes (or csv columns), with the first six attributes corresponding to test parameters, and the remaining attributes corresponding to performance metrics collected during each test.

### Test parameters
* `pattern` resilience pattern used to invoke the target service (possible values are "Baseline", "Retry", and "CircuitBreaker").
* `succ_rate` the target service's success rate (possible values are 0.0, 0.25, and 0.50).
* `timeout` timeout parameter used to configure the Retry and Circui Breaker patterns (possible values are 0ms, 50ms, 75ms, 100ms and 200ms).
* `framework` resilience framework/language used (possible values are "Java", with the Resilience4j library, and "DotNet", with the Polly library). 
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
