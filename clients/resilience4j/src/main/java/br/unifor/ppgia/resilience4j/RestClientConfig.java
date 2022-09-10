package br.unifor.ppgia.resilience4j;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestTemplate;

import java.time.Duration;

@Configuration
public class RestClientConfig {
    private final static Logger logger = LoggerFactory.getLogger(RestClientConfig.class);

    @Value("${READ_TIMEOUT:0}")
    private Long readTimeout;

    @Bean
    public RestTemplate buildRestTemplate(RestTemplateBuilder restTemplateBuilder) {
        logger.info("Read timeout is {}.", readTimeout);
        if (readTimeout > 0) {
            restTemplateBuilder.setReadTimeout(Duration.ofMillis(readTimeout));
        }
        return restTemplateBuilder.build();
    }

    @Bean
    public RestClient buildRestClient(RestTemplate restTemplate) {
        return new RestClient(restTemplate);
    }
}
