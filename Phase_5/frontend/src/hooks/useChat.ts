import { useState, useCallback, useEffect, useRef } from 'react';
import api from '../services/api';
import { daprState } from '../services/daprState';
import { useAuth } from '../contexts/AuthProvider';

interface Message {
  id: string;
  content: string;
  sender: 'user' | 'assistant';
  timestamp: string;
  status: 'sent' | 'delivered' | 'error';
}

interface ChatHistory {
  messages: Message[];
  conversationId: number | null;
  updatedAt: string;
}

const CHAT_HISTORY_KEY = 'history';

export const useChat = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [isInitialized, setIsInitialized] = useState(false);
  const { user } = useAuth();
  const retryQueueRef = useRef<string[]>([]);

  // Load chat history on mount
  useEffect(() => {
    const loadChatHistory = async () => {
      if (!user) {
        setIsInitialized(true);
        return;
      }

      try {
        const historyKey = `${user.id}-${CHAT_HISTORY_KEY}`;
        const history = await daprState.get<ChatHistory>(historyKey);

        if (history) {
          // Only restore messages, NOT the conversationId - always start fresh
          // This prevents using stale conversation IDs that no longer exist
          setMessages(history.messages || []);
          setConversationId(null); // Always start with null (new conversation)
          console.log(`✅ Chat history loaded: ${history.messages?.length || 0} messages (starting fresh conversation)`);
        }
      } catch (err) {
        console.error('Failed to load chat history:', err);
      } finally {
        setIsInitialized(true);
      }
    };

    loadChatHistory();
  }, [user]);

  // Save chat history whenever messages change
  useEffect(() => {
    if (!isInitialized || !user) return;

    const saveChatHistory = async () => {
      try {
        const historyKey = `${user.id}-${CHAT_HISTORY_KEY}`;
        const history: ChatHistory = {
          messages,
          conversationId,
          updatedAt: new Date().toISOString(),
        };
        await daprState.set(historyKey, history);
      } catch (err) {
        console.error('Failed to save chat history:', err);
      }
    };

    // Debounce saves to avoid excessive writes
    const timeoutId = setTimeout(saveChatHistory, 500);
    return () => clearTimeout(timeoutId);
  }, [messages, conversationId, isInitialized, user]);

  const sendMessage = useCallback(async (content: string, skipConversationIdCheck = false) => {
    if (!content.trim()) return;

    // Add user message immediately
    const userMessage: Message = {
      id: Date.now().toString(),
      content,
      sender: 'user',
      timestamp: new Date().toISOString(),
      status: 'sent',
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      // Send message to backend with token
      // Use null conversation_id if this is a retry after conversation not found
      const effectiveConversationId = skipConversationIdCheck ? null : conversationId;

      const response = await api.sendChatMessage({
        message: content,
        conversation_id: effectiveConversationId,
      });

      // Update conversation ID if this is the first message
      if (effectiveConversationId === null && response.conversation_id) {
        setConversationId(response.conversation_id);
      }

      // Add assistant response
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: response.response,
        sender: 'assistant',
        timestamp: new Date().toISOString(),
        status: 'delivered',
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err: any) {
      console.error('Chat error:', err);
      const errorMessage = err.message || 'Failed to send message';

      // Check if error is about conversation not found AND we haven't already retried
      if (errorMessage.includes('Conversation') && errorMessage.includes('not found') && conversationId && !skipConversationIdCheck) {
        console.log('♻️ Conversation not found, resetting and retrying with new conversation...');

        // Remove the user message that failed
        setMessages((prev) => prev.filter(msg => msg.id !== userMessage.id));

        // Reset conversation ID and retry immediately with skipConversationIdCheck=true
        setConversationId(null);

        // Use setTimeout to ensure state update is processed
        setTimeout(() => {
          sendMessage(content, true); // Pass true to skip using the old conversation ID
        }, 50);
        return;
      }

      setError(errorMessage);

      // Mark user message as error
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === userMessage.id ? { ...msg, status: 'error' as const } : msg
        )
      );
    } finally {
      setIsLoading(false);
    }
  }, [conversationId]);

  const clearChat = useCallback(async () => {
    setMessages([]);
    setConversationId(null);
    setError(null);

    // Also clear from persistent storage
    if (user) {
      try {
        const historyKey = `${user.id}-${CHAT_HISTORY_KEY}`;
        await daprState.delete(historyKey);
      } catch (err) {
        console.error('Failed to clear chat history:', err);
      }
    }
  }, [user]);

  return {
    messages,
    isLoading,
    error,
    sendMessage,
    clearChat,
    isInitialized,
  };
};
