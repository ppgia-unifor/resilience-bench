using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Polly;
using ResiliencePatterns.Polly.Models;

namespace ResiliencePatterns.Polly.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class BaselineController : Controller
    {
        private readonly BackendService _backendService;

        public BaselineController(BackendService backendService)
        {
            _backendService = backendService;
        }

        public async Task<ResilienceModuleMetrics> IndexAsync(Config<object> config)
        {
            return await _backendService.MakeRequestAsync(Policy.NoOpAsync(), config);
        }
    }
}
