import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { authAPI, ApiError } from "../services/api";

export const useAuth = () => {
  // Инициализируем состояние сразу из localStorage
  const [isAuthenticated, setIsAuthenticated] = useState(() => {
    return !!localStorage.getItem("access_token");
  });
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const login = async (username: string, password: string) => {
    setLoading(true);
    try {
      const response = await authAPI.login(username, password);
      localStorage.setItem("access_token", response.data.access_token);
      setIsAuthenticated(true);
      navigate("/chat");
      return { success: true };
    } catch (error: unknown) {
      // Используем unknown вместо any
      const apiError = error as ApiError;
      return {
        success: false,
        error: apiError.response?.data?.detail || "Login failed",
      };
    } finally {
      setLoading(false);
    }
  };

  const register = async (username: string, email: string, password: string) => {
    setLoading(true);
    try {
      await authAPI.register(username, email, password);
      return await login(username, password);
    } catch (error: unknown) {
      const apiError = error as ApiError;
      return {
        success: false,
        error: apiError.response?.data?.detail || "Registration failed",
      };
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    setIsAuthenticated(false);
    navigate("/login");
  };

  return { isAuthenticated, loading, login, register, logout };
};
