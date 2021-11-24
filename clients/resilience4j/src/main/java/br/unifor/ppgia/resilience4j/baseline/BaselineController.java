package br.unifor.ppgia.resilience4j.baseline;

import br.unifor.ppgia.resilience4j.BackendServiceTemplate;
import br.unifor.ppgia.resilience4j.retry.BackendServiceWithRetry;
import br.unifor.ppgia.resilience4j.Config;
import br.unifor.ppgia.resilience4j.User;
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

    private BackendServiceTemplate backendService;
    private final String host;
    private final RestTemplate restTemplate;
    private final User user;
    public BaselineController(@Value("#{environment.HOST}") String host,
                           RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
        this.host = host;
        this.user = new User();
    }

    @PostMapping
    public ResponseEntity<?> index(@RequestBody Config<RetryRequestModel> config) {
        this.backendService = new BackendServiceSimple(restTemplate, host);
        var metrics = user.spawnAsync(backendService, config);
        return ResponseEntity.ok(metrics);
    }
}
