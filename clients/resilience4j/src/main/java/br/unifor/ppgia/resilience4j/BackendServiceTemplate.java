package br.unifor.ppgia.resilience4j;

import io.vavr.CheckedFunction0;
import io.vavr.control.Try;
import org.springframework.http.ResponseEntity;
import org.springframework.util.StopWatch;
import org.springframework.web.client.RestClientException;

public abstract class BackendServiceTemplate {
    private final ResilienceModuleMetrics metrics;
    private final RestClient restClient;

    public BackendServiceTemplate(RestClient restClient) {
        this.restClient = restClient;
        metrics = new ResilienceModuleMetrics();
    }

    protected abstract CheckedFunction0<ResponseEntity<String>> decorate(CheckedFunction0<ResponseEntity<String>> checkedFunction);

    private ResponseEntity<String> sendRequest(String targetUrl) {
        var requestStopwatch = new StopWatch();
        try {
            requestStopwatch.start();
            var response = restClient.get(targetUrl);
            requestStopwatch.stop();
            if (response.getStatusCode().is2xxSuccessful()) {
                metrics.registerSuccess(requestStopwatch.getTotalTimeMillis());
            }
            return response;
        } catch (RestClientException e) {
            requestStopwatch.stop();
            metrics.registerError(requestStopwatch.getTotalTimeMillis());
            throw e;
        }
    }

    public <P> ResilienceModuleMetrics doHttpRequest(Config<P> config) {
        var successfulCalls = 0;
        var totalCalls = 0;
        var externalStopwatch = new StopWatch();
        externalStopwatch.start();
        while (successfulCalls < config.getSuccessfulRequests() && config.getMaxRequests() > metrics.getTotalRequests()) {
            var supplier = decorate(() -> this.sendRequest(config.getTargetUrl()));
            var result = Try.of(supplier).recover(throwable -> ResponseEntity.status(503).build()).get();
            if (result.getStatusCode().is2xxSuccessful()) {
                successfulCalls++;
            }
            totalCalls++;
        }
        externalStopwatch.stop();
        metrics.registerTotals(totalCalls, successfulCalls, externalStopwatch.getTotalTimeMillis());
        return metrics;
    }
}
