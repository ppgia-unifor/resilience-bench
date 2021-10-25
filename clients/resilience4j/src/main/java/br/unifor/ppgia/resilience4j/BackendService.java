package br.unifor.ppgia.resilience4j;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

@Component
public class BackendService {
    private final String endpoint;
    private final RestTemplate restTemplate;

    public BackendService(
            RestTemplate restTemplate,
            @Value("#{environment.SERVER_HOST}") String host
    ) {
        this.restTemplate = restTemplate;
        this.endpoint = host + "/status/200";
    }

    public String doHttpRequest() {
        var entity = new HttpEntity<String>(new HttpHeaders());
        return this.restTemplate.exchange(endpoint, HttpMethod.GET, entity, String.class).getBody();
    }
}
