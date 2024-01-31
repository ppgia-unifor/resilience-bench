package br.unifor.ppgia.resilience4j.circuitBreaker;

import io.github.resilience4j.circuitbreaker.CircuitBreakerConfig.SlidingWindowType;

public class CircuitBreakerRequestModel {
    private final Float failureRateThreshold;
    private final Integer slidingWindowSize;
    private final Integer minimumNumberOfCalls;
    private final SlidingWindowType slidingWindowType;

    public CircuitBreakerRequestModel(Float failureRateThreshold,
                                      Integer slidingWindowSize,
                                      Integer minimumNumberOfCalls,
                                      String slidingWindowType) {
        this.failureRateThreshold = failureRateThreshold;
        this.slidingWindowSize = slidingWindowSize;
        this.minimumNumberOfCalls = minimumNumberOfCalls;

        if (slidingWindowType == null || slidingWindowType.isEmpty()) {
            this.slidingWindowType = SlidingWindowType.COUNT_BASED;
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
}
