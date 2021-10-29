namespace ResiliencePatterns.Polly
{
    public class Metrics
    {
        public int SuccessfulRequest { get; private set; }
        public int UnsuccessfulRequests { get; private set; }
        public int TotalRequests { get; private set; }
        public long SuccessTime { get; private set; }
        public long ErrorTime { get; private set; }

        public long TotalTime { get; set; }

        public void RegisterSuccess(long elapsedTime)
        {
            SuccessfulRequest++;
            TotalRequests++;
            SuccessTime += elapsedTime;
        }

        public void RegisterError(long elapsedTime)
        {
            UnsuccessfulRequests++;
            TotalRequests++;
            ErrorTime += elapsedTime;
        }
    }
}
