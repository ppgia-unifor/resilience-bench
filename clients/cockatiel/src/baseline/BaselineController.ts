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
  config.maxRequests = body.maxRequests;
  config.successfulRequests = body.successfulRequests;
  config.targetUrl = body.targetUrl;
  return config;
}

routerBaseline.post('/baseline/', (req: Request, res: Response) => {
  const config: Config = handleRequest(req);
  const policy: IPolicy = new NoopPolicy();
  const result = backendService.makeRequest(config, policy);
  result.then(prom => {
    res.json(prom)
  }).catch( _ =>{
    res.sendStatus(500)
  })
});

export default routerBaseline
