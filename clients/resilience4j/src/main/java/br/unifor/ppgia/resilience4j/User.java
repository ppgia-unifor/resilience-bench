package br.unifor.ppgia.resilience4j;

import java.util.List;
import java.util.stream.LongStream;

import static java.util.stream.Collectors.toList;

public class User {

    public List<ResilienceModuleMetrics> spawnAsync(BackendServiceTemplate backendService, Config<?> config) {
        return LongStream
                .rangeClosed(1, config.getConcurrentUsers())
                .boxed()
                .parallel()
                .map((i) -> backendService.doHttpRequest(i, config))
                .collect(toList());
    }
}
