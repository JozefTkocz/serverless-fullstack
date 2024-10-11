import axios, { AxiosRequestConfig, AxiosInstance } from "axios";

class ApiClient {
  url: string;
  client: AxiosInstance;

  constructor() {
    this.url = process.env.BACKEND_API_URL;
    this.client = axios.create({
      baseURL: this.url,
    });
  }

  async post(data?: object, config?: AxiosRequestConfig) {
    return await this.client.post(this.url, data, config);
  }

  async requestOtp(email: string) {
    return await this.post({ email: email });
  }
}

export const apiClient = new ApiClient();
