using System.Text.Json.Serialization;

namespace ResiliencePatterns.Polly
{
    public class ResilienceModuleMetrics
    {
        public ResilienceModuleMetrics(int clientId)
        {
            ClientId = clientId;
        }

        [JsonIgnore]
        public int ClientId { get; }
        public int SuccessfulRequest { get; private set; }
        public int UnsuccessfulRequests { get; private set; }
        public int TotalRequests { get; private set; }
        public long SuccessTime { get; private set; }
        public long ErrorTime { get; private set; }
        public long TotalTime { get; private set; }
        [JsonIgnore]
        public bool Successful { get; private set; }

        public void RegisterSuccess(long elapsedTime)
        {
            SuccessfulRequest++;
            SuccessTime += elapsedTime;
            Successful = true;
            IncrementTotals(elapsedTime);
        }

        public void RegisterError(long elapsedTime)
        {
            UnsuccessfulRequests++;
            ErrorTime += elapsedTime;
            Successful = false;
            IncrementTotals(elapsedTime);
        }

        private void IncrementTotals(long elapsedTime)
        {
            TotalTime += elapsedTime;
            TotalRequests++;
        }
    }
}
