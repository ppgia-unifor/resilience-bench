using System;
using System.Diagnostics;
using System.Net.Http;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using Polly;
using ResiliencePatterns.Polly.Models;

namespace ResiliencePatterns.Polly
{
    public class BackendService
    {
        private readonly IHttpClientFactory _clientFactory;
        private readonly ILogger<BackendService> _logger;

        public BackendService(IHttpClientFactory clientFactory, ILogger<BackendService> logger)
        {
            _clientFactory = clientFactory;
            HttpClient = _clientFactory.CreateClient("backend");
            _logger = logger;
            _logger.LogInformation("http client created point to {baseAddress}", HttpClient.BaseAddress);
        }

        public HttpClient HttpClient { get; }

        /// <summary>
        /// Makes sequential requests to the backend service 
        /// </summary>
        /// <returns>A list of metrics. Each metric represents each try to do a succesful request</returns>
        public async Task<ResilienceModuleMetrics> MakeRequestAsync<T>(AsyncPolicy policy, Config<T> config) where T : class
        {
            var successfulCalls = 0;
            var totalCalls = 0;
            var metrics = new ResilienceModuleMetrics();

            var externalStopwatch = new Stopwatch();
            var requestStopwatch = new Stopwatch();
            externalStopwatch.Start();

            while (successfulCalls < config.SuccessfulRequests && config.MaxRequests > metrics.TotalRequests)
            {
                var policyResult = await policy.ExecuteAndCaptureAsync(async () =>
                {
                    try
                    {
                        requestStopwatch.Reset();
                        requestStopwatch.Start();
                        var result = await HttpClient.SendAsync(new HttpRequestMessage(HttpMethod.Get, config.TargetUrl));
                        requestStopwatch.Stop();
                        if (result.IsSuccessStatusCode)
                        {
                            metrics.RegisterSuccess(requestStopwatch.ElapsedMilliseconds);
                            return result;
                        }
                        else
                        {
                            throw new HttpRequestException();
                        }                        
                    }
                    catch (Exception)
                    {
                        if (requestStopwatch.IsRunning) 
                        {
                            requestStopwatch.Stop();
                        }
                        metrics.RegisterError(requestStopwatch.ElapsedMilliseconds);
                        throw;
                    }

                });
                if (policyResult.Outcome == OutcomeType.Successful)
                {
                    successfulCalls++;
                }
                totalCalls++;
                _logger.LogInformation("TotalCalls: {totalCalls} TotalRequests: {metrics.TotalRequests} SuccessfulRequests: {metrics.SuccessfulRequests}", totalCalls, metrics.TotalRequests, metrics.SuccessfulRequests);
            }
            externalStopwatch.Stop();
            metrics.RegisterTotals(totalCalls, successfulCalls, externalStopwatch.ElapsedMilliseconds);
            return metrics;
        }
    }
}
