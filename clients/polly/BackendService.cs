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
            var totStarts = 0;
            var totSuccessStops = 0;
            var totFailStops = 0;
            var metrics = new ResilienceModuleMetrics();

            var externalStopwatch = new Stopwatch();
            var requestStopwatch = new Stopwatch();
            PolicyResult<System.Net.Http.HttpResponseMessage> policyResult = null;
            externalStopwatch.Start();
            while (successfulCalls < targetSuccessfulRequests && maxRequestsAllowed > metrics.TotalRequests)
            {
                try
                {
                    policyResult = await policy.ExecuteAndCaptureAsync(async () =>
                    {
                        requestStopwatch.Reset();
                        requestStopwatch.Start();
                        totStarts++;
                        _logger.LogInformation("requestWatch started");
                        var result = await HttpClient.SendAsync(new HttpRequestMessage(HttpMethod.Get, _resource));
                        requestStopwatch.Stop();
                        totSuccessStops++;
                        _logger.LogInformation("requestWatch stopped - success");
                        if (result.IsSuccessStatusCode)
                        {
                            metrics.RegisterSuccess(requestStopwatch.ElapsedMilliseconds);
                            return result;
                        }
                        else
                        {
                            throw new HttpRequestException();
                        }
                    });
                }
                catch (Exception e)// when ((e is HttpRequestException) || (e is TaskCanceledException))
                {
                    _logger.LogInformation("Exception {e}", e);
                    if (requestStopwatch.IsRunning) 
                    {
                        requestStopwatch.Stop();
                        totFailStops++;
                    }
                    _logger.LogInformation("requestWatch stopped - exception");
                    metrics.RegisterError(requestStopwatch.ElapsedMilliseconds);
                }
                //_logger.LogInformation("Policy result exception: {policyResult.FinalException}", policyResult.FinalException);
                if (policyResult.Outcome == OutcomeType.Successful)
                {
                    successfulCalls++;
                }
                else
                {
                    if (requestStopwatch.IsRunning) 
                    {
                        requestStopwatch.Stop();
                        totFailStops++;
                        _logger.LogInformation("requestWatch stopped - policyResult");
                        metrics.RegisterError(requestStopwatch.ElapsedMilliseconds);
                    }                 
                }
                totalCalls++;
            }
            externalStopwatch.Stop();
            _logger.LogInformation("TotStarts: {totStarts} TotSuccessStops: {totSuccessStops} TotFailStops: {totFailStops} TotStops: {totSuccessStops+totFailStops}", totStarts, totSuccessStops, totFailStops, totSuccessStops+totFailStops);
            metrics.RegisterTotals(totalCalls, successfulCalls, externalStopwatch.ElapsedMilliseconds);
            return metrics;
        }
    }
}
