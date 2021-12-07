package br.unifor.ppgia.resilience4j.circuitBreaker;

import br.unifor.ppgia.resilience4j.BackendServiceTemplate;
import br.unifor.ppgia.resilience4j.Config;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.client.RestTemplate;

@Controller
@RequestMapping("/cb")
public class CircuitBreakerController {

    private final String host;
    private final String resource;
    private final RestTemplate restTemplate;

    public CircuitBreakerController(RestTemplate restTemplate,
                                    @Value("#{environment.HOST}") String host,
                                    @Value("#{environment.RESOURCE}") String resource) {
        this.restTemplate = restTemplate;
        this.host = host;
        this.resource = resource;
    }

    @PostMapping
    public ResponseEntity<?> index(@RequestBody Config<CircuitBreakerRequestModel> config) {
        var backendService = new BackendServiceWithCircuitBreaker(restTemplate, host, resource, config.getParams());
        var metrics = backendService.doHttpRequest(config);
        return ResponseEntity.ok(metrics);
    }
}
