package br.unifor.ppgia.clientresilience4j.retry;

public class RetryRequestModel {
    private final Integer maxAttempts;
    private final Integer waitDuration;
    private final String intervalFunction;
    private final Integer initialIntervalMillis;

    public RetryRequestModel(Integer maxAttempts, Integer waitDuration, String intervalFunction, Integer initialIntervalMillis) {
        this.maxAttempts = maxAttempts;
        this.waitDuration = waitDuration;
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
}
