import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Vite 配置：React 插件（编译 JSX）+ 开发代理
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    // 开发代理：前端代码请求 /api/* 时，Vite 转发到后端 :8001（8000 被 Docker 占用）
    // 作用：前端写相对路径即可，绕开浏览器 CORS 限制
    proxy: {
      "/api": "http://127.0.0.1:8001",
    },
  },
});
