package br.unifor.ppgia.resilience4j;

import br.unifor.ppgia.resilience4j.retry.RetryRequestModel;
import io.github.resilience4j.retry.Retry;
import io.github.resilience4j.retry.RetryConfig;
import io.github.resilience4j.retry.RetryRegistry;
import org.springframework.http.ResponseEntity;
import org.springframework.web.client.RestTemplate;

import java.util.function.Supplier;

import static io.github.resilience4j.core.IntervalFunction.ofExponentialBackoff;
import static io.github.resilience4j.retry.Retry.decorateSupplier;

public class BackendServiceWithRetry extends BackendService {

    private final Retry retryPolicy;

    public BackendServiceWithRetry(
            RestTemplate restTemplate,
            String host,
            RetryRequestModel retryRequestModel
    ) {
        super(restTemplate, host);
        var retryConfig = createRetryWithExponentialBackoff(retryRequestModel);
        retryPolicy = RetryRegistry.of(retryConfig).retry("retry");
    }

    @Override
    protected Supplier<ResponseEntity<String>> decorate(Supplier<ResponseEntity<String>> supplier) {
        return decorateSupplier(retryPolicy, supplier);
    }

    private static RetryConfig createRetryWithExponentialBackoff(RetryRequestModel body) {
        var initialConfig = RetryConfig.custom().maxAttempts(body.getMaxAttempts());
        return initialConfig.intervalFunction(ofExponentialBackoff(body.getInitialIntervalMillis(), body.getMultiplier())).build();
    }
}
