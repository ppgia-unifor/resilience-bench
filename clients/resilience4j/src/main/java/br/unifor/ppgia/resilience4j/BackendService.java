package br.unifor.ppgia.resilience4j;

import io.vavr.CheckedFunction0;
import io.vavr.control.Try;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.ResponseEntity;
import org.springframework.util.StopWatch;
import org.springframework.web.client.RestTemplate;

import static org.springframework.http.HttpMethod.GET;

public abstract class BackendService {
    private final String endpoint;
    private final RestTemplate restTemplate;

    public BackendService(
            RestTemplate restTemplate,
            String host
    ) {
        this.restTemplate = restTemplate;
        this.endpoint = host + "/status/200";
    }

    protected abstract CheckedFunction0<ResponseEntity<String>> decorate(CheckedFunction0<ResponseEntity<String>> supplier);

    public <P> ResilienceModuleMetrics doHttpRequest(long userId, Config<P> config) {
        var successfulRequests = 0;
        var totalRequests = 0;
        var metrics = new ResilienceModuleMetrics(userId);
        var entity = new HttpEntity<String>(new HttpHeaders());

        var externalStopwatch = new StopWatch();
        externalStopwatch.start();
        while (successfulRequests < config.getTargetSuccessfulRequests() && config.getMaxRequestsAllowed() > totalRequests) {

            CheckedFunction0<ResponseEntity<String>> sendRequestFn = () -> {
                var requestStopwatch = new StopWatch();
                try {
                    requestStopwatch.start();
                    var response = this.restTemplate.exchange(endpoint, GET, entity, String.class);
                    requestStopwatch.stop();
                    if (response.getStatusCode().is2xxSuccessful()) {
                        metrics.registerSuccess(requestStopwatch.getTotalTimeMillis());
                    }
                    return response;
                } catch (Exception e) {
                    metrics.registerError(requestStopwatch.getTotalTimeMillis());
                    throw e;
                }
            };
            var result = Try.of(decorate(sendRequestFn)).recover(throwable -> ResponseEntity.status(500).build()).get();

            if (result.getStatusCode().is2xxSuccessful()) {
                successfulRequests++;
            }
            totalRequests++;
        }
        externalStopwatch.stop();
        metrics.registerTotals(totalRequests, successfulRequests, externalStopwatch.getTotalTimeMillis());
        return metrics;
    }
}
