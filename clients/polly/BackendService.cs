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

        public async Task<ResilienceModuleMetrics> MakeRequestAsync(AsyncPolicy policy, int clientId, int targetSuccessfulRequests, int maxRequestsAllowed)
        {
            var metrics = new ResilienceModuleMetrics(clientId);

            while (metrics.SuccessfulRequest < targetSuccessfulRequests && maxRequestsAllowed > metrics.TotalRequests)
            {
                var internalStopwatch = new Stopwatch();
                internalStopwatch.Start();

                var policyResult = await policy.ExecuteAndCaptureAsync(async () =>
                {
                    var result = await HttpClient.SendAsync(new HttpRequestMessage(HttpMethod.Get, "/status/200"));
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
