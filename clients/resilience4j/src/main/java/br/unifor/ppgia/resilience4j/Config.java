package br.unifor.ppgia.resilience4j;

public class Config<P> {

    private int maxRequestsAllowed;
    private int targetSuccessfulRequests;
    private P params;

    public int getMaxRequestsAllowed() {
        return maxRequestsAllowed;
    }

    public void setMaxRequestsAllowed(int maxRequestsAllowed) {
        this.maxRequestsAllowed = maxRequestsAllowed;
    }

    public int getTargetSuccessfulRequests() {
        return targetSuccessfulRequests;
    }

    public void setTargetSuccessfulRequests(int targetSuccessfulRequests) {
        this.targetSuccessfulRequests = targetSuccessfulRequests;
    }

    public P getParams() {
        return params;
    }

    public void setParams(P params) {
        this.params = params;
    }
}
