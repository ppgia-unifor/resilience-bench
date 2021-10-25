package br.unifor.ppgia.resilience4j.circuitBreaker;

import br.unifor.ppgia.resilience4j.BackendService;
import io.github.resilience4j.circuitbreaker.CircuitBreakerConfig;
import io.github.resilience4j.circuitbreaker.CircuitBreakerRegistry;
import io.vavr.control.Try;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;

import java.time.Duration;

import static io.github.resilience4j.circuitbreaker.CircuitBreaker.*;

@Controller
@RequestMapping("/cb")
public class CircuitBreakerController {

    private final BackendService backendService;

    public CircuitBreakerController(BackendService backendService) {
        this.backendService = backendService;
    }

    @PostMapping
    public ResponseEntity<?> index(@RequestBody CircuitBreakerRequestModel params) {
        var circuitBreakerConfig = CircuitBreakerConfig.custom()
                .failureRateThreshold(params.getFailureRateThreshold())
                .slidingWindowSize(params.getSlidingWindowSize())
                .minimumNumberOfCalls(params.getMinimumNumberOfCalls())
                .waitDurationInOpenState(Duration.ofMillis(params.getWaitDurationInOpenState()))
                .permittedNumberOfCallsInHalfOpenState(params.getPermittedNumberOfCallsInHalfOpenState())
                .slowCallRateThreshold(params.getSlowCallRateThreshold())
                .slowCallDurationThreshold(Duration.ofMillis(params.getSlowCallDurationThreshold()))
                .build();

        var circuitBreakerRegistry = CircuitBreakerRegistry.of(circuitBreakerConfig);
        var circuitBreaker = circuitBreakerRegistry.circuitBreaker("cb1");

        circuitBreaker.getEventPublisher()
                .onSuccess(event -> {
//                    result.getResilienceModuleToExternalService().setSuccess(result.getResilienceModuleToExternalService().getSuccess() + 1);
                })
                .onError(event -> {
//                    accumlatedErrorTime += (System.currentTimeMillis() - errorTime);
//                    result.getResilienceModuleToExternalService().setError(result.getResilienceModuleToExternalService().getError() + 1);
                })
                .onStateTransition(event -> {
//                    if( event.getStateTransition().getToState().toString().equals(State.OPEN.toString()) ) {
//                        inactiveTime = System.currentTimeMillis();
//                        result.getCircuitBreakerMetrics().setBreakCount( result.getCircuitBreakerMetrics().getBreakCount() + 1 );
//                    }
                });

        var decoratedSupplier = decorateSupplier(circuitBreaker, backendService::doHttpRequest);
        Try.ofSupplier(decoratedSupplier);
        return ResponseEntity.ok().build();
    }
}
