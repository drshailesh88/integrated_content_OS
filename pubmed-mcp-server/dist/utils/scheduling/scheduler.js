/**
 * @fileoverview Provides a singleton service for scheduling and managing cron jobs.
 * This service wraps the 'node-cron' library to offer a unified interface for
 * defining, starting, stopping, and listing recurring tasks within the application.
 * @module src/utils/scheduling/scheduler
 */
import cron, { createTask } from "node-cron";
import { logger } from "../internal/index.js";
import { requestContextService } from "../internal/requestContext.js";
/**
 * A singleton service for scheduling and managing cron jobs.
 */
export class SchedulerService {
    static instance;
    jobs = new Map();
    /** @private */
    constructor() {
        logger.info("SchedulerService initialized.", {
            requestId: "scheduler-init",
            timestamp: new Date().toISOString(),
        });
    }
    /**
     * Gets the singleton instance of the SchedulerService.
     * @returns The singleton SchedulerService instance.
     */
    static getInstance() {
        if (!SchedulerService.instance) {
            SchedulerService.instance = new SchedulerService();
        }
        return SchedulerService.instance;
    }
    /**
     * Schedules a new job.
     *
     * @param id - A unique identifier for the job.
     * @param schedule - The cron pattern for the schedule (e.g., '* * * * *').
     * @param taskFunction - The function to execute on schedule. It receives a RequestContext.
     * @param description - A description of the job.
     * @returns The newly created Job object.
     */
    schedule(id, schedule, taskFunction, description) {
        if (this.jobs.has(id)) {
            throw new Error(`Job with ID '${id}' already exists.`);
        }
        if (!cron.validate(schedule)) {
            throw new Error(`Invalid cron schedule: ${schedule}`);
        }
        const task = createTask(schedule, async () => {
            const job = this.jobs.get(id);
            if (job && job.isRunning) {
                logger.warning(`Job '${id}' is already running. Skipping this execution.`, {
                    requestId: `job-skip-${id}`,
                    timestamp: new Date().toISOString(),
                });
                return;
            }
            if (job) {
                job.isRunning = true;
            }
            const context = requestContextService.createRequestContext({
                jobId: id,
                schedule,
            });
            logger.info(`Starting job '${id}'...`, context);
            try {
                await Promise.resolve(taskFunction(context));
                logger.info(`Job '${id}' completed successfully.`, context);
            }
            catch (error) {
                logger.error(`Job '${id}' failed.`, error, context);
            }
            finally {
                if (job) {
                    job.isRunning = false;
                }
            }
        });
        const newJob = {
            id,
            schedule,
            description,
            task,
            isRunning: false,
        };
        this.jobs.set(id, newJob);
        logger.info(`Job '${id}' scheduled: ${description}`, {
            requestId: `job-schedule-${id}`,
            timestamp: new Date().toISOString(),
        });
        return newJob;
    }
    /**
     * Starts a scheduled job.
     * @param id - The ID of the job to start.
     */
    start(id) {
        const job = this.jobs.get(id);
        if (!job) {
            throw new Error(`Job with ID '${id}' not found.`);
        }
        job.task.start();
        logger.info(`Job '${id}' started.`, {
            requestId: `job-start-${id}`,
            timestamp: new Date().toISOString(),
        });
    }
    /**
     * Stops a scheduled job.
     * @param id - The ID of the job to stop.
     */
    stop(id) {
        const job = this.jobs.get(id);
        if (!job) {
            throw new Error(`Job with ID '${id}' not found.`);
        }
        job.task.stop();
        logger.info(`Job '${id}' stopped.`, {
            requestId: `job-stop-${id}`,
            timestamp: new Date().toISOString(),
        });
    }
    /**
     * Removes a job from the scheduler. The job is stopped before being removed.
     * @param id - The ID of the job to remove.
     */
    remove(id) {
        const job = this.jobs.get(id);
        if (!job) {
            throw new Error(`Job with ID '${id}' not found.`);
        }
        job.task.stop();
        this.jobs.delete(id);
        logger.info(`Job '${id}' removed.`, {
            requestId: `job-remove-${id}`,
            timestamp: new Date().toISOString(),
        });
    }
    /**
     * Gets a list of all scheduled jobs.
     * @returns An array of all Job objects.
     */
    listJobs() {
        return Array.from(this.jobs.values());
    }
}
/**
 * The singleton instance of the SchedulerService.
 * Use this instance for all job scheduling operations.
 */
export const schedulerService = SchedulerService.getInstance();
//# sourceMappingURL=scheduler.js.map