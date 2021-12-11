package br.unifor.ppgia.resilience4j;

import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestTemplate;
import java.time.Duration;

@Configuration
public class GeneralConfig {
    @Bean
    public RestTemplate restTemplate(RestTemplateBuilder restTemplateBuilder) {
        return restTemplateBuilder
           //.setConnectTimeout(Duration.ofSeconds(2))
           .setReadTimeout(Duration.ofSeconds(2))
           .build();
    }
}
