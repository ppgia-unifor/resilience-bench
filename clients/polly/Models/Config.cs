namespace ResiliencePatterns.Polly.Models
{
    public class Config<P> where P : class
    {
        public int MaxRequestsAllowed { get; set; }
        public int TargetSuccessfulRequests { get; set; }

        public string TargetUrl { get; set; }

        public P Params { get; set; }
    }
}
