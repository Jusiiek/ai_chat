import { request } from "../utils/request";
import { BASE_URL } from "../constants/config";

type TaskStatus = 'PENDING' | 'STARTED' | 'SUCCESS' | 'FAILURE';

interface TaskOptions {
  interval?: number;
  maxRetries?: number;
}

export class Task {
  private taskId: string;
  private interval: number;
  private maxRetries: number;
  private currentRetries: number = 0;
  private isPolling: boolean = false;
  private abortController: AbortController;

  public onSuccess: (result: any) => void = () => {};
  public onFailure: (error: any) => void = () => {};

  constructor(taskId: string, options: TaskOptions = {}) {
      this.taskId = taskId;
      this.interval = options.interval || 1000;
      this.maxRetries = options.maxRetries || 5;
      this.abortController = new AbortController();
  }

  start(): void {
      if (this.isPolling) return;

      this.isPolling = true;
      this.poll();
  }

  stop(): void {
      this.isPolling = false;
      this.abortController.abort();
      this.abortController = new AbortController();
  }

  private async getTaskResult(chat_id: string): Promise<Response> {
        const { res } = await request({
            url: `${BASE_URL}api/tasks/${chat_id}`,
            method: "GET",
        });
        return res
    }

  private async poll(): Promise<void> {
      if (!this.isPolling) return;

      try {
          const response = await this.getTaskResult(this.taskId)

      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

      const data = await response.json() as {
          status: TaskStatus;
          result?: any;
          error?: string;
      };

      switch (data.status) {
          case 'SUCCESS':
              this.onSuccess(data.result);
              this.stop();
              break;

          case 'FAILURE':
              this.onFailure(data.error || 'Task failed');
              this.stop();
              break;

          default:
              setTimeout(() => this.poll(), this.interval);
              break;
      }
    } catch (error) {
          if (this.currentRetries < this.maxRetries) {
              this.currentRetries++;
              setTimeout(() => this.poll(), this.interval);
          } else {
              this.onFailure(error);
              this.stop();
          }
      }
  }
  async waitForCompletion(): Promise<any> {
      return new Promise((resolve, reject) => {
          this.onSuccess = resolve;
          this.onFailure = reject;
          this.start();
      });
  }
}
