import winston from 'winston';

// Define log levels
const logLevels = {
  error: 0,
  warn: 1,
  info: 2,
  debug: 3,
};

// Configure Winston logger
const logger = winston.createLogger({
  level: 'debug', // Minimum log level to display
  format: winston.format.combine(
    winston.format.colorize(), // Add colors to logs
    winston.format.timestamp(), // Add timestamps to logs
    winston.format.printf(({ timestamp, level, message }) => {
      return `${timestamp} [${level.toUpperCase()}]: ${message}`;
    })
  ),
  transports: [
    new winston.transports.Console(), // Output logs to the console
  ],
});

export default logger;
