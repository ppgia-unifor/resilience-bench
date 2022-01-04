using System;
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
        private readonly BackendService _backendService;

        public RetryController(BackendService backendService)
        {
            _backendService = backendService;
        }

        [HttpPost]
        public async Task<ResilienceModuleMetrics> IndexAsync(Config<RetryConfig> config)
        {
            var retry = CreateRetryExponencialBackoff(config.Params);
            var metrics = await _backendService.MakeRequestAsync(retry, config.TargetSuccessfulRequests, config.MaxRequestsAllowed);
            return metrics;
        }

        private static AsyncPolicy CreateRetryExponencialBackoff(RetryConfig retryConfig)
        {
            return Policy
                // .Handle<HttpRequestException>()
                .Handle<Exception>()
                .WaitAndRetryAsync(
                    retryCount: retryConfig.Count,
                    sleepDurationProvider: (retryNumber) =>
                        TimeSpan.FromMilliseconds(Math.Pow(retryConfig.ExponentialBackoffPow, retryNumber) * retryConfig.SleepDuration)
                );
        }
    }
}
