package br.unifor.ppgia.resilience4j.baseline;

import br.unifor.ppgia.resilience4j.Config;
import br.unifor.ppgia.resilience4j.retry.RetryRequestModel;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.client.RestTemplate;

@Controller
@RequestMapping("/baseline")
public class BaselineController {

    private final RestTemplate restTemplate;
    private final String host;
    private final String resource;

    public BaselineController(RestTemplate restTemplate,
                              @Value("#{environment.HOST}") String host,
                              @Value("#{environment.RESOURCE}") String resource) {
        this.restTemplate = restTemplate;
        this.host = host;
        this.resource = resource;
    }

    @PostMapping
    public ResponseEntity<?> index(@RequestBody Config<RetryRequestModel> config) {
        var backendService = new BackendServiceSimple(restTemplate, host, resource);
        var metrics = backendService.doHttpRequest(config);
        return ResponseEntity.ok(metrics);
    }
}
