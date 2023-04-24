import express, { Express } from 'express';
import dotenv from 'dotenv'
import routerBaseline from './baseline/BaselineController';
import routerRetry from './pattern/retry/RetryController';
import routerCircuitBreaker from './pattern/circuitBreaker/CircuitBreakerController';
dotenv.config();

const app: Express = express();
const port = process.env.PORT

app.use('/', routerBaseline);
app.use('/', routerRetry);
app.use('/', routerCircuitBreaker);


app.listen(port, () => {
  console.log(`⚡️[server]: Server is running at https://localhost:${port}`);
});
