package br.unifor.ppgia.resilience4j.retry;

import br.unifor.ppgia.resilience4j.BackendServiceTemplate;
import io.github.resilience4j.retry.Retry;
import io.github.resilience4j.retry.RetryConfig;
import io.github.resilience4j.retry.RetryRegistry;
import io.vavr.CheckedFunction0;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.client.RestTemplate;

import static io.github.resilience4j.core.IntervalFunction.ofExponentialBackoff;
import static io.github.resilience4j.retry.Retry.decorateCheckedSupplier;

public class BackendServiceWithRetry extends BackendServiceTemplate {

    private final static Logger logger = LoggerFactory.getLogger(BackendServiceWithRetry.class);
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
        retryPolicy.getEventPublisher().onRetry(event -> {
            logger.info("Retry {}", event.getNumberOfRetryAttempts());
        });
    }

    @Override
    protected CheckedFunction0<ResponseEntity<String>> decorate(CheckedFunction0<ResponseEntity<String>> checkedFunction) {
        return decorateCheckedSupplier(retryPolicy, checkedFunction);
    }

    private static RetryConfig createRetryWithExponentialBackoff(RetryRequestModel body) {
        return RetryConfig
                .custom()
                .maxAttempts(body.getMaxAttempts())
                .intervalFunction(ofExponentialBackoff(body.getInitialIntervalMillis(), body.getMultiplier()))
                .build();
    }
}
