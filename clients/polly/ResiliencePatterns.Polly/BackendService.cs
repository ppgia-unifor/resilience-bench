using System;
using System.Diagnostics;
using System.Net.Http;
using System.Threading.Tasks;

namespace ResiliencePatterns.Polly
{
    public class BackendService
    {
        public BackendService()
        {
        }

        public async Task<HttpResponseMessage> MakeRequest()
        {
            try
            {
                //var stopWatch = new Stopwatch();
                //stopWatch.Start();

                //HttpResponseMessage result = null;
                // result = await ResponseViaTCP(urlConfiguration);
                var httpClient = new HttpClient();
                httpClient.BaseAddress = new Uri("https://httpbin.org");
                var result = await httpClient.SendAsync(new HttpRequestMessage(HttpMethod.Get, "/status/500"));

                //stopWatch.Stop();

                if (result.IsSuccessStatusCode)
                {
                    //_metrics.IncrementeResilienceModuleSuccess();
                    //_metrics.IncrementeResilienceModuleSuccessTime(stopWatch.ElapsedMilliseconds);
                }
                else
                {
                    //_metrics.IncrementeResilienceModuleErrorTime(stopWatch.ElapsedMilliseconds);
                }

                if (!result.IsSuccessStatusCode)
                    throw new HttpRequestException();

                return result;
            }
            catch (Exception e)
            {
                Console.WriteLine(e);
                //_metrics.IncrementeResilienceModuleError();
                throw;
            }
        }
    }
}
