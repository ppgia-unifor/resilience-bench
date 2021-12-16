namespace ResiliencePatterns.Polly
{
    public class ResilienceModuleMetrics
    {
        public int SuccessfulCalls { get; private set; }

        public int UnsuccessfulCalls { get; private set; }

        public int TotalCalls
        {
            get
            {
                return SuccessfulCalls + UnsuccessfulCalls;
            }
        }

        /// <summary>
        /// Total of successful requests
        /// </summary>
        public int SuccessfulRequests { get; private set; }

        /// <summary>
        /// Total of unsuccessful requests
        /// </summary>
        public int UnsuccessfulRequests { get; private set; }

        /// <summary>
        /// A sum of successful and unsuccessful requests
        /// </summary>
        public int TotalRequests
        {
            get
            {
                return UnsuccessfulRequests + SuccessfulRequests;
            }
        }

        /// <summary>
        /// Time spent in ms to get a successful response
        /// </summary>
        public long SuccessTime { get; private set; }

        public double SuccessTimePerRequest
        {
            get
            {
                if (SuccessfulRequests > 0)
                {
                    return SuccessTime / (double)SuccessfulRequests;
                }
                else
                {
                    return 0;
                }
            }
        }

        /// <summary>
        /// Time spent in ms to get a unsuccessful response
        /// </summary>
        public long ErrorTime { get; private set; }

        public double ErrorTimePerRequest
        {
            get
            {


                if (UnsuccessfulRequests > 0)
                {
                    return ErrorTime / (double)UnsuccessfulRequests;
                }
                else
                {
                    return 0;
                }
            }
        }

        /// <summary>
        /// Sum of success and error time
        /// </summary>
        public long TotalContentionTime
        {
            get
            {
                return SuccessTime + ErrorTime;
            }
        }

        public long TotalExecutionTime { get; private set; }

        public double Throughput
        {
            get
            {
                return TotalRequests / TotalExecutionTime;
            }
        }

        public void RegisterSuccess(long elapsedTime)
        {
            SuccessfulRequests++;
            SuccessTime += elapsedTime;
        }

        public void RegisterError(long elapsedTime)
        {
            UnsuccessfulRequests++;
            ErrorTime += elapsedTime;
        }

        public void RegisterTotals(int totalRequests, int successfulRequests, long totalExecutionTime)
        {
            SuccessfulCalls = successfulRequests;
            UnsuccessfulCalls = totalRequests - successfulRequests;
            TotalExecutionTime = totalExecutionTime;
        }
    }
}
