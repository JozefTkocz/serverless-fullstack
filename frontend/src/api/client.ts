import axios, { AxiosRequestConfig, AxiosInstance } from "axios";

class ApiClient {
  url: string;
  client: AxiosInstance;

  constructor() {
    this.url = process.env.BACKEND_API_URL || "";
    this.client = axios.create({
      baseURL: this.url,
    });
    // this.client.defaults.headers.common["Authorization"] =
    //   `Bearer ${localStorage.getItem("access_token")}`;
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

  async login(email: string, passCode: string): Promise<boolean> {
    const result = await this.client.post("/auth/login", {
      email: email,
      otp: passCode,
    });
    console.log(result.data);
    return result.data;
  }

  async check() {
    const result = await this.client.get("/auth/check-login");
    console.log(result);
  }
}

export const apiClient = new ApiClient();
