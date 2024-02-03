package br.unifor.ppgia.resilience4j.circuitBreaker;

import br.unifor.ppgia.resilience4j.BackendServiceTemplate;
import br.unifor.ppgia.resilience4j.RestClient;
import io.github.resilience4j.circuitbreaker.CircuitBreaker;
import io.github.resilience4j.circuitbreaker.CircuitBreakerConfig;
import io.github.resilience4j.circuitbreaker.CircuitBreakerRegistry;
import io.vavr.CheckedFunction0;
import org.springframework.http.ResponseEntity;

import static io.github.resilience4j.circuitbreaker.CircuitBreaker.decorateCheckedSupplier;

import java.time.Duration;

public class BackendServiceWithCircuitBreaker extends BackendServiceTemplate {

    private final CircuitBreaker circuitBreakerPolicy;

    public BackendServiceWithCircuitBreaker(
            RestClient restClient,
            CircuitBreakerRequestModel circuitBreakerRequestModel
    ) {
        super(restClient);
        circuitBreakerPolicy = CircuitBreakerRegistry.of(createCircuitBreaker(circuitBreakerRequestModel)).circuitBreaker("cb");
    }

    @Override
    protected CheckedFunction0<ResponseEntity<String>> decorate(CheckedFunction0<ResponseEntity<String>> checkedFunction) {
        return decorateCheckedSupplier(circuitBreakerPolicy, checkedFunction);
    }

    static CircuitBreakerConfig createCircuitBreaker(CircuitBreakerRequestModel params) {
        var builder = CircuitBreakerConfig.custom().slidingWindowType(params.getSlidingWindowType());

        if (params.getPermittedNumberOfCallsInHalfOpenState() != null) {
            builder.permittedNumberOfCallsInHalfOpenState(params.getPermittedNumberOfCallsInHalfOpenState());
        }
        if (params.getWaitDurationInOpenState() != null) {
            builder.waitDurationInOpenState(Duration.ofMillis(params.getWaitDurationInOpenState()));
        }
        if (params.getFailureRateThreshold() != null) {
            builder.failureRateThreshold(params.getFailureRateThreshold());
        }
        if (params.getSlidingWindowSize() != null) {
            builder.slidingWindowSize(params.getSlidingWindowSize());
        }
        if (params.getMinimumNumberOfCalls() != null) {
            builder.minimumNumberOfCalls(params.getMinimumNumberOfCalls());
        }
        return builder.build();
    }
}
