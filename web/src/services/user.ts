import { request } from "../utils/request";
import { BASE_URL } from '../constants/config';
import { ServiceReturnInterface } from "../interfaces/services/base";


export const USERS_ENDPOINTS = {
    activeUser: `${BASE_URL}users/active-user`,
    user: (user_id: string) => `${BASE_URL}users/${user_id}`,
};

class Users {
    async fetchCurrentUser(): Promise<ServiceReturnInterface> {
        return await request({
            url: USERS_ENDPOINTS.activeUser,
            method: "GET",
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
