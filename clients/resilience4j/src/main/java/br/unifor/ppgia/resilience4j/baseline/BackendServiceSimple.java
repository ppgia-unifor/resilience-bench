package br.unifor.ppgia.resilience4j.baseline;

import br.unifor.ppgia.resilience4j.BackendServiceTemplate;
import br.unifor.ppgia.resilience4j.RestClient;
import io.vavr.CheckedFunction0;
import org.springframework.http.ResponseEntity;

public class BackendServiceSimple extends BackendServiceTemplate {

    public BackendServiceSimple(RestClient restClient) {
        super(restClient);
    }

    @Override
    protected CheckedFunction0<ResponseEntity<String>> decorate(CheckedFunction0<ResponseEntity<String>> checkedFunction) {
        return checkedFunction;
    }
}
