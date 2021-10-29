using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Polly;

namespace ResiliencePatterns.Polly.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class BaselineController : Controller
    {
        private BackendService backendService = new BackendService();

        public async Task<Metrics> IndexAsync()
        {
            var result = await backendService.MakeRequestAsync(Policy.NoOpAsync());
            return result;
        }
    }
}
