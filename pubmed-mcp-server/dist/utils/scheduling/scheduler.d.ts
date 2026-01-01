/**
 * @fileoverview Provides a singleton service for scheduling and managing cron jobs.
 * This service wraps the 'node-cron' library to offer a unified interface for
 * defining, starting, stopping, and listing recurring tasks within the application.
 * @module src/utils/scheduling/scheduler
 */
import { ScheduledTask } from "node-cron";
import { RequestContext } from "../internal/index.js";
/**
 * Represents a scheduled job managed by the SchedulerService.
 */
export interface Job {
    /** A unique identifier for the job. */
    id: string;
    /** The cron pattern defining the job's schedule. */
    schedule: string;
    /** A description of what the job does. */
    description: string;
    /** The underlying 'node-cron' task instance. */
    task: ScheduledTask;
    /** Indicates whether the job is currently running. */
    isRunning: boolean;
}
/**
 * A singleton service for scheduling and managing cron jobs.
 */
export declare class SchedulerService {
    private static instance;
    private jobs;
    /** @private */
    private constructor();
    /**
     * Gets the singleton instance of the SchedulerService.
     * @returns The singleton SchedulerService instance.
     */
    static getInstance(): SchedulerService;
    /**
     * Schedules a new job.
     *
     * @param id - A unique identifier for the job.
     * @param schedule - The cron pattern for the schedule (e.g., '* * * * *').
     * @param taskFunction - The function to execute on schedule. It receives a RequestContext.
     * @param description - A description of the job.
     * @returns The newly created Job object.
     */
    schedule(id: string, schedule: string, taskFunction: (context: RequestContext) => void | Promise<void>, description: string): Job;
    /**
     * Starts a scheduled job.
     * @param id - The ID of the job to start.
     */
    start(id: string): void;
    /**
     * Stops a scheduled job.
     * @param id - The ID of the job to stop.
     */
    stop(id: string): void;
    /**
     * Removes a job from the scheduler. The job is stopped before being removed.
     * @param id - The ID of the job to remove.
     */
    remove(id: string): void;
    /**
     * Gets a list of all scheduled jobs.
     * @returns An array of all Job objects.
     */
    listJobs(): Job[];
}
/**
 * The singleton instance of the SchedulerService.
 * Use this instance for all job scheduling operations.
 */
export declare const schedulerService: SchedulerService;
//# sourceMappingURL=scheduler.d.ts.map