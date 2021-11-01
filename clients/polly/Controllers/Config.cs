namespace ResiliencePatterns.Polly.Controllers
{
    public class Config<P>
    {
        public int Users { get; set; }
        public P Params { get; set; }
    }
}
