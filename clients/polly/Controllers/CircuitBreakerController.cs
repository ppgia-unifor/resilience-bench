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
    public class CircuitBreakerController : Controller
    {
        private readonly User _user;

        public CircuitBreakerController(User user)
        {
            _user = user;
        }

        [HttpPost]
        public async Task<IEnumerable<ResilienceModuleMetrics>> IndexAsync(Config<CircuitBreakerConfig> circuitBreakerConfig)
        {
            var cb = CreateCircuitBreakerSimplePolicy(circuitBreakerConfig.Params);
            return await _user.SpawnAsync(cb, circuitBreakerConfig);
        }

        private static AsyncPolicy CreateCircuitBreakerSimplePolicy(CircuitBreakerConfig circuitBreakerConfig)
        {
            return Policy
                .Handle<Exception>()
                .CircuitBreakerAsync(
                    exceptionsAllowedBeforeBreaking: circuitBreakerConfig.ExceptionsAllowedBeforeBreaking,
                    durationOfBreak: TimeSpan.FromMilliseconds(circuitBreakerConfig.DurationOfBreaking));
        }
    }
}
