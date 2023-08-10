import { Stopwatch } from "ts-stopwatch";
import { BrokenCircuitError, IPolicy } from "cockatiel";
import axios, { AxiosResponse } from "axios";
import { Config } from "./Config";
import ResilienceModuleMetrics from "./ResilienceModuleMetrics";
import { queue } from "async";

export default class BackendService {

  public async makeRequest(config: Config, policy: IPolicy): Promise<JSON> {
    let successfulCall: number = 0;
    let totalCall: number = 0;
    const metrics = new ResilienceModuleMetrics();

    const externalStopwatch = new Stopwatch();
    const requestStopwatch = new Stopwatch();

    let errorType: any;

    policy.onSuccess(() => {
      requestStopwatch.stop();
      metrics.registerSuccess(requestStopwatch.getTime());
    })

    policy.onFailure(() => {
      if (errorType != null && !(errorType instanceof BrokenCircuitError)) {
        requestStopwatch.stop();
        metrics.registerError(requestStopwatch.getTime());
      }
    })

    externalStopwatch.start();
    while (successfulCall < config.successfulRequests && config.maxRequests > metrics.getTotalRequests()) {
      requestStopwatch.reset();
      requestStopwatch.start();
      var q = queue(function(item, callback) {

        let res = policy
          .execute(() =>
            axios.get(config.targetUrl)
              .catch((err) => {
                errorType = err;
                throw err;
              }))
          .catch(() => { })


        res.then(() => {
          successfulCall++;
        })

      });

      q.drain();

      totalCall++;

    }

    externalStopwatch.stop();
    console.log("successfulCall: " + successfulCall + " unsuccessfulCall: " + (totalCall - successfulCall) + " successfulRequests: " + metrics.getSuccessfulRequests() + " unsuccessfulRequests: " + metrics.getUnsuccessfulRequests() + " time: " + externalStopwatch.getTime())
    metrics.registerTotals(successfulCall, totalCall, externalStopwatch.getTime());

    return metrics.toJSON();
  }
}
