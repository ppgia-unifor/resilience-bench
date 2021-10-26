using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using ResiliencePatterns.Polly.Models;

namespace ResiliencePatterns.Polly.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class BaselineController : Controller
    {
        private BackendService backendService = new BackendService();

        public async Task<MetricStatus> IndexAsync()
        {
            await backendService.MakeRequest();
            return new MetricStatus();
        }
    }
}
