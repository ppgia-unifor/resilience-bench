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
        private readonly User _user;

        public BaselineController(User user)
        {
            _user = user;
        }

        public async Task<IEnumerable<ResilienceModuleMetrics>> IndexAsync(Config<object> config)
        {
            return await _user.SpawnAsync(Policy.NoOpAsync(), config);
        }
    }
}
