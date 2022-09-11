package br.unifor.ppgia.resilience4j;

public class Config<P> {

    private int maxRequests;
    private int successfulRequests;
    private String targetUrl;
    private P patternParams;

    public int getMaxRequests() {
        return maxRequests;
    }

    public void setMaxRequests(int maxRequests) {
        this.maxRequests = maxRequests;
    }

    public int getSuccessfulRequests() {
        return successfulRequests;
    }

    public void setSuccessfulRequests(int successfulRequests) {
        this.successfulRequests = successfulRequests;
    }

    public P getPatternParams() {
        return patternParams;
    }

    public void setPatternParams(P patternParams) {
        this.patternParams = patternParams;
    }

    public String getTargetUrl() {
        return targetUrl;
    }

    public void setTargetUrl(String targetUrl) {
        this.targetUrl = targetUrl;
    }
}
