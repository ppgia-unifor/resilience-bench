using System;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Polly;
using Polly.Retry;
using ResiliencePatterns.Polly.Models;

namespace ResiliencePatterns.Polly.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class RetryController : Controller
    {
        private BackendService backendService = new BackendService();

        [HttpPost]
        public async Task<MetricStatus> IndexAsync(RetryConfig retryConfig)
        {
            var retry = CreateRetryExponencialBackoff(retryConfig);
            var result = await retry.ExecuteAndCaptureAsync(async () => await backendService.MakeRequest());

            return new MetricStatus();
        }

        private AsyncRetryPolicy CreateRetryExponencialBackoff(RetryConfig retryConfig)
        {
            return Policy
                .Handle<Exception>()
                .WaitAndRetryAsync(
                    retryCount: retryConfig.Count,
                    sleepDurationProvider: (i) =>
                        TimeSpan.FromMilliseconds(Math.Pow(retryConfig.ExponentialBackoffPow, i) * retryConfig.SleepDuration),
                    onRetry: (exception, timeout, context) =>
                    {
                        //_metricService.RetryMetric.IncrementRetryCount();
                        //_metricService.RetryMetric.IncrementRetryTotalTimeout((long)timeout.TotalMilliseconds);
                        Console.WriteLine($"\tNew timeout of [{timeout}]");
                    });
        }
    }
}
