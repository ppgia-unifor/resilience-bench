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
    public class CircuitBreakerController : Controller
    {
        private readonly BackendService _backendService;

        public CircuitBreakerController(BackendService backendService) 
        {
            _backendService = backendService;
        }

        [HttpPost]
        public async Task<ResilienceModuleMetrics> IndexAsync(Config<CircuitBreakerConfig> config)
        {
            var cb = CreateCircuitBreaker(config.PatternParams);
            var metrics = await _backendService.MakeRequestAsync(cb, config);
            return metrics;
        }

        private AsyncPolicy CreateCircuitBreaker(CircuitBreakerConfig circuitBreakerConfig)
        {
            var policy = Policy.Handle<HttpRequestException>().Or<TaskCanceledException>();
            if (circuitBreakerConfig.ExceptionsAllowedBeforeBreaking > 0)
            {
                return policy.CircuitBreakerAsync(
                    exceptionsAllowedBeforeBreaking: circuitBreakerConfig.ExceptionsAllowedBeforeBreaking,
                    durationOfBreak: TimeSpan.FromMilliseconds(circuitBreakerConfig.DurationOfBreak)
                );
            }
            return policy.AdvancedCircuitBreakerAsync(
                failureThreshold: circuitBreakerConfig.FailureThreshold,
                samplingDuration: TimeSpan.FromMilliseconds(circuitBreakerConfig.SamplingDuration),
                minimumThroughput: circuitBreakerConfig.MinimumThroughput,
                durationOfBreak: TimeSpan.FromMilliseconds(circuitBreakerConfig.DurationOfBreak)
            );
        }
    }
}
