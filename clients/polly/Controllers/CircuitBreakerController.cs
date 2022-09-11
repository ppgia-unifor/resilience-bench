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
            var cb = CreateCircuitBreakerSimplePolicy(config.PatternParams);
            var metrics = await _backendService.MakeRequestAsync(cb, config);
            return metrics;
        }

        private static AsyncPolicy CreateCircuitBreakerSimplePolicy(CircuitBreakerConfig circuitBreakerConfig)
        {
            return Policy
                .Handle<HttpRequestException>()
                .Or<TaskCanceledException>()
                .CircuitBreakerAsync(
                    exceptionsAllowedBeforeBreaking: circuitBreakerConfig.ExceptionsAllowedBeforeBreaking,
                    durationOfBreak: TimeSpan.FromMilliseconds(circuitBreakerConfig.DurationOfBreaking));
        }
    }
}
