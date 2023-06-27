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
    const internalStopwatch = new Stopwatch();

    externalStopwatch.start();
    while (successfulCall < config.successfulRequests && config.maxRequests > metrics.getTotalRequests()) {
      internalStopwatch.reset();
      internalStopwatch.start();
      let res = await policy
        .execute(() => axios.get(config.targetUrl))
        .then(() => {
          internalStopwatch.stop();
          metrics.registerSuccess(internalStopwatch.getTime());

        })
        .catch(() => {
          internalStopwatch.stop();
          metrics.registerError(internalStopwatch.getTime());


        })

      if (res?.status == 200) {
        successfulCall++
      }

      totalCall++;

    }

    externalStopwatch.stop();
    console.log("successfulCall: " + successfulCall + " unsuccessfulCall: " + (totalCall - successfulCall) + " successfulRequests: " + metrics.getSuccessfulRequests() + " unsuccessfulRequests: " + metrics.getUnsuccessfulRequests() + " time: " + externalStopwatch.getTime())
    metrics.registerTotals(successfulCall, totalCall, externalStopwatch.getTime());

    return metrics.toJSON();
  }
}
