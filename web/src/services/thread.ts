import { request } from "../utils/request";
import { BASE_URL } from '../constants/config';
import { ServiceReturnInterface } from "../interfaces/services/base";


export const THREADS_ENDPOINTS = {
    list_or_create: `${BASE_URL}api/threads/`,
    thread: (thread_id: string) => `${BASE_URL}api/threads/${thread_id}`,
};

class Threads {
    async getThreadList(): Promise<ServiceReturnInterface> {
        return await request({
            url: THREADS_ENDPOINTS.list_or_create,
            method: "GET",
        });
    }

    async createThread(userMessage: string): Promise<ServiceReturnInterface> {
        return await request({
            url: THREADS_ENDPOINTS.list_or_create,
            method: "POST",
            body: { user_message: userMessage }
        });
    }
}

export const ThreadsService = new Threads();
