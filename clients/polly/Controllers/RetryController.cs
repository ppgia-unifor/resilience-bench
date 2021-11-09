using System;
using System.Collections.Generic;
using System.Net.Http;
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
        private readonly User _user;

        public RetryController(User user)
        {
            _user = user;
        }

        [HttpPost]
        public async Task<IEnumerable<ResilienceModuleMetrics>> IndexAsync(Config<RetryConfig> retryConfig)
        {
            var retry = CreateRetryExponencialBackoff(retryConfig.Params);
            return await _user.SpawnAsync(retry, retryConfig);
        }

        private static AsyncPolicy CreateRetryExponencialBackoff(RetryConfig retryConfig)
        {
            return Policy
                .Handle<HttpRequestException>()
                .WaitAndRetryAsync(
                    retryCount: retryConfig.Count,
                    sleepDurationProvider: (retryNumber) =>
                        TimeSpan.FromMilliseconds(Math.Pow(retryConfig.ExponentialBackoffPow, retryNumber) * retryConfig.SleepDuration)
                );
        }
    }
}
