package br.unifor.ppgia.resilience4j;

public class ResilienceModuleMetrics {
    private final long userId;
    private int successfulCalls;
    private int unsuccessfulCalls;
    private int successfulRequests;
    private int unsuccessfulRequests;
    private long successTime;
    private long errorTime;
    private long totalExecutionTime;

    public ResilienceModuleMetrics(long userId) {
        this.userId = userId;
    }

    public long getUserId() {
        return userId;
    }

    public int getSuccessfulCalls() {
        return successfulCalls;
    }

    public int getUnsuccessfulCalls() {
        return unsuccessfulCalls;
    }

    public int getSuccessfulRequests() {
        return successfulRequests;
    }

    public int getUnsuccessfulRequests() {
        return unsuccessfulRequests;
    }

    public long getSuccessTime() {
        return successTime;
    }

    public long getErrorTime() {
        return errorTime;
    }

    public long getTotalExecutionTime() {
        return totalExecutionTime;
    }

    public long getTotalContentionTime() {
        return successTime + errorTime;
    }

    public int getTotalRequests() {
        return successfulRequests + unsuccessfulRequests;
    }

    public void registerSuccess(long elapsedTime) {
        successfulRequests++;
        successTime += elapsedTime;
    }

    public void registerError(long elapsedTime) {
        unsuccessfulRequests++;
        errorTime += elapsedTime;
    }

    public void registerTotals(int totalRequests, int successfulRequests, long totalExecutionTime) {
        successfulCalls = successfulRequests;
        unsuccessfulCalls = totalRequests - successfulRequests;
        this.totalExecutionTime = totalExecutionTime;
    }
}
