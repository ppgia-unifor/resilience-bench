using System;
using System.Collections.Generic;
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
        private readonly Client _client;

        public RetryController(Client client)
        {
            _client = client;
        }

        [HttpPost]
        public async Task<IEnumerable<ClientMetrics>> IndexAsync(Config<RetryConfig> retryConfig)
        {
            var retry = CreateRetryExponencialBackoff(retryConfig.Params);
            return await _client.SpawnAsync(retry, retryConfig);
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
