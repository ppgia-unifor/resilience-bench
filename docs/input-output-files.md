# Scenarios (input file)

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
| testId | `string` | no | Identifier of test. If not set, a timespam will be generated. |
| concurrentUsers | `number` |  yes | Number of concurrent virtual users to invoke the HTTP server during each test. |
| rounds | `number` | yes | Number of test executions per scenario. |
| targetSuccessfulRequests | `number` | yes | Minimum number of successful invocations from the client to the server application. |
| maxRequestsAllowed | `number` | yes | Maximum number of invocations the client application is allowed to perform overall. |

The latter parameter is useful to prevent the client application from never reaching the required number of successful invocations in a reasonable window of time, which may happen under high server failure rates.

#### Fault injection

Rate with which the proxy server will inject failures into the request stream the target service receives from the client application.

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| type | `string` | yes | Type of fault. Accepted values: *delay* or *fault*. |
| percentage | `array` | yes | Rate which the proxy server will inject failures into the request stream. |
| duration | `number` | no | Time in miliseconds the server will delay. Required when type is *delay*. |
| status | `number` | no | HTTP status code the server will return. Required when type is *abort*. |


#### Pattern

Resilience strategy the client application will use to invoke the target service. It's an array where is possible to define several clients and their patterns. Each pattern (e.g: retry or circuit breaker) is one object in this array. To group them in the result dataset, use `lib` and `platform` properties. 

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| pattern | `string` | yes | The name of pattern. |
| platform | `string` | yes | The name of plataform. |
| lib | `string` | yes | The name of library. |
| url | `string` | yes | The url that process the tasks wrapped in pattern |
| configTemplate | `object` | yes | The library's pattern configuration. It's a dynamic object and the value will be processed and passed to the `url`. |



# Results (output file)

<table>
    <thead>
        <tr>
            <th>Parameter</th>
            <th>Type</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>totalCalls</td>
            <td><code>number</code></td>
            <td>number of total invocations of the target service by the client application</td>
        </tr>
        <tr>
            <td>successfulCalls</td>
            <td><code>number</code></td>
            <td rowspan=2>segmented number of successful and unsuccessful invocations of the target service by the client application</td>
        </tr>
        <tr>
            <td>unsuccessfulCalls</td>
            <td><code>number</code></td>
        </tr>
        <tr>
            <td>totalRequests</td>
            <td><code>number</code></td>
            <td>number of total requests of the target service by the client application, including the retries</td>
        </tr>
        <tr>
            <td>successfulRequests</td>
            <td><code>number</code></td>
            <td rowspan=2>segmented number of successful and unsuccessful requests of the target service by the client application, including the retries</td>
        </tr>
        <tr>
            <td>unsuccessfulRequests</td>
            <td><code>number</code></td>
        </tr>
        <tr>
            <td>successTime</td>
            <td><code>number</code></td>
            <td></td>
        </tr>
        <tr>
            <td>successTimePerRequest</td>
            <td><code>number</code></td>
            <td></td>
        </tr>
        <tr>
            <td>errorTime</td>
            <td><code>number</code></td>
            <td></td>
        </tr>
         <tr>
            <td>errorTimePerRequest</td>
            <td><code>number</code></td>
            <td></td>
        </tr>
        <tr>
            <td>totalContentionTime</td>
            <td><code>number</code></td>
            <td>Total execution time spent waiting for either a successful or an unsuccessful response from the target service</td>
        </tr>
        <tr>
            <td>contentionRate</td>
            <td><code>number</code></td>
            <td>Fraction of the client application's total execution time spent waiting for either a successful or an unsuccessful response from the target service</td>
        </tr>
        <tr>
            <td>throughput</td>
            <td><code>number</code></td>
            <td>Requests per seconds sent to target service by client service</td>
        </tr>
        <tr>
            <td>userId</td>
            <td><code>number</code></td>
            <td>Unique identifier of the virtual user</td>
        </tr>
        <tr>
            <td>startTime</td>
            <td><code>timestamp</code></td>
            <td rowspan=2>Time when the client service start/end sending requests to target service</td>
        </tr>
        <tr>
            <td>endTime</td>
            <td><code>timestamp</code></td>
        </tr>
        <tr>
            <td>users</td>
            <td><code>number</code></td>
            <td>Virtual users simulated in this round</td>
        </tr>
        <tr>
            <td>round</td>
            <td><code>number</code></td>
            <td>Current round of the test</td>
        </tr>
        <tr>
            <td>lib</td>
            <td><code>string</code></td>
            <td>The library name</td>
        </tr>
        <tr>
            <td>pattern</td>
            <td><code>string</code></td>
            <td>The pattern name</td>
        </tr>
        <tr>
            <td>faultPercentage</td>
            <td><code>number</code></td>
            <td>Rate of failure which was injected into the request stream</td>
        </tr>
        <tr>
            <td>faultType</td>
            <td><code>string</code></td>
            <td>Type of failure which was injected into the request stream</td>
        </tr>
        <tr>
            <td>faultStatus</td>
            <td><code>number</code></td>
            <td>HTTP status code sent when the request failed</td>
        </tr>
    </tbody>
</table>
