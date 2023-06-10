import { Stopwatch } from "ts-stopwatch";
import { IPolicy } from "cockatiel";
import axios from "axios";
import { Config } from "./Config";
import ResilienceModuleMetrics from "./ResilienceModuleMetrics";

export default class BackendService {

  public async makeRequest(config: Config, policy: IPolicy): Promise<JSON> {

    let successulCalls: number = 0;
    let totalCalls: number = 0;
    const metrics = new ResilienceModuleMetrics();

    const externalStopwatch = new Stopwatch();
    const requestStopwatch = new Stopwatch();

    policy.onSuccess(() => {
      successulCalls++;
    });

    externalStopwatch.start();
    while (successulCalls < config.successfulRequests && config.maxRequests > metrics.getTotalRequests()) {
      requestStopwatch.reset();
      requestStopwatch.start();
      await policy.execute(() => axios.get(config.targetUrl)
        .then(() => {
          requestStopwatch.stop();
          metrics.registerSuccess(requestStopwatch.getTime());
        })
        .catch(() => {
          requestStopwatch.stop();
          metrics.registerError(requestStopwatch.getTime());
        })
      );
      totalCalls++
    }

    externalStopwatch.stop();
    metrics.registerTotals(totalCalls, successulCalls, externalStopwatch.getTime());

    return metrics.toJSON();
  }
}
