package br.unifor.ppgia.resilience4j.retry;

public class RetryRequestModel {
    private final Integer maxAttempts;
    private final Integer waitDuration;
    private final Double multiplier;
    private final String intervalFunction;
    private final Integer initialIntervalMillis;

    public RetryRequestModel(Integer maxAttempts, Integer waitDuration, Double multiplier, String intervalFunction, Integer initialIntervalMillis) {
        this.maxAttempts = maxAttempts;
        this.waitDuration = waitDuration;
        this.multiplier = multiplier;
        this.intervalFunction = intervalFunction;
        this.initialIntervalMillis = initialIntervalMillis;
    }

    public Integer getMaxAttempts() {
        return maxAttempts;
    }

    public Integer getWaitDuration() {
        return waitDuration;
    }

    public String getIntervalFunction() {
        return intervalFunction;
    }

    public Integer getInitialIntervalMillis() {
        return initialIntervalMillis;
    }

    public Double getMultiplier() {
        return multiplier;
    }
}
