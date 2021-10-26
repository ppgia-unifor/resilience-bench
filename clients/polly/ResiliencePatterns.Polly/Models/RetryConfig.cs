namespace ResiliencePatterns.Polly.Models
{
    public enum SleepDurationType
    {
        FIXED = 0,
        EXPONENTIAL_BACKOFF = 1
    }

    public class RetryConfig
    {
        public int Count { get; set; }
        public SleepDurationType SleepDurationType { get; set; }
        public int SleepDuration { get; set; }
        public float ExponentialBackoffPow { get; set; }
    }
}