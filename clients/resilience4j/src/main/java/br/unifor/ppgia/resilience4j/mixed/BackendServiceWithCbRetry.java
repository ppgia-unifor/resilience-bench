package br.unifor.ppgia.resilience4j.mixed;

import br.unifor.ppgia.resilience4j.BackendServiceTemplate;
import br.unifor.ppgia.resilience4j.RestClient;
import io.github.resilience4j.circuitbreaker.CircuitBreaker;
import io.github.resilience4j.circuitbreaker.CircuitBreakerConfig;
import io.github.resilience4j.circuitbreaker.CircuitBreakerRegistry;
import io.github.resilience4j.circuitbreaker.event.CircuitBreakerEvent;
import io.vavr.CheckedFunction0;
import org.slf4j.Logger;
import org.springframework.http.ResponseEntity;

import java.time.Duration;

public class BackendServiceWithCircuitBreaker extends BackendServiceTemplate {

    private final CircuitBreaker circuitBreakerPolicy;

    private final static Logger logger = org.slf4j.LoggerFactory.getLogger(BackendServiceWithCircuitBreaker.class);

    public BackendServiceWithCircuitBreaker(
            RestClient restClient,
            CircuitBreakerRequestModel circuitBreakerRequestModel
    ) {
        super(restClient);
        circuitBreakerPolicy = CircuitBreakerRegistry.of(createCircuitBreaker(circuitBreakerRequestModel)).circuitBreaker("cb");
        circuitBreakerPolicy.getEventPublisher().onEvent(event -> {
            if (!event.getEventType().equals(CircuitBreakerEvent.Type.NOT_PERMITTED)) {
                logger.info("FailureRate: " + circuitBreakerPolicy.getMetrics().getFailureRate());
            }
        });
        circuitBreakerPolicy.getEventPublisher().onFailureRateExceeded(event -> {
            logger.info("Failure rate exceeded: "+ event.getFailureRate());
        });
        circuitBreakerPolicy.getEventPublisher().onStateTransition(event -> {
            logger.info("State transition from: " + event.getStateTransition().getFromState() + " to: " + event.getStateTransition().getToState());
        });
    }

    @Override
    protected CheckedFunction0<ResponseEntity<String>> decorate(CheckedFunction0<ResponseEntity<String>> checkedFunction) {
        return circuitBreakerPolicy.decorateCheckedSupplier(checkedFunction);
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
