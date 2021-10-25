package br.unifor.ppgia.resilience4j.retry;

import br.unifor.ppgia.resilience4j.BackendService;
import io.github.resilience4j.retry.RetryConfig;
import io.github.resilience4j.retry.RetryRegistry;
import io.vavr.control.Try;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;

import java.time.Duration;

import static io.github.resilience4j.core.IntervalFunction.ofExponentialBackoff;
import static io.github.resilience4j.retry.Retry.decorateSupplier;

@Controller
@RequestMapping("/retry")
public class RetryController {

    private final BackendService backendService;

    public RetryController(BackendService backendService) {
        this.backendService = backendService;
    }

    @PostMapping
    public ResponseEntity<?> index(@RequestBody RetryRequestModel body) {
        var config = buildConfig(body);
        var retry = RetryRegistry.of(config).retry("retry1");
        retry.getEventPublisher()
                .onError(event -> {
                    System.out.println("error");
                })
                .onRetry(event -> {
                    System.out.println("try again");
                });
        var decoratedSupplier = decorateSupplier(retry, backendService::doHttpRequest);
        Try.ofSupplier(decoratedSupplier).get();
        return ResponseEntity.ok().build();
    }

    private RetryConfig buildConfig(RetryRequestModel body) {
        var initialConfig = RetryConfig.custom().maxAttempts(body.getMaxAttempts());
        if ("FIXED".equalsIgnoreCase(body.getIntervalFunction())) {
            return initialConfig.waitDuration(Duration.ofMillis(body.getWaitDuration())).build();
        } else {
            return initialConfig.intervalFunction(ofExponentialBackoff(body.getInitialIntervalMillis())).build();
        }
    }
}
