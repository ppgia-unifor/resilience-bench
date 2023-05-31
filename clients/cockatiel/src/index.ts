import express, { Express } from 'express';
import routerBaseline from './baseline/BaselineController';
import routerRetry from './pattern/retry/RetryController';
import routerCircuitBreaker from './pattern/circuitBreaker/CircuitBreakerController';

const app: Express = express();
const port = process.env.PORT || 80;

app.use('/', routerBaseline);
app.use('/', routerRetry);
app.use('/', routerCircuitBreaker);

app.listen(port, () => {
  console.log(`Server is running at https://localhost:${port}`);
});
