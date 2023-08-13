import { Request, Response, Router } from 'express';
import bodyParser from "body-parser";
import { Config } from '../../Config';
import { ExponentialBackoff, handleAll, IPolicy, retry } from 'cockatiel';
import BackendService from '../../BackendService';

const routerRetry: Router = Router();

routerRetry.use(bodyParser.json());

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

routerRetry.post('/retry/', async (req: Request, res: Response) => {
  try {

    const body = req.body;
    const config: Config = handleRequest(body);
    const policy: IPolicy = createPolicy(body.patternParams);
    const backendService = new BackendService();
    const result = await backendService.makeRequest(config, policy);

    res.send(result);
  } catch (error: any) {
    res.status(500).send({ error: error.message || 'Internal Server Error' });
  }
});
export default routerRetry;
