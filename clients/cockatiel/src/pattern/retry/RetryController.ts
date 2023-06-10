import { Request, Response, Router } from 'express';
import bodyParser from "body-parser";
import { Config } from '../../Config';
import { ExponentialBackoff, handleAll, IPolicy, retry } from 'cockatiel';
import BackendService from '../../BackendService';

const routerRetry: Router = Router();

routerRetry.use(bodyParser.json());

const backendService: BackendService = new BackendService();

function handleRequest(body: any): Config {
  const config = new Config();
  config.maxRequests = body.maxRequests;
  config.successfulRequests = body.successfulRequests;
  config.targetUrl = body.targetUrl;
  return config;
}

function createPolicy(patternConfig: any): IPolicy {
  return retry(
    handleAll,
    {
      backoff: new ExponentialBackoff(
        {
          exponent: patternConfig.exponent,
          maxDelay: patternConfig.maxDelay,
          initialDelay: patternConfig.initialDelay,
        }),
      maxAttempts: patternConfig.maxAttempts
    });
}

routerRetry.post('/retry/', (req: Request, res: Response) => {
  const body = req.body;
  const config: Config = handleRequest(body);
  const policy: IPolicy = createPolicy(body.patternParams);
  const result = backendService.makeRequest(config, policy);
  result.then(prom => {
    res.json(prom)
  }).catch( _ =>{
    res.sendStatus(500)
  })
});
export default routerRetry;
