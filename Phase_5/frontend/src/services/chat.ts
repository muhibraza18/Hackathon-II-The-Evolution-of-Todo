import { LOCAL_STORAGE_KEYS, ERROR_MESSAGES } from '../utils/constants';
import api from './api';

interface Message {
  id: string;
  content: string;
  sender: 'user' | 'assistant';
  timestamp: string;
  status: 'sent' | 'delivered' | 'error';
}

interface SendMessageResult {
  success: boolean;
  response?: string;
  conversationId?: number;
  toolCalls?: any[];
  error?: string;
}

interface FormatMessageParams {
  content: string;
  sender: 'user' | 'assistant';
  timestamp?: Date;
}

interface ChatService {
  sendMessage: (message: string, conversationId?: number | null) => Promise<SendMessageResult>;
  getCurrentConversationId: () => number | null;
  setCurrentConversationId: (conversationId: number) => void;
  clearCurrentConversationId: () => void;
  formatMessage: (content: string, sender: 'user' | 'assistant', timestamp?: Date) => Message;
}

/**
 * Chat service functions
 */
export const chatService: ChatService = {
  /**
   * Send a chat message
   */
  async sendMessage(message, conversationId = null) {
    try {
      const messageData = {
        message: message,
        conversation_id: conversationId
      };

      const response = await api.sendChatMessage(messageData);

      // Update conversation ID in local storage if it's new
      if (response.conversation_id && !conversationId) {
        localStorage.setItem(LOCAL_STORAGE_KEYS.CONVERSATION_ID, response.conversation_id.toString());
      }

      return {
        success: true,
        response: response.response,
        conversationId: response.conversation_id,
        toolCalls: response.tool_calls || []
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.message || ERROR_MESSAGES.SERVER_ERROR
      };
    }
  },

  /**
   * Get current conversation ID
   */
  getCurrentConversationId() {
    const storedId = localStorage.getItem(LOCAL_STORAGE_KEYS.CONVERSATION_ID);
    return storedId ? parseInt(storedId, 10) : null;
  },

  /**
   * Set current conversation ID
   */
  setCurrentConversationId(conversationId) {
    localStorage.setItem(LOCAL_STORAGE_KEYS.CONVERSATION_ID, conversationId.toString());
  },

  /**
   * Clear current conversation ID
   */
  clearCurrentConversationId() {
    localStorage.removeItem(LOCAL_STORAGE_KEYS.CONVERSATION_ID);
  },

  /**
   * Format message for display
   */
  formatMessage(content, sender, timestamp = new Date()) {
    return {
      id: Date.now().toString() + Math.random().toString(36).substr(2, 9), // Generate unique ID
      content,
      sender, // 'user' or 'assistant'
      timestamp: timestamp.toISOString(),
      status: 'sent' as const // 'sent', 'delivered', 'error'
    };
  }
};