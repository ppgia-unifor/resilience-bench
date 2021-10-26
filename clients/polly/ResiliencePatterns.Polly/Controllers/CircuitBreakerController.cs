using System;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Polly;
using Polly.CircuitBreaker;
using ResiliencePatterns.Polly.Models;

namespace ResiliencePatterns.Polly.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class CircuitBreakerController : Controller
    {
        private BackendService backendService = new BackendService();

        [HttpPost]
        public async Task<MetricStatus> IndexAsync(CircuitBreakerConfig circuitBreakerConfig)
        {
            var cb = CreateCircuitBreakerSimplePolicy(circuitBreakerConfig);
            await cb.ExecuteAndCaptureAsync(() => backendService.MakeRequest());
            return new MetricStatus();
        }

        private AsyncCircuitBreakerPolicy CreateCircuitBreakerSimplePolicy(CircuitBreakerConfig circuitBreakerConfig)
        {
            return Policy
                .Handle<Exception>()
                .CircuitBreakerAsync(
                    exceptionsAllowedBeforeBreaking: circuitBreakerConfig.ExceptionsAllowedBeforeBreaking,
                    durationOfBreak: TimeSpan.FromMilliseconds(circuitBreakerConfig.DurationOfBreaking),
                    onBreak: (exception, timeOfBreak) =>
                    {
                        //_metricService.CircuitBreakerMetric.IncrementBreakCount();
                        //_metricService.CircuitBreakerMetric.IncrementBreakTime((long)timeOfBreak.TotalMilliseconds);
                        Console.WriteLine($"\t[{DateTime.Now}] Break for [{timeOfBreak}]");
                    },
                    onReset: () => Console.WriteLine($"\tReseted"),
                    () => Console.WriteLine($"\t[{DateTime.Now}] HalfOpen"));
        }
    }
}
