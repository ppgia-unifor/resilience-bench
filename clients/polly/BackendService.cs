using System;
using System.Diagnostics;
using System.Net.Http;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using Polly;

namespace ResiliencePatterns.Polly
{
    public class BackendService
    {
        private readonly IHttpClientFactory _clientFactory;
        private readonly ILogger<BackendService> _logger;

        private readonly string _resource;

        public BackendService(IHttpClientFactory clientFactory, ILogger<BackendService> logger)
        {
            _clientFactory = clientFactory;
            HttpClient = _clientFactory.CreateClient("backend");
            _resource = Environment.GetEnvironmentVariable("RESOURCE_PATH");
            _logger = logger;
            _logger.LogInformation("http client created point to {baseAddress}", HttpClient.BaseAddress);
        }

        public HttpClient HttpClient { get; }

        /// <summary>
        /// Makes sequential requests to the backend service 
        /// </summary>
        /// <param name="policy">Police to wrap the http call to the backend service</param>
        /// <param name="targetSuccessfulRequests">Amount of successful request that it should does</param>
        /// <param name="maxRequestsAllowed">Ceiling of requests to try to reach the number specified in {targetSuccessfulRequests}</param>
        /// <returns>A list of metrics. Each metric represents each try to do a succesful request</returns>
        public async Task<ResilienceModuleMetrics> MakeRequestAsync(AsyncPolicy policy, int targetSuccessfulRequests, int maxRequestsAllowed)
        {
            var successfulCalls = 0;
            var totalCalls = 0;
            var metrics = new ResilienceModuleMetrics();

            var externalStopwatch = new Stopwatch();
            externalStopwatch.Start();
            while (successfulRequests < targetSuccessfulRequests && maxRequestsAllowed > totalRequests)
            {
                var policyResult = await policy.ExecuteAndCaptureAsync(async () =>
                {
                    var requestStopwatch = new Stopwatch();
                    requestStopwatch.Start();
                    try
                    {
                        var result = await HttpClient.SendAsync(new HttpRequestMessage(HttpMethod.Get, _resource));
                        requestStopwatch.Stop();
                        if (result.IsSuccessStatusCode)
                        {
                            metrics.RegisterSuccess(requestStopwatch.ElapsedMilliseconds);
                            return result;
                        }
                        throw new HttpRequestException();
                    }
                    catch (HttpRequestException e)
                    {
                        requestStopwatch.Stop();
                        metrics.RegisterError(requestStopwatch.ElapsedMilliseconds);
                        throw new HttpRequestException();
                    }
                });
                if (policyResult.Outcome == OutcomeType.Successful)
                {
                    successfulCalls++;
                }
                totalCalls++;
            }
            externalStopwatch.Stop();
            metrics.RegisterTotals(totalCalls, successfulCalls, externalStopwatch.ElapsedMilliseconds);
            return metrics;
        }
    }
}
