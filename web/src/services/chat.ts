import { request } from "../utils/request";
import { BASE_URL } from '../constants/config';
import { ServiceReturnInterface } from "../interfaces/services/base";


export const CHATS_ENDPOINTS = {
    get_or_create: (id: string) => `${BASE_URL}api/chats/${id}`,
};

class Chats {
    async getChat(chatId: string): Promise<ServiceReturnInterface> {
        return await request({
            url: CHATS_ENDPOINTS.get_or_create(chatId),
            method: "GET",
        });
    }

    async createChat(threadId: string, userMessage: string): Promise<ServiceReturnInterface> {
        return await request({
            url: CHATS_ENDPOINTS.get_or_create(threadId),
            method: "POST",
            body: { user_message: userMessage }
        });
    }
}

export const ChatsService = new Chats();
