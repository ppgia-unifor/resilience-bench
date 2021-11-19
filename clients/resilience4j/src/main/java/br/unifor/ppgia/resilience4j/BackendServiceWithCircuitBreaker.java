package br.unifor.ppgia.resilience4j;

import br.unifor.ppgia.resilience4j.circuitBreaker.CircuitBreakerRequestModel;
import io.github.resilience4j.circuitbreaker.CircuitBreaker;
import io.github.resilience4j.circuitbreaker.CircuitBreakerConfig;
import io.github.resilience4j.circuitbreaker.CircuitBreakerRegistry;
import org.springframework.http.ResponseEntity;
import org.springframework.web.client.RestTemplate;

import java.time.Duration;
import java.util.function.Supplier;

import static io.github.resilience4j.circuitbreaker.CircuitBreaker.decorateSupplier;

public class BackendServiceWithCircuitBreaker extends BackendService {

    private final CircuitBreaker circuitBreakerPolicy;

    public BackendServiceWithCircuitBreaker(
            RestTemplate restTemplate,
            String host,
            CircuitBreakerRequestModel circuitBreakerRequestModel
    ) {
        super(restTemplate, host);
        circuitBreakerPolicy = CircuitBreakerRegistry.of(createCircuitBreaker(circuitBreakerRequestModel)).circuitBreaker("cb");
    }

    @Override
    protected Supplier<ResponseEntity<String>> decorate(Supplier<ResponseEntity<String>> supplier) {
        return decorateSupplier(circuitBreakerPolicy, supplier);
    }

    private static CircuitBreakerConfig createCircuitBreaker(CircuitBreakerRequestModel params) {
        return CircuitBreakerConfig.custom()
                .failureRateThreshold(params.getFailureRateThreshold())
                .slidingWindowSize(params.getSlidingWindowSize())
                .minimumNumberOfCalls(params.getMinimumNumberOfCalls())
                .waitDurationInOpenState(Duration.ofMillis(params.getWaitDurationInOpenState()))
                .permittedNumberOfCallsInHalfOpenState(params.getPermittedNumberOfCallsInHalfOpenState())
                .slowCallRateThreshold(params.getSlowCallRateThreshold())
                .slowCallDurationThreshold(Duration.ofMillis(params.getSlowCallDurationThreshold()))
                .build();
    }
}
