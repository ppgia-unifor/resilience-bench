using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Polly;

namespace ResiliencePatterns.Polly.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class BaselineController : Controller
    {
        private readonly Client _client;

        public BaselineController(Client client)
        {
            _client = client;
        }

        public async Task<List<ClientMetrics>> IndexAsync(Config<object> config)
        {
            return await _client.SpawnAsync(Policy.NoOpAsync(), config.Users);
        }
    }
}
