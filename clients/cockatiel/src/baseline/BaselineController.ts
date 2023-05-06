import { Request, Response, Router } from 'express';
import bodyParser from "body-parser";
import { Config } from "../Config";
import { NoopPolicy, IPolicy } from "cockatiel";
import BackendService from '../BackendService';

const routerBaseline: Router = Router();

routerBaseline.use(bodyParser.json());

const backendService: BackendService = new BackendService();

function handleRequest(req: Request): Config {
  const body = req.body;
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

routerBaseline.post('/baseline/', (req: Request, res: Response) => {

  const config: Config = handleRequest(req)
  const policy: IPolicy = new NoopPolicy();

  const result = backendService.makeRequest(config, policy);

  res.send(result);
});

export default routerBaseline
