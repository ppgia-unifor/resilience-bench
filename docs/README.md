## ResilienceBench Architecture

The ResilienceBench architecture contains four main components: a **scheduler**, a **client service**, a **proxy service**, and a **target service**, which interact at run time as depicted in the figure below. 

<br/><br/>
<img src="resiliencebench-arch-trans-color.png" width=900>
<br/><br/>

The scheduler (i) parses and executes the set of resilience test scenarios specified by the ResilienceBench user in a [JSON input file](#scenarios-input-file); (ii) invokes the client service with the test parameters for each scenario; and (iii) collects the test results received from the client service and returns them to the user in a [CSV output file](#results-output-file).  

The client service (i) invokes the target service using a given resilience pattern (e.g., Retry), as specified in the test scenario being executed; (ii) collects and calculates a set of performance and resilience metrics (e.g., mean response timefrom the result of each target service invocation; and (iii) returns the collected performance metrics to the scheduler.

The proxy service transparently injects a given type of failure (e.g., abort or delay failures) into the target service invocation flow, according to a given failure rate.

Finally, the target service simply processess and responds to the client service's requests.

## Test scenarios (input file)

ResilienceBench test scenarios consist of a set of test parameters specified as a JSON file. The JSON code below shows an example of a test scenario:

```json
{
    "testId": "MyTest",
    "concurrentUsers": [25],
    "rounds": 10,
    "maxRequestsAllowed": 100,
    "targetSuccessfulRequests": 25,
    "fault": {
        "type": "abort",
        "percentage": [50],
        "status": 503
    },
    "patterns": [
        {
            "pattern": "retry",
            "platform": "java",
            "lib": "resilience4j",
            "url": "http://resilience4j/retry",
            "patternConfig": {
                "maxAttempts": 6,
                "multiplier": 1.5,
                "intervalFunction": "EXPONENTIAL_BACKOFF",
                "initialIntervalMillis": [100]
            }
        }
    ]
}
```
The test scenario parameters are grouped into two categories: **control parameters**, and **resilience parameters**.

### Control parameters

These parameters control the test scenarios execution. 

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| testId | `string` | no | The test identifier. If not defined, a test identifier will be automatically generated containing the date and time of the test execution. The test identifier is used as the name of the CSV file to be generated containing the test results. |
| concurrentUsers | `array of numbers` |  yes | Array containing the numbers of instances of the client service that will concurrently invoke the target service during each scenario execution. Each element of the array represents a different test scenario. |
| rounds | `number` | yes | Number of executions of each scenario. |
| targetSuccessfulRequests | `number` | yes | Expected number of successful invocations of the target service by the client service. |
| maxRequestsAllowed | `number` | yes | Maximum number of (either successful or unsuccessful) invocations of the target service by the client service. |
| fault | `faultSpec` | yes | Specification of the failure type to be injected by the proxy service into the target service invocation flow. See the faultSpec scheme below |

The latter parameter is useful to prevent the client application from never reaching the required number of successful invocations in a reasonable window of time, which may happen under high server failure rates.

#### FaultSpec scheme

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| type | `string` | yes | Type of failure to be injected. Currently supported types: *delay* and *abort*. |
| percentage | `array of numbers` | yes | Array containing the percentages of failures to be injected by the proxy service into the target service invocation flow. Each element of the array represents a different test scenario. 
| duration | `number` | no | Duration (in miliseconds) of the delay failures to injected by the proxy service. Required when type is *delay*. |
| status | `number` | no | HTTP status code to be returned by the proxy service to the client service upon each failed invocation. Required when type is *abort*. |


### Resilience parameters

These parameters define and configure the resilience strategy the client application will use to invoke the target service. 

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| pattern | `string` | yes | The name of the resilience strategy to be used by the cliente service. |
| platform | `string` | yes | The name of the language/plataform where the client service was implemented. |
| lib | `string` | yes | The name of the resilience library used by the client service. |
| url | `string` | yes | The url where the client service is deployed. |
| patternConfig | `object` | yes | The set of configuration paramaters used by the client service to instantiate the given resilience strategy. |

