package br.unifor.ppgia.resilience4j;

import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestTemplate;
import java.time.Duration;
import java.lang.Long;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


@Configuration
public class GeneralConfig {
    private final static Logger logger = LoggerFactory.getLogger(GeneralConfig.class);
    
    @Bean
    public RestTemplate restTemplate(RestTemplateBuilder restTemplateBuilder) {
        long readTimeout = 0;
        String readTimeoutEnv = System.getenv("READ_TIMEOUT");

        if (readTimeoutEnv != null && !readTimeoutEnv.isEmpty()) {
            try {
                readTimeout = Long.parseLong(readTimeoutEnv);
            }
            catch (NumberFormatException e) {
                logger.error("Invalid timeout value {}! Treating as zero", readTimeoutEnv);
            }
            
        }
        return restTemplateBuilder
           .setReadTimeout(Duration.ofMillis(readTimeout))
           .build();
    }
}
