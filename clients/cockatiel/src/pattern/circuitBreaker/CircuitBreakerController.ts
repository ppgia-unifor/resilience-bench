import { Request, Response, Router } from 'express';
import bodyParser from "body-parser";
import { circuitBreaker, ConsecutiveBreaker, handleAll, IPolicy, SamplingBreaker } from 'cockatiel';
import { Config } from '../../Config';
import BackendService from '../../BackendService';

const routerCircuitBreaker: Router = Router();

routerCircuitBreaker.use(bodyParser.json());

function handleRequest(body: any): Config {
  const config = new Config();
  config.maxRequests = body.maxRequests;
  config.successfulRequests = body.successfulRequests;
  config.targetUrl = body.targetUrl;
  return config;
}

function createPolicyConsecutive(patternConfig: any): IPolicy {
  return circuitBreaker(
    handleAll,
    {
      halfOpenAfter: patternConfig.halfOpenAfter,
      breaker: new ConsecutiveBreaker(patternConfig.exceptionsAllowedBeforeBreaking),
    }
  );
}

function createPolicySampling(patternConfig: any): IPolicy {
  return circuitBreaker(
    handleAll,
    {
      halfOpenAfter: patternConfig.halfOpenAfter,
      breaker: new SamplingBreaker({
        threshold: patternConfig.threshold,
        duration: patternConfig.duration,
        minimumRps: patternConfig.minimumRps
      }),
    }
  );
}

routerCircuitBreaker.post('/circuitbreaker/consecutive/', async (req: Request, res: Response) => {
  try {

    const body = req.body;
    const config: Config = handleRequest(body);
    const policy: IPolicy = createPolicyConsecutive(body.patternParams);
    const backendService = new BackendService();
    const result = await backendService.makeRequest(config, policy);

    res.send(result);
  } catch (error: any) {
    res.status(500).send({ error: error.message || 'Internal Server Error' });
  }
});


routerCircuitBreaker.post('/circuitbreaker/sampling/', async (req: Request, res: Response) => {
  try {

    const body = req.body;
    const config: Config = handleRequest(body);
    const policy: IPolicy = createPolicySampling(body.patternParams);
    const backendService = new BackendService();
    const result = await backendService.makeRequest(config, policy);

    res.send(result);
  } catch (error: any) {
    res.status(500).send({ error: error.message || 'Internal Server Error' });
  }
});


export default routerCircuitBreaker
