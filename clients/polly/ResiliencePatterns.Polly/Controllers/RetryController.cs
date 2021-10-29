using System;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Polly;
using ResiliencePatterns.Polly.Models;

namespace ResiliencePatterns.Polly.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class RetryController : Controller
    {
        private BackendService backendService = new BackendService();

        [HttpPost]
        public async Task<Metrics> IndexAsync(RetryConfig retryConfig)
        {
            var retry = CreateRetryExponencialBackoff(retryConfig);
            var result = await backendService.MakeRequestAsync(retry);
            return result;
        }

        private AsyncPolicy CreateRetryExponencialBackoff(RetryConfig retryConfig)
        {
            return Policy
                .Handle<Exception>()
                .WaitAndRetryAsync(
                    retryCount: retryConfig.Count,
                    sleepDurationProvider: (i) =>
                        TimeSpan.FromMilliseconds(Math.Pow(retryConfig.ExponentialBackoffPow, i) * retryConfig.SleepDuration));
        }
    }
}
