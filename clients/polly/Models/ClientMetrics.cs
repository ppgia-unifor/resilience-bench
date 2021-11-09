using System;
using System.Collections.Generic;

namespace ResiliencePatterns.Polly
{
    public class ClientMetrics
    {
        public int ClientId { get; set; }
        public long TotalExecutionTime { get; set; }
        public int TotalSuccess { get; set; }
        public int TotalError { get; set; }
        public List<ResilienceModuleMetrics> ResilienceModule { get; set; }
    }
}
