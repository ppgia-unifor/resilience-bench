package br.unifor.ppgia.resilience4j.baseline;

import br.unifor.ppgia.resilience4j.BackendServiceTemplate;
import io.vavr.CheckedFunction0;
import org.springframework.http.ResponseEntity;
import org.springframework.web.client.RestTemplate;

public class BackendServiceSimple extends BackendServiceTemplate {

    public BackendServiceSimple(RestTemplate restTemplate, String host) {
        super(restTemplate, host);
    }

    @Override
    protected CheckedFunction0<ResponseEntity<String>> decorate(CheckedFunction0<ResponseEntity<String>> checkedFunction) {
        return checkedFunction;
    }
}
