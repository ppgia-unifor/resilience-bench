package br.unifor.ppgia.resilience4j.retry;

import br.unifor.ppgia.resilience4j.BackendService;
import br.unifor.ppgia.resilience4j.BackendServiceWithRetry;
import br.unifor.ppgia.resilience4j.Config;
import br.unifor.ppgia.resilience4j.User;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.client.RestTemplate;

@Controller
@RequestMapping("/retry")
public class RetryController {

    private BackendService backendService;
    private final String host;
    private final RestTemplate restTemplate;
    private final User user;
    public RetryController(@Value("#{environment.BACKEND_HOST}") String host,
                           RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
        this.host = host;
        this.user = new User();
    }

    @PostMapping
    public ResponseEntity<?> index(@RequestBody Config<RetryRequestModel> config) {
        this.backendService = new BackendServiceWithRetry(restTemplate, host, config.getParams());
        var metrics = user.spawnAsync(backendService, config);
        return ResponseEntity.ok(metrics);
    }
}
