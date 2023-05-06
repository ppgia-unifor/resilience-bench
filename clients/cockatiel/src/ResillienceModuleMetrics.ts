export class ResillienceModuleMetrics {
  private successfulCalls: number = 0;
  private unsuccessfulCalls: number = 0;
  private successfulRequests: number = 0;
  private unsuccessfulRequests: number = 0;
  private successTime: number = 0;
  private errorTime: number = 0;
  private totalExecutionTime: number = 0;

  constructor() { }

  getSuccessfulCalls(): number {
    return this.successfulCalls;
  }

  getUnsuccessfulCalls(): number {
    return this.unsuccessfulCalls;
  }

  getTotalCalls(): number {
    return this.getSuccessfulCalls() + this.getUnsuccessfulCalls();
  }

  getSuccessfulRequests(): number {
    return this.successfulRequests;
  }

  getUnsuccessfulRequests(): number {
    return this.unsuccessfulRequests;
  }

  getSuccessTime(): number {
    return this.successTime;
  }

  getSuccessTimePerRequest(): number {
    if (this.successfulRequests > 0) {
      return this.successTime / this.successfulRequests;
    } else {
      return 0;
    }
  }

  getErrorTime(): number {
    return this.errorTime;
  }

  getErrorTimePerRequest(): number {
    if (this.unsuccessfulRequests > 0) {
      return this.errorTime / this.unsuccessfulRequests;
    } else {
      return 0;
    }
  }

  getThroughput(): number {
    if (this.totalExecutionTime > 0) {
      return (1000 * this.getTotalRequests()) / this.totalExecutionTime;
    } else {
      return 0;
    }
  }

  getTotalExecutionTime(): number {
    return this.totalExecutionTime;
  }

  getTotalContentionTime(): number {
    return this.successTime + this.errorTime;
  }

  getContentionRate(): number {
    if (this.totalExecutionTime > 0) {
      return this.getTotalContentionTime() / this.totalExecutionTime;
    } else {
      return 0;
    }
  }

  getTotalRequests(): number {
    return this.successfulRequests + this.unsuccessfulRequests;
  }

  registerSuccess(elapsedTime: number): void {
    this.successfulRequests++;
    this.successTime += elapsedTime;
  }

  registerError(elapsedTime: number): void {
    this.unsuccessfulRequests++;
    this.errorTime += elapsedTime;
  }

  registerTotals(totalCalls: number, successfulCalls: number, totalExecutionTime: number): void {
    this.successfulCalls = successfulCalls;
    this.unsuccessfulCalls = totalCalls - this.successfulCalls;
    this.totalExecutionTime = totalExecutionTime;
  }
}
