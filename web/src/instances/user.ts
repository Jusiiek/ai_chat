import { TokenInterface, UserInterface } from "@/interfaces/instances/user";


class User {
  private user: UserInterface | null = null;
  private tokenData: TokenInterface | null = null;
  private userKey = "ai_chat_user";
  private tokenKey = "ai_chat_token";

  get() {
    if (this.user) {
      return this.user;
    }
    const savedUser = localStorage.getItem(this.userKey);
    if (savedUser) {
      this.user = JSON.parse(savedUser);
      if (this.user)
        this.set(this.user);
      return this.user;
    }
    const savedToken = localStorage.getItem(this.tokenKey);
    if (savedToken) {
      this.tokenData = JSON.parse(savedToken);
      if (this.tokenData)
        this.setToken(this.tokenData);
      return this.tokenData;
    }
  }

  set(userData: UserInterface) {
    localStorage.setItem(this.userKey, JSON.stringify(userData));
    this.user = userData;
  }

  setToken(tokenData: TokenInterface) {
    localStorage.setItem(this.tokenKey, JSON.stringify(tokenData));
    this.tokenData = tokenData
  }

  clear() {
    localStorage.removeItem(this.userKey);
    localStorage.removeItem(this.tokenKey);
    this.user = null;
    this.tokenData = null;
  }

  getToken() {
    this.get()
    return this.tokenData?.access_token;
  }

  getTokenType() {
    this.get()
    return this.tokenData?.token_type;
  }

  isSuperUser() {
    this.get();
    return this.user?.is_superuser;
  }
}

export const ActiveUser = new User();
