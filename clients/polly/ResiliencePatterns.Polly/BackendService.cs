using System;
using System.Diagnostics;
using System.Net.Http;
using System.Threading.Tasks;
using Polly;

namespace ResiliencePatterns.Polly
{
    public class BackendService
    {
        private static HttpClient httpClient;

        public static HttpClient HttpClient
        {
            get
            {
                if (httpClient == null)
                {
                    lock (httpClient)
                    {
                        httpClient = new HttpClient();
                        httpClient.BaseAddress = new Uri("https://httpbin.org");
                    }
                }
                return httpClient;
            }
        }

        public async Task<Metrics> MakeRequestAsync(AsyncPolicy policy)
        {
            var maxRequestsAllowed = 4;
            var targetSuccessfulRequests = 25;
            var metrics = new Metrics();
            var externalStopwatch = new Stopwatch();
            externalStopwatch.Start();

            while (metrics.SuccessfulRequest < targetSuccessfulRequests && maxRequestsAllowed > metrics.TotalRequests)
            {
                var internalStopwatch = new Stopwatch();
                internalStopwatch.Start();

                var policyResult = await policy.ExecuteAndCaptureAsync(async () =>
                {
                    var result = await HttpClient.SendAsync(new HttpRequestMessage(HttpMethod.Get, "/status/500"));
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

            externalStopwatch.Stop();
            metrics.TotalTime = externalStopwatch.ElapsedMilliseconds;

            return metrics;
        }
    }
}
