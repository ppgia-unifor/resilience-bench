package br.unifor.ppgia.resilience4j;

import io.vavr.CheckedFunction0;
import io.vavr.control.Try;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.ResponseEntity;
import org.springframework.util.StopWatch;
import org.springframework.web.client.HttpServerErrorException;
import org.springframework.web.client.RestTemplate;

import static org.springframework.http.HttpMethod.GET;

public abstract class BackendServiceTemplate {
    private final String endpoint;
    private final RestTemplate restTemplate;

    public BackendServiceTemplate(
            RestTemplate restTemplate,
            String host
    ) {
        this.restTemplate = restTemplate;
        this.endpoint = host + "/status/200";
    }

    protected abstract CheckedFunction0<ResponseEntity<String>> decorate(CheckedFunction0<ResponseEntity<String>> checkedFunction);

    public <P> ResilienceModuleMetrics doHttpRequest(long userId, Config<P> config) {
        var successfulCalls = 0;
        var totalCalls = 0;
        var metrics = new ResilienceModuleMetrics(userId);
        var headers = new HttpHeaders();
        headers.add("Keep-Alive", "timeout=0, max=0");
        headers.add("Cache-Control", "no-cache");
        var entity = new HttpEntity<String>(headers);

        var externalStopwatch = new StopWatch();
        externalStopwatch.start();
        while (successfulCalls < config.getTargetSuccessfulRequests() && config.getMaxRequestsAllowed() > totalCalls) {
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
                } catch (HttpServerErrorException e) {
                    requestStopwatch.stop();
                    metrics.registerError(requestStopwatch.getTotalTimeMillis());
                    throw e;
                }
            };
            var result = Try.of(decorate(sendRequestFn)).recover(throwable -> ResponseEntity.status(500).build()).get();

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
