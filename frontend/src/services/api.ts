import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export interface LoginRequest {
  username: string;
  password: string;
}

export interface SignupRequest {
  username: string;
  email: string;
  password: string;
}

export interface RecommendationRequest {
  age: number;
  location: string;
  skills: string[];
  interests: string[];
  language: string;
}

export interface CareerMatch {
  career: string;
  score: number;
  local_demand: string;
  description: string;
}

export interface RecommendationResponse {
  matches: CareerMatch[];
}

export const authAPI = {
  login: async (data: LoginRequest) => {
    const response = await api.post('/auth/login', data);
    return response.data;
  },
  
  signup: async (data: SignupRequest) => {
    const response = await api.post('/auth/signup', data);
    return response.data;
  },
  
  getMe: async () => {
    const response = await api.get('/auth/me');
    return response.data;
  }
};

export const recommendationAPI = {
  getRecommendations: async (data: RecommendationRequest): Promise<RecommendationResponse> => {
    const response = await api.post('/recommend', data);
    return response.data;
  }
};

export default api;
