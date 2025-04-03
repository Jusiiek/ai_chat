import {request} from "../utils/request";
import {BASE_URL} from '../constants/config';
import {AuthInterface} from "../interfaces/services/auth";
import {ServiceReturnInterface} from "../interfaces/services/base";
import {RequestResponse} from "../interfaces/utils/request";
import {ActiveUser} from "../instances/user";


export const AUTH_ENDPOINTS = {
    login: `${BASE_URL}auth/jwt/login`,
    logout: `${BASE_URL}auth/jwt/logout`,
    register: `${BASE_URL}auth/register`,
};

class Auth {
    async register(body: object): Promise<RequestResponse> {
        return await request({
            url: AUTH_ENDPOINTS.register,
            method: "POST",
            body,
        });
    }

    async login(body: AuthInterface): Promise<ServiceReturnInterface> {
        const {data, res} = await request({
            url: AUTH_ENDPOINTS.login,
            method: "POST",
            skipRedirect: true,
            body,
        });
        if (res.status === 200) {
            ActiveUser.setToken(data);
        }
        return {
            data,
            res,
        };
    }

    async logout(): Promise<RequestResponse> {
        return await request({
            url: AUTH_ENDPOINTS.logout,
            method: "POST"
        });
    }
}

export const AuthService = new Auth();
