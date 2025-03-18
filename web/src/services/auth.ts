import { request } from "@/utils/request";
import { BASE_URL } from '@/constants/config';
import { AuthInterface } from "@interfaces/services/auth.ts";
import { ServiceReturnInterface } from "@interfaces/services/base.ts";
import { RequestResponse } from "@interfaces/utils/request.ts";
import { ActiveUser } from "@instances/user.ts";


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
    const formData = new FormData();
    formData.append("password", body.password);
    formData.append("email", body.email);
    const { data, res } = await request({
      url: AUTH_ENDPOINTS.login,
      method: "POST",
      skipRedirect: true,
      formData,
    });
    if (res.status === 200) {
      ActiveUser.setToken(data);
    }
    return {
      data,
      res,
    };
  }

  async logout(token: string): Promise<RequestResponse>  {
    return await request({
      url: AUTH_ENDPOINTS.logout,
      method: "POST",
      body: {token: token}
    });
  }
}

export const AuthService = new Auth();
