import { Request, Response, Router } from 'express';
import bodyParser from "body-parser";
import { circuitBreaker, ConsecutiveBreaker, handleAll, IPolicy } from 'cockatiel';
import { Config } from '../../Config';
import BackendService from '../../BackendService';

const routerCircuitBreaker: Router = Router();

routerCircuitBreaker.use(bodyParser.json());

const backendService: BackendService = new BackendService();

function handleRequest(body: any): Config {
  const config = new Config();

  if (body.hasOwnProperty('maxRequests')) {
    config.maxRequests = body.maxRequests
  }

  if (body.hasOwnProperty('successfulRequests')) {
    config.successfulRequests = body.successfulRequests
  }

  if (body.hasOwnProperty('targetUrl')) {
    config.targetUrl = body.targetUrl
  }

  return config;
}

function createPolicy(patternConfig: any): IPolicy {

  return circuitBreaker(
    handleAll,
    {
      halfOpenAfter: patternConfig.halfOpenAfter,
      breaker: new ConsecutiveBreaker(patternConfig.exceptionsAllowedBeforeBreaking),
    }
  )

}

routerCircuitBreaker.post('/circuitbreaker/', (req: Request, res: Response) => {


  const body = req.body;

  const config: Config = handleRequest(body)

  const policy: IPolicy = createPolicy(body.patternParams);

  const result = backendService.makeRequest(config, policy);

  res.send(result);
});

export default routerCircuitBreaker
