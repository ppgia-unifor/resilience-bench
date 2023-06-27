import { Stopwatch } from "ts-stopwatch";
import { IPolicy } from "cockatiel";
import axios from "axios";
import { Config } from "./Config";
import ResilienceModuleMetrics from "./ResilienceModuleMetrics";

export default class BackendService {

  public async makeRequest(config: Config, policy: IPolicy): Promise<JSON> {
    let successfulCall: number = 0;
    let totalCall: number = 0;
    const metrics = new ResilienceModuleMetrics();

    const externalStopwatch = new Stopwatch();
    const requestStopwatch = new Stopwatch();

    let circuitOpenError: boolean = false;

    policy.onSuccess(() => {
      requestStopwatch.stop();
      metrics.registerSuccess(requestStopwatch.getTime());
    })

    policy.onFailure(() => {
      requestStopwatch.stop();
      metrics.registerError(requestStopwatch.getTime());
    })

    externalStopwatch.start();
    while (successfulCall < config.successfulRequests && config.maxRequests > metrics.getTotalRequests()) {
      circuitOpenError = false;
      requestStopwatch.reset();
      requestStopwatch.start();
      let res = await policy
        .execute(() => axios.get(config.targetUrl))
        .catch((err) => {
          if (err instanceof BrokenCircuitError) {
            circuitOpenError = true;
          }
        })

      if (res?.status == 200) {
        successfulCall++
      }

      if (!circuitOpenError) {
        totalCall++;
      }

    }

    externalStopwatch.stop();
    console.log("successfulCall: " + successfulCall + " unsuccessfulCall: " + (totalCall - successfulCall) + " successfulRequests: " + metrics.getSuccessfulRequests() + " unsuccessfulRequests: " + metrics.getUnsuccessfulRequests() + " time: " + externalStopwatch.getTime())
    metrics.registerTotals(successfulCall, totalCall, externalStopwatch.getTime());

    return metrics.toJSON();
  }
}
