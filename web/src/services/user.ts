import { request } from "../utils/request";
import { BASE_URL } from '../constants/config';
import { ServiceReturnInterface } from "../interfaces/services/base";
import { currentUserUpdate } from "../interfaces/services/user";


export const USERS_ENDPOINTS = {
    activeUser: `${BASE_URL}api/users/active-user`,
    user: (user_id: string) => `${BASE_URL}api/users/${user_id}`,
};

class Users {
    async fetchCurrentUser(): Promise<ServiceReturnInterface> {
        return await request({
            url: USERS_ENDPOINTS.activeUser,
            method: "GET",
        });
    }

    async updateCurrentUser(body: currentUserUpdate): Promise<ServiceReturnInterface> {
        return await request({
            url: USERS_ENDPOINTS.activeUser,
            method: "PUT",
            body
        });
    }

    async fetchUserData(user_id: string): Promise<ServiceReturnInterface> {
        return await request({
            url: USERS_ENDPOINTS.user(user_id),
            method: "GET",
        });
    }
}

export const UsersService = new Users();
