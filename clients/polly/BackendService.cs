using System;
using System.Diagnostics;
using System.Net.Http;
using System.Threading.Tasks;
using Polly;

namespace ResiliencePatterns.Polly
{
    public class BackendService
    {
        private readonly IHttpClientFactory _clientFactory;

        public BackendService(IHttpClientFactory clientFactory)
        {
            _clientFactory = clientFactory;
            HttpClient = _clientFactory.CreateClient("backend");
        }

        public HttpClient HttpClient { get; }

        public async Task<ResilienceModuleMetrics> MakeRequestAsync(AsyncPolicy policy, int clientId)
        {
            var maxRequestsAllowed = 10;
            var targetSuccessfulRequests = 25;
            var metrics = new ResilienceModuleMetrics(clientId);
            Random rnd = new Random();

            while (metrics.SuccessfulRequest < targetSuccessfulRequests && maxRequestsAllowed > metrics.TotalRequests)
            {
                var internalStopwatch = new Stopwatch();
                internalStopwatch.Start();

                var policyResult = await policy.ExecuteAndCaptureAsync(async () =>
                {
                    var result = await HttpClient.SendAsync(new HttpRequestMessage(HttpMethod.Get, "/status/" + rnd.Next(2, 5) + "00"));
                    if (!result.IsSuccessStatusCode)
                    {
                        metrics.RegisterError(internalStopwatch.ElapsedMilliseconds);
                    }
                    return result;
                });

                internalStopwatch.Stop();

                if (policyResult.Outcome == OutcomeType.Successful)
                    metrics.RegisterSuccess(internalStopwatch.ElapsedMilliseconds);
            }
            return metrics;
        }
    }
}
