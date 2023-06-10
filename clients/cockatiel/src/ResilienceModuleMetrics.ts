export default class ResilienceModuleMetrics {
    private successfulCalls: number = 0;
    private unsuccessfulCalls: number = 0;
    private successfulRequests: number = 0;
    private unsuccessfulRequests: number = 0;
    private successTime: number = 0;
    private errorTime: number = 0;
    private totalExecutionTime: number = 0;

    public getSuccessfulCalls(): number {
        return this.successfulCalls;
    }

    public getUnsuccessfulCalls(): number {
        return this.unsuccessfulCalls;
    }

    public getTotalCalls(): number {
        return this.successfulCalls + this.unsuccessfulCalls;
    }

    public getSuccessfulRequests(): number {
        return this.successfulRequests;
    }

    public getUnsuccessfulRequests(): number {
        return this.unsuccessfulRequests;
    }

    public getTotalRequests(): number {
        return this.successfulRequests + this.unsuccessfulRequests;
    }

    public getSuccessTime(): number {
        return this.successTime;
    }

    public getSuccessTimePerRequest(): number {
        if (this.successfulRequests > 0) {
            return this.successTime / this.successfulRequests;
        } else {
            return 0;
        }
    }

    public getErrorTime(): number {
        return this.errorTime;
    }

    public getErrorTimePerRequest(): number {
        if (this.unsuccessfulRequests > 0) {
            return this.errorTime / this.unsuccessfulRequests;
        } else {
            return 0;
        }
    }

    public getTotalContentionTime(): number {
        return this.successTime + this.errorTime;
    }

    public getContentionRate(): number {
        if (this.totalExecutionTime > 0) {
            return this.getTotalContentionTime() / this.totalExecutionTime;
        } else {
            return 0;
        }
    }

    public getTotalExecutionTime(): number {
        return this.totalExecutionTime;
    }

    public getThroughput(): number {
        if (this.totalExecutionTime > 0) {
            return (1000 * this.getTotalRequests()) / this.totalExecutionTime;
        } else {
            return 0;
        }
    }

    public registerSuccess(elapsedTime: number): void {
        this.successfulRequests++;
        this.successTime += elapsedTime;
    }

    public registerError(elapsedTime: number): void {
        this.unsuccessfulRequests++;
        this.errorTime += elapsedTime;
    }

    public registerTotals(totalCalls: number, successfulCalls: number, totalExecutionTime: number): void {
        this.successfulCalls = successfulCalls;
        this.unsuccessfulCalls = totalCalls - successfulCalls;
        this.totalExecutionTime = totalExecutionTime;
    }

    public toJSON(): JSON {
        const metricsObject = {
            successfulCalls: this.successfulCalls,
            unsuccessfulCalls: this.unsuccessfulCalls,
            totalCalls: this.getTotalCalls(),
            successfulRequests: this.successfulRequests,
            unsuccessfulRequests: this.unsuccessfulRequests,
            totalRequests: this.getTotalRequests(),
            successTime: this.successTime,
            successTimePerRequest: this.getSuccessTimePerRequest(),
            errorTime: this.errorTime,
            errorTimePerRequest: this.getErrorTimePerRequest(),
            totalContentionTime: this.getTotalContentionTime(),
            contentionRate: this.getContentionRate(),
            totalExecutionTime: this.totalExecutionTime,
            throughput: this.getThroughput()
        };

        return JSON.parse(JSON.stringify(metricsObject));
    }
}

