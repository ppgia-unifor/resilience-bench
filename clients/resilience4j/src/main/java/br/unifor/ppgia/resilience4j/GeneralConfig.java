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
public class GeneralConfig {
    private final static Logger logger = LoggerFactory.getLogger(GeneralConfig.class);

    @Value("${READ_TIMEOUT:0}")
    private Long readTimeout;

    @Value("${BACKEND_HOST:http://localhost:9211}")
    private String host;

    @Value("${RESOURCE_PATH:/status/200}")
    private String resource;

    @Bean
    public RestTemplate buildRestTemplate(RestTemplateBuilder restTemplateBuilder) {
        logger.info("Read timeout is {}.", readTimeout);
        logger.info("Root uri is {}.", host);
        logger.info("Resource is {}.", resource);
        return restTemplateBuilder.setReadTimeout(Duration.ofMillis(readTimeout)).rootUri(host).build();
    }

    @Bean
    public RestClient buildRestClient(RestTemplate restTemplate) {
        return new RestClient(restTemplate, resource);
    }
}
