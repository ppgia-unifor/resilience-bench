using System.Collections.Generic;
using System.Diagnostics;
using System.Threading.Tasks;
using System.Linq;
using Polly;
using ResiliencePatterns.Polly.Controllers;

namespace ResiliencePatterns.Polly
{
    public class Client
    {
        private readonly BackendService _backendService;

        public Client(BackendService backendService)
        {
            _backendService = backendService;
        }

        public async Task<List<ClientMetrics>> SpawnAsync<P>(AsyncPolicy policy, Config<P> config) where P : class
        {
            var stopwatch = new Stopwatch();
            stopwatch.Start();

            var tasks = new List<Task<ResilienceModuleMetrics>>();
            for (var i = 1; i <= config.ConcurrentClients; i++)
            {
                tasks.Add(_backendService.MakeRequestAsync(policy, i, config.TargetSuccessfulRequests, config.MaxRequestsAllowed));
            }

            var results = await Task.WhenAll(tasks);
            
            stopwatch.Stop();

            var clientMetricsList = new List<ClientMetrics>();
            var listResults = new List<ResilienceModuleMetrics>(results);
            var metricsByClient = listResults.GroupBy(r => r.ClientId);

            foreach (var result in metricsByClient)
            {
                clientMetricsList.Add(new ClientMetrics
                {
                    ClientId = result.Key,
                    ConcurrentClients = config.ConcurrentClients,
                    TotalTime = result.Sum(r => r.TotalTime),
                    TotalError = result.Sum(r => r.UnsuccessfulRequests),
                    TotalSuccess = result.Sum(r => r.SuccessfulRequest),
                    ResilienceModule = result.ToList(),
                });
            }

            return clientMetricsList;
        }
    }
}
