package br.unifor.ppgia.resilience4j.circuitBreaker;

import org.junit.jupiter.api.Test;

import io.github.resilience4j.circuitbreaker.CircuitBreakerConfig;

import static io.github.resilience4j.circuitbreaker.CircuitBreakerConfig.SlidingWindowType;
import static org.junit.jupiter.api.Assertions.assertEquals;

class CircuitBreakerRequestModelTest {

  @Test
  void getSlidingWindowTypeNullTest() {
    var target = new CircuitBreakerRequestModel(
            0.5f,
            10,
            10,
            10,
            10,
            10,
            null
    );
    assertEquals(target.getSlidingWindowType(), CircuitBreakerConfig.DEFAULT_SLIDING_WINDOW_TYPE);
  }
  @Test
  void getSlidingWindowTypeEmptyTest() {
    var target = new CircuitBreakerRequestModel(
            0.5f,
            10,
            10,
            10,
            10,
            10,
            ""
    );
    assertEquals(target.getSlidingWindowType(), CircuitBreakerConfig.DEFAULT_SLIDING_WINDOW_TYPE);
  }
  @Test
  void getSlidingWindowTypeCountBasedTest() {
    var target = new CircuitBreakerRequestModel(
            0.5f,
            10,
            10,
            10,
            10,
            10,
            "COUNT_BASED"
    );

    assertEquals(target.getSlidingWindowType(), SlidingWindowType.COUNT_BASED);
  }

  @Test
  void getSlidingWindowTypeTimeBasedTest() {
    var target = new CircuitBreakerRequestModel(
            0.5f,
            10,
            10,
            10,
            10,
            10,
            "TIME_BASED"
    );
    assertEquals(target.getSlidingWindowType(), SlidingWindowType.TIME_BASED);
  }
}