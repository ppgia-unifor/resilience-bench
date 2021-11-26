package br.unifor.ppgia.resilience4j.retry;

import br.unifor.ppgia.resilience4j.BackendServiceTemplate;
import br.unifor.ppgia.resilience4j.retry.RetryRequestModel;
import io.github.resilience4j.retry.Retry;
import io.github.resilience4j.retry.RetryConfig;
import io.github.resilience4j.retry.RetryRegistry;
import io.vavr.CheckedFunction0;
import org.springframework.http.ResponseEntity;
import org.springframework.web.client.RestTemplate;

import static io.github.resilience4j.core.IntervalFunction.ofExponentialBackoff;
import static io.github.resilience4j.retry.Retry.decorateCheckedSupplier;

public class BackendServiceWithRetry extends BackendServiceTemplate {

    private final Retry retryPolicy;

    public BackendServiceWithRetry(
            RestTemplate restTemplate,
            String host,
            String resource,
            RetryRequestModel retryRequestModel
    ) {
        super(restTemplate, host, resource);
        var retryConfig = createRetryWithExponentialBackoff(retryRequestModel);
        retryPolicy = RetryRegistry.of(retryConfig).retry("retry");
    }

    @Override
    protected CheckedFunction0<ResponseEntity<String>> decorate(CheckedFunction0<ResponseEntity<String>> checkedFunction) {
        return decorateCheckedSupplier(retryPolicy, checkedFunction);
    }

    private static RetryConfig createRetryWithExponentialBackoff(RetryRequestModel body) {
        var initialConfig = RetryConfig.custom().maxAttempts(body.getMaxAttempts());
        return initialConfig.intervalFunction(ofExponentialBackoff(body.getInitialIntervalMillis(), body.getMultiplier())).build();
    }
}
