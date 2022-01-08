package br.unifor.ppgia.resilience4j;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.client.RestTemplate;

public class RestClient {

    private final static Logger logger = LoggerFactory.getLogger(RestClient.class);

    private final RestTemplate restTemplate;
    private final String resource;

    public RestClient(RestTemplate restTemplate, String resource) {
        this.restTemplate = restTemplate;
        this.resource = resource;
    }

    public ResponseEntity<String> get() {
        var response = restTemplate.getForEntity(resource, String.class);
        var bodyLength = response.hasBody() ? response.getBody().length() : 0;
        logger.info("Response: body size {} status {}", bodyLength, response.getStatusCode());
        return response;
    }
}
