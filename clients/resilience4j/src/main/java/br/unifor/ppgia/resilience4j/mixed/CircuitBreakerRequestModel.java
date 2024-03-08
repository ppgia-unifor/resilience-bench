package br.unifor.ppgia.resilience4j.circuitBreaker;

import java.time.Duration;

import io.github.resilience4j.circuitbreaker.CircuitBreakerConfig;
import io.github.resilience4j.circuitbreaker.CircuitBreakerConfig.SlidingWindowType;

public class CircuitBreakerRequestModel {
    private final Float failureRateThreshold;
    private final Integer slidingWindowSize;
    private final Integer minimumNumberOfCalls;
    private final Integer waitDurationInOpenState;

    private final Integer permittedNumberOfCallsInHalfOpenState;

    private final Integer permittedNumberOfCallsInOpenState;
    private final SlidingWindowType slidingWindowType;

    public CircuitBreakerRequestModel(Float failureRateThreshold,
                                      Integer slidingWindowSize,
                                      Integer minimumNumberOfCalls,
                                      Integer waitDurationInOpenState,
                                      Integer permittedNumberOfCallsInHalfOpenState,
                                      Integer permittedNumberOfCallsInOpenState,
                                      String slidingWindowType) {
        this.failureRateThreshold = failureRateThreshold;
        this.slidingWindowSize = slidingWindowSize;
        this.minimumNumberOfCalls = minimumNumberOfCalls;
        this.waitDurationInOpenState = waitDurationInOpenState;
        this.permittedNumberOfCallsInHalfOpenState = permittedNumberOfCallsInHalfOpenState;
        this.permittedNumberOfCallsInOpenState = permittedNumberOfCallsInOpenState;

        if (slidingWindowType == null || slidingWindowType.isEmpty()) {
            this.slidingWindowType = CircuitBreakerConfig.DEFAULT_SLIDING_WINDOW_TYPE;
        } else {
            this.slidingWindowType = SlidingWindowType.valueOf(slidingWindowType);
        }
    }

    public Float getFailureRateThreshold() {
        return failureRateThreshold;
    }

    public Integer getSlidingWindowSize() {
        return slidingWindowSize;
    }

    public Integer getMinimumNumberOfCalls() {
        return minimumNumberOfCalls;
    }

    public SlidingWindowType getSlidingWindowType() {
        return slidingWindowType;
    }

    public Integer getWaitDurationInOpenState() {
        return waitDurationInOpenState;
    }

    public Integer getPermittedNumberOfCallsInHalfOpenState() {
        return permittedNumberOfCallsInHalfOpenState;
    }

    public Integer getPermittedNumberOfCallsInOpenState() {
        return permittedNumberOfCallsInOpenState;
    }
}
