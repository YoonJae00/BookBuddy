import axios from 'axios';

const baseURL = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  }
});

export const apiService = {
  getNovels: () => api.get('/novels'),
  createNovel: (data: any) => api.post('/novels/', data),
  sendMessage: (characterId: string, message: string, userId: string = "anonymous") => 
    api.post(`/chat/${characterId}`, { content: message, user_id: userId }),
  getCharacters: (novelId: string) => 
    api.get(`/novels/${novelId}/characters`),
  getChatHistory: (characterId: string) => 
    api.get(`/chat/history/${characterId}`),
};