import { defineConfig } from "vite";
import viteReact from "@vitejs/plugin-react";
import eslint from "vite-plugin-eslint";
import EnvironmentPlugin from "vite-plugin-environment";
import { TanStackRouterVite } from "@tanstack/router-plugin/vite";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    viteReact(),
    eslint(),
    EnvironmentPlugin(["BACKEND_API_URL"]),
    TanStackRouterVite(),
  ],
});
