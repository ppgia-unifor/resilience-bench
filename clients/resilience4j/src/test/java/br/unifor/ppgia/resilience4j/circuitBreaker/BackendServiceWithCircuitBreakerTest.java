package br.unifor.ppgia.resilience4j.circuitBreaker;

import io.github.resilience4j.circuitbreaker.CircuitBreakerConfig;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class BackendServiceWithCircuitBreakerTest {

  @Test
  void createCircuitBreakerTest() {
    var cb = BackendServiceWithCircuitBreaker.createCircuitBreaker(new CircuitBreakerRequestModel(
            0.5f,
            10,
            10,
            10,
            10,
            10,
            "COUNT_BASED"
    ));

    assertEquals(cb.getFailureRateThreshold(), 0.5f);
    assertEquals(cb.getSlidingWindowSize(), 10);
    assertEquals(cb.getMinimumNumberOfCalls(), 10);
    assertEquals(cb.getSlidingWindowType(), CircuitBreakerConfig.SlidingWindowType.COUNT_BASED);
  }
}