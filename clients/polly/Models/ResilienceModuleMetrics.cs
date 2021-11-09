using System.Text.Json.Serialization;

namespace ResiliencePatterns.Polly
{
    public class ResilienceModuleMetrics
    {
        public ResilienceModuleMetrics(int userId)
        {
            UserId = userId;
        }

        public int UserId { get; }

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

        /// <summary>
        /// Time spent in ms to get a unsuccessful response
        /// </summary>
        public long ErrorTime { get; private set; }

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

        public long TotalExecutionTime { get; set; }

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
    }
}
