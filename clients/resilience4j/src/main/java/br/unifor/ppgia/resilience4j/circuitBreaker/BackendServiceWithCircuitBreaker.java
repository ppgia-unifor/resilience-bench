package br.unifor.ppgia.resilience4j.circuitBreaker;

import br.unifor.ppgia.resilience4j.BackendServiceTemplate;
import br.unifor.ppgia.resilience4j.circuitBreaker.CircuitBreakerRequestModel;
import io.github.resilience4j.circuitbreaker.CircuitBreaker;
import io.github.resilience4j.circuitbreaker.CircuitBreakerConfig;
import io.github.resilience4j.circuitbreaker.CircuitBreakerRegistry;
import io.vavr.CheckedFunction0;
import org.springframework.http.ResponseEntity;
import org.springframework.web.client.RestTemplate;

import java.time.Duration;

import static io.github.resilience4j.circuitbreaker.CircuitBreaker.decorateCheckedSupplier;

public class BackendServiceWithCircuitBreaker extends BackendServiceTemplate {

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
    protected CheckedFunction0<ResponseEntity<String>> decorate(CheckedFunction0<ResponseEntity<String>> checkedFunction) {
        return decorateCheckedSupplier(circuitBreakerPolicy, checkedFunction);
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
