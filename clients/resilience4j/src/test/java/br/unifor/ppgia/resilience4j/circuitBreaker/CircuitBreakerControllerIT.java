package br.unifor.ppgia.resilience4j.circuitBreaker;

import br.unifor.ppgia.resilience4j.ClientResilience4jApplication;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.boot.web.server.LocalServerPort;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.test.context.junit.jupiter.SpringExtension;

import static org.junit.jupiter.api.Assertions.assertEquals;

@ExtendWith(SpringExtension.class)
@SpringBootTest(classes = ClientResilience4jApplication.class, webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class CircuitBreakerControllerIT {

  @LocalServerPort
  private int port;
  TestRestTemplate restTemplate = new TestRestTemplate();

  HttpHeaders headers = new HttpHeaders();

  @Test
  void sendAllParametersTest() {
    headers.add("Content-type", "application/json");
    var entity = new HttpEntity<>("{\n" +
        "  \"maxRequests\": 10,\n" +
        "  \"successfulRequests\": 10,\n" +
        "  \"targetUrl\": \"http://localhost:8080\",\n" +
        "  \"patternParams\": {\n" +
        "    \"failureRateThreshold\": 60,\n" +
        "    \"minimumNumberOfCalls\": 100,\n" +
        "    \"slidingWindowSize\": 10\n" +
        "  }\n" +
        "}", headers);
    var response = restTemplate.exchange(
        createURLWithPort("/cb"),
        HttpMethod.POST, entity, String.class);

    assertEquals(response.getStatusCode(), HttpStatus.OK);
  }

  private String createURLWithPort(String uri) {
    return "http://localhost:" + port + uri;
  }
}
