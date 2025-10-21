/**
 * Session State Management with Zustand
 */
import { create } from 'zustand';

export interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface SessionStore {
  sessionId: string | null;
  messages: Message[];
  completionPercentage: number;
  specSections: Record<string, string>;
  isComplete: boolean;
  isLoading: boolean;
  selectedRepositories: string[];
  userProfile: 'technical' | 'non_technical';
  
  // Actions
  setSessionId: (id: string) => void;
  addMessage: (message: Message) => void;
  updateCompletion: (percentage: number, sections: Record<string, string>) => void;
  setLoading: (loading: boolean) => void;
  setRepositories: (repos: string[]) => void;
  setUserProfile: (profile: 'technical' | 'non_technical') => void;
  reset: () => void;
}

export const useSessionStore = create<SessionStore>((set) => ({
  sessionId: null,
  messages: [],
  completionPercentage: 0,
  specSections: {},
  isComplete: false,
  isLoading: false,
  selectedRepositories: [],
  userProfile: 'technical',
  
  setSessionId: (id) => set({ sessionId: id }),
  
  addMessage: (message) => set((state) => ({
    messages: [...state.messages, message]
  })),
  
  updateCompletion: (percentage, sections) => set({
    completionPercentage: percentage,
    specSections: sections,
    isComplete: percentage >= 80
  }),
  
  setLoading: (loading) => set({ isLoading: loading }),
  
  setRepositories: (repos) => set({ selectedRepositories: repos }),
  
  setUserProfile: (profile) => set({ userProfile: profile }),
  
  reset: () => set({
    sessionId: null,
    messages: [],
    completionPercentage: 0,
    specSections: {},
    isComplete: false,
    isLoading: false,
    selectedRepositories: [],
    userProfile: 'technical'
  })
}));


