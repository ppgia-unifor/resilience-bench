package br.unifor.ppgia.resilience4j;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class ResilienceModuleMetrics {
    private final static Logger logger = LoggerFactory.getLogger(ResilienceModuleMetrics.class);

    private int successfulCalls;
    private int unsuccessfulCalls;
    private int successfulRequests;
    private int unsuccessfulRequests;
    private long successTime;
    private long errorTime;
    private long totalExecutionTime;

    public ResilienceModuleMetrics() {
    }

    public int getSuccessfulCalls() {
        return successfulCalls;
    }

    public int getUnsuccessfulCalls() {
        return unsuccessfulCalls;
    }

    public int getTotalCalls() {
        return getSuccessfulCalls() + getUnsuccessfulCalls();
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

    public double getSuccessTimePerRequest() {
        if (successfulRequests > 0) {
                return successTime / (double) successfulRequests;
            }
        else {
            return 0;
        }
    }

    public long getErrorTime() {
        return errorTime;
    }

    public double getErrorTimePerRequest() {
        if (unsuccessfulRequests > 0) {
                return errorTime / (double) unsuccessfulRequests;
            }
        else {
            return 0;
        }
    }

    public double getThroughput() {
        if (totalExecutionTime > 0) {
                return 1000 * getTotalRequests() / (double) totalExecutionTime;
            }
        else {
            return 0;
        }       
    }
    
    public long getTotalExecutionTime() {
        return totalExecutionTime;
    }

    public long getTotalContentionTime() {
        return successTime + errorTime;
    }

    public double getContentionRate() {
        if (totalExecutionTime > 0) {
                return getTotalContentionTime() / (double) totalExecutionTime;
            }
        else {
            return 0;
        }
    }
    
    public int getTotalRequests() {
        return successfulRequests + unsuccessfulRequests;
    }

    public void registerSuccess(long elapsedTime) {
        successfulRequests++;
        successTime += elapsedTime;
        logger.info("Registering {} successful request in {} ms", successfulRequests, successTime);
    }

    public void registerError(long elapsedTime) {
        unsuccessfulRequests++;
        errorTime += elapsedTime;
        logger.info("Registering {} unsuccessful request in {} ms", unsuccessfulRequests, errorTime);
    }

    public void registerTotals(int totalCalls, int successfulCalls, long totalExecutionTime) {
        this.successfulCalls = successfulCalls;
        unsuccessfulCalls = totalCalls - this.successfulCalls;
        this.totalExecutionTime = totalExecutionTime;
    }
}
