import api from "./Api";

export const getComments = async (text: string, tone: string, observations: string) => {
    
    try {
        const response = await api.post('/comments', {
          text,
          tone,
          observations
      });
        return response.data.comment;
    } catch (error) {
        console.error('Error generating comment:', error);
        throw error;
    }
};

export const getContentByUrl = async (url: string) => {
    try {
        const data = {
            url
        };
        const response = await api.post(`/content`, data);
        return response.data.content;
    } catch (error) {
        console.error('Error generating content:', error);
        throw error;
    }
};