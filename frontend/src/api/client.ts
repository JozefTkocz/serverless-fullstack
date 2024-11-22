import axios, { AxiosRequestConfig, AxiosInstance } from "axios";
import { AUTH_TOKEN_KEY } from "../features/login";

type LoginResponse = {
  auth_token: string;
  session_token: { email: string; message: string };
};

class ApiClient {
  url: string;
  client: AxiosInstance;

  constructor() {
    this.url = process.env.BACKEND_API_URL || "";
    this.client = axios.create({
      baseURL: this.url,
    });
    this.setAuthToken();
  }

  setAuthToken() {
    this.client.defaults.headers.common["auth_token"] =
      window.localStorage.getItem(AUTH_TOKEN_KEY);
    console.log(window.localStorage.getItem(AUTH_TOKEN_KEY));
  }

  async healthCheck() {
    return await this.client.get("/");
  }

  async post(data?: object, config?: AxiosRequestConfig) {
    return await this.client.post(this.url, data, config);
  }

  async registerUser(email: string) {
    const _ = await this.client.post("/auth/register", { email: email });
  }

  async requestOtp(email: string) {
    const _ = await this.client.post("/auth/otp", { email: email });
  }

  async login(email: string, passCode: string): Promise<LoginResponse> {
    try {
      const result = await this.client.post("/auth/login", {
        email: email,
        otp: passCode,
      });
      return result.data;
    } catch {
      return {
        auth_token: "",
        session_token: { email: email, message: "Failed to login!" },
      };
    }
  }

  async checkLogin(): Promise<boolean> {
    this.setAuthToken();
    const result = await this.client.get("/auth/check-login", {
      headers: { auth_token: window.localStorage.getItem(AUTH_TOKEN_KEY) },
    });
    console.log(result);
    return result.data;
  }
}

export const apiClient = new ApiClient();
