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
        private readonly Client _client;

        public CircuitBreakerController(Client client)
        {
            _client = client;
        }

        [HttpPost]
        public async Task<List<ClientMetrics>> IndexAsync(Config<CircuitBreakerConfig> circuitBreakerConfig)
        {
            var cb = CreateCircuitBreakerSimplePolicy(circuitBreakerConfig.Params);
            return await _client.SpawnAsync(cb, circuitBreakerConfig);
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
