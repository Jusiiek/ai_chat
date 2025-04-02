import { request } from "../utils/request";
import { BASE_URL } from '../constants/config';
import { ServiceReturnInterface } from "../interfaces/services/base";


export const CHATS_ENDPOINTS = {
    get_or_create: (id: string) => `${BASE_URL}api/chats/${id}`,
};

class Chats {
    async getChat(chat_id: string): Promise<ServiceReturnInterface> {
        return await request({
            url: CHATS_ENDPOINTS.get_or_create(chat_id),
            method: "GET",
        });
    }
}

export const ChatsService = new Chats();
