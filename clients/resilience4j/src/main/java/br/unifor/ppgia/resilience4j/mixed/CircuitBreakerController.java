package br.unifor.ppgia.resilience4j.circuitBreaker;

import br.unifor.ppgia.resilience4j.Config;
import br.unifor.ppgia.resilience4j.RestClient;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/cb")
public class CircuitBreakerController {

    private final RestClient restClient;

    public CircuitBreakerController(RestClient restClient) {
        this.restClient = restClient;
    }

    @PostMapping
    public ResponseEntity<?> index(@RequestBody Config<CircuitBreakerRequestModel> config) {
        var backendService = new BackendServiceWithCircuitBreaker(restClient, config.getPatternParams());
        var metrics = backendService.doHttpRequest(config);
        return ResponseEntity.ok(metrics);
    }
}
