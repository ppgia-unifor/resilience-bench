package br.unifor.ppgia.resilience4j.circuitBreaker;

public class CircuitBreakerRequestModel {
    private final Float failureRateThreshold;
    private final Integer slidingWindowSize;
    private final Integer minimumNumberOfCalls;
    private final Integer waitDurationInOpenState; //waitDurationInOpenState [ms]
    private final Integer permittedNumberOfCallsInHalfOpenState;
    private final Integer slowCallRateThreshold;
    private final Integer slowCallDurationThreshold; //[ms]

    public CircuitBreakerRequestModel(Float failureRateThreshold,
                                      Integer slidingWindowSize,
                                      Integer minimumNumberOfCalls,
                                      Integer waitDurationInOpenState,
                                      Integer permittedNumberOfCallsInHalfOpenState,
                                      Integer slowCallRateThreshold,
                                      Integer slowCallDurationThreshold
    ) {
        this.failureRateThreshold = failureRateThreshold;
        this.slidingWindowSize = slidingWindowSize;
        this.minimumNumberOfCalls = minimumNumberOfCalls;
        this.waitDurationInOpenState = waitDurationInOpenState;
        this.permittedNumberOfCallsInHalfOpenState = permittedNumberOfCallsInHalfOpenState;
        this.slowCallRateThreshold = slowCallRateThreshold;
        this.slowCallDurationThreshold = slowCallDurationThreshold;
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

    public Integer getWaitDurationInOpenState() {
        return waitDurationInOpenState;
    }

    public Integer getPermittedNumberOfCallsInHalfOpenState() {
        return permittedNumberOfCallsInHalfOpenState;
    }

    public Integer getSlowCallRateThreshold() {
        return slowCallRateThreshold;
    }

    public Integer getSlowCallDurationThreshold() {
        return slowCallDurationThreshold;
    }
}
