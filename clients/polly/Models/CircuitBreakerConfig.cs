namespace ResiliencePatterns.Polly.Models
{
    public class CircuitBreakerConfig
    {
        public int DurationOfBreak { get; set; }
        public int ExceptionsAllowedBeforeBreaking { get; set; }
        public bool IsSimpleConfiguration { get; set; }
        public double FailureThreshold { get; set; }
        public double SamplingDuration { get; set; }
        public int MinimumThroughput { get; set; }
    }
}
