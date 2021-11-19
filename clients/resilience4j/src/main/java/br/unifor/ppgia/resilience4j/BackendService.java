package br.unifor.ppgia.resilience4j;

import io.github.resilience4j.decorators.Decorators;
import org.springframework.http.*;
import org.springframework.util.StopWatch;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

import java.util.function.Supplier;

import static org.springframework.http.HttpMethod.*;

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

    protected abstract Supplier<ResponseEntity<String>> decorate(Supplier<ResponseEntity<String>> supplier);

    public <P> ResilienceModuleMetrics doHttpRequest(long userId, Config<P> config) {
        var successfulRequests = 0;
        var totalRequests = 0;
        var metrics = new ResilienceModuleMetrics(userId);
        var entity = new HttpEntity<String>(new HttpHeaders());

        var externalStopwatch = new StopWatch();
        externalStopwatch.start();
        while (successfulRequests < config.getTargetSuccessfulRequests() && config.getMaxRequestsAllowed() > totalRequests) {

            Supplier<ResponseEntity<String>> supplier = () -> {
                var requestStopwatch = new StopWatch();
                try {
                    requestStopwatch.start();
                    var response = this.restTemplate.exchange(endpoint, GET, entity, String.class);
                    requestStopwatch.stop();
                    if (response.getStatusCode().is2xxSuccessful()) {
                        metrics.registerSuccess(requestStopwatch.getTotalTimeMillis());
                    }
                    return response;
                } catch (RestClientException e) {
                    metrics.registerError(requestStopwatch.getTotalTimeMillis());
                    throw e;
                }
            };

            var result = decorate(supplier).get();

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
