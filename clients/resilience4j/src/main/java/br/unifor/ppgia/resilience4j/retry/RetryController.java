package br.unifor.ppgia.resilience4j.retry;

import br.unifor.ppgia.resilience4j.Config;
import br.unifor.ppgia.resilience4j.RestClient;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/retry")
public class RetryController {

    private final RestClient restClient;

    public RetryController(RestClient restClient) {
        this.restClient = restClient;
    }

    @PostMapping
    public ResponseEntity<?> index(@RequestBody Config<RetryRequestModel> config) {
        var backendService = new BackendServiceWithRetry(restClient, config.getPatternParams());
        var metrics = backendService.doHttpRequest(config);
        return ResponseEntity.ok(metrics);
    }
}
