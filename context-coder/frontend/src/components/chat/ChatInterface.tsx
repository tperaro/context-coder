import { useState, useRef, useEffect } from 'react';
import { useSessionStore } from '@/stores/session';
import { apiClient } from '@/api/client';
import { Button } from '@/components/ui/button';
import { Send, Loader2 } from 'lucide-react';
import VoiceInput from './VoiceInput';

export default function ChatInterface() {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  const {
    sessionId,
    messages,
    completionPercentage,
    isLoading,
    selectedRepositories,
    userProfile,
    addMessage,
    updateCompletion,
    setLoading
  } = useSessionStore();
  
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };
  
  useEffect(() => {
    scrollToBottom();
  }, [messages]);
  
  const handleSend = async () => {
    if (!input.trim() || !sessionId || isLoading) return;
    
    const userMessage = {
      role: 'user' as const,
      content: input.trim(),
      timestamp: new Date()
    };
    
    addMessage(userMessage);
    setInput('');
    setLoading(true);
    
    try {
      const response = await apiClient.chat(
        sessionId, 
        userMessage.content,
        undefined,
        selectedRepositories,
        userProfile
      );
      
      addMessage({
        role: 'assistant',
        content: response.ai_response,
        timestamp: new Date()
      });
      
      updateCompletion(response.completion_percentage, response.spec_sections);
    } catch (error) {
      console.error('Chat error:', error);
      addMessage({
        role: 'assistant',
        content: 'Desculpe, ocorreu um erro. Por favor, tente novamente.',
        timestamp: new Date()
      });
    } finally {
      setLoading(false);
    }
  };
  
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };
  
  return (
    <div className="flex flex-col h-full">
      {/* Progress Bar */}
      <div className="bg-slate-100 dark:bg-slate-800 p-3 border-b">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium">Progresso da Especificação</span>
          <span className="text-sm font-bold">{completionPercentage}%</span>
        </div>
        <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-2">
          <div
            className="bg-blue-600 h-2 rounded-full transition-all duration-500"
            style={{ width: `${completionPercentage}%` }}
          />
        </div>
      </div>
      
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-muted-foreground mt-10">
            <p className="text-lg mb-2">👋 Olá! Vamos criar uma especificação juntos.</p>
            <p className="text-sm">Descreva a feature que você quer desenvolver.</p>
          </div>
        )}
        
        {messages.map((message, idx) => (
          <div
            key={idx}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] rounded-lg px-4 py-2 ${
                message.role === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-slate-100'
              }`}
            >
              <p className="whitespace-pre-wrap">{message.content}</p>
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-slate-100 dark:bg-slate-800 rounded-lg px-4 py-2">
              <Loader2 className="w-5 h-5 animate-spin" />
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>
      
      {/* Input */}
      <div className="border-t bg-white dark:bg-slate-900 p-4">
        <div className="flex gap-2">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyPress}
            placeholder="Digite sua mensagem... (Shift+Enter para nova linha)"
            className="flex-1 resize-none rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows={3}
            disabled={isLoading}
          />
          <div className="flex flex-col gap-2">
            <VoiceInput onTranscript={(text) => setInput(input + ' ' + text)} />
            <Button
              onClick={handleSend}
              disabled={!input.trim() || isLoading}
              size="lg"
              className="px-6"
            >
              {isLoading ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <Send className="w-5 h-5" />
              )}
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}

