import { Request, Response, Router } from 'express';
import bodyParser from "body-parser";
import { Config } from "../Config";
import { NoopPolicy, IPolicy } from "cockatiel";
import BackendService from '../BackendService';

const routerBaseline: Router = Router();

routerBaseline.use(bodyParser.json());

function handleRequest(body: any): Config {
  const config = new Config();
  config.maxRequests = body.maxRequests;
  config.successfulRequests = body.successfulRequests;
  config.targetUrl = body.targetUrl;
  return config;
}

routerBaseline.post('/baseline/', async (req: Request, res: Response) => {
  try {

    const body = req.body;
    const config: Config = handleRequest(body);
    const policy: IPolicy = new NoopPolicy();
    const backendService = new BackendService();
    const result = await backendService.makeRequest(config, policy);

    res.send(result);
  } catch (error: any) {
    res.status(500).send({ error: error.message || 'Internal Server Error' });
  }
});

export default routerBaseline
