using System.Collections.Generic;
using System.Threading.Tasks;
using Polly;
using ResiliencePatterns.Polly.Controllers;

namespace ResiliencePatterns.Polly
{
    public class User
    {
        private readonly BackendService _backendService;

        public User(BackendService backendService)
        {
            _backendService = backendService;
        }

        public async Task<IEnumerable<ResilienceModuleMetrics>> SpawnAsync<P>(AsyncPolicy policy, Config<P> config) where P : class
        {
            var tasks = new List<Task<ResilienceModuleMetrics>>();
            for (var userId = 1; userId <= config.ConcurrentUsers; userId++)
            {
                tasks.Add(_backendService.MakeRequestAsync(policy, userId, config.TargetSuccessfulRequests, config.MaxRequestsAllowed));
            }
            var metrics = await Task.WhenAll(tasks);
            return metrics;
        }
    }
}
