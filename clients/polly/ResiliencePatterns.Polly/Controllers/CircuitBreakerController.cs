using System;
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
        private BackendService backendService = new BackendService();

        [HttpPost]
        public async Task<Metrics> IndexAsync(CircuitBreakerConfig circuitBreakerConfig)
        {
            var cb = CreateCircuitBreakerSimplePolicy(circuitBreakerConfig);
            var result = await backendService.MakeRequestAsync(cb);
            return result;
        }

        private AsyncPolicy CreateCircuitBreakerSimplePolicy(CircuitBreakerConfig circuitBreakerConfig)
        {
            return Policy
                .Handle<Exception>()
                .CircuitBreakerAsync(
                    exceptionsAllowedBeforeBreaking: circuitBreakerConfig.ExceptionsAllowedBeforeBreaking,
                    durationOfBreak: TimeSpan.FromMilliseconds(circuitBreakerConfig.DurationOfBreaking));
        }
    }
}
