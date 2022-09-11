namespace ResiliencePatterns.Polly.Models
{
    public class Config<P> where P : class
    {
        public int MaxRequests { get; set; }
        public int SuccessfulRequests { get; set; }

        public string TargetUrl { get; set; }

        public P PatternParams { get; set; }
    }
}
