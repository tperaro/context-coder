/**
 * API Client for Context2Task Backend
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

export interface ChatResponse {
  session_id: string;
  ai_response: string;
  completion_percentage: number;
  spec_sections: Record<string, string>;
  is_complete: boolean;
}

export interface SessionState {
  session_id: string;
  user_profile: string;
  selected_repositories: string[];
  completion_percentage: number;
  current_node?: string;
  iteration_count: number;
}

export interface RepositoryInfo {
  path: string;
  name: string;
  is_indexed: boolean;
  indexing_status?: string;
  file_count?: number;
  last_modified?: string;
}

export interface DiscoverRepositoriesResponse {
  repositories: RepositoryInfo[];
  total_found: number;
  indexed_count: number;
}

export interface IndexRepositoryRequest {
  path: string;
  force?: boolean;
}

export interface IndexRepositoryResponse {
  path: string;
  status: string;
  message: string;
  file_count?: number;
}

export const apiClient = {
  async chat(
    sessionId: string, 
    message: string, 
    command?: string,
    selectedRepositories?: string[],
    userProfile: string = 'technical'
  ): Promise<ChatResponse> {
    const response = await fetch(`${API_BASE_URL}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_id: sessionId,
        message,
        command,
        selected_repositories: selectedRepositories,
        user_profile: userProfile
      })
    });
    
    if (!response.ok) {
      throw new Error(`API error: ${response.statusText}`);
    }
    
    return response.json();
  },
  
  async getSessionState(sessionId: string): Promise<SessionState> {
    const response = await fetch(`${API_BASE_URL}/api/session/${sessionId}/state`);
    
    if (!response.ok) {
      throw new Error(`API error: ${response.statusText}`);
    }
    
    return response.json();
  },
  
  async executeCommand(sessionId: string, command: string): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/api/command/${sessionId}/${command}`, {
      method: 'POST'
    });
    
    if (!response.ok) {
      throw new Error(`API error: ${response.statusText}`);
    }
    
    return response.json();
  },
  
  async exportMarkdown(sessionId: string, featureTitle: string): Promise<Blob> {
    const response = await fetch(`${API_BASE_URL}/api/export/spec`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_id: sessionId,
        feature_title: featureTitle,
        format: 'markdown'
      })
    });
    
    if (!response.ok) {
      throw new Error(`Export error: ${response.statusText}`);
    }
    
    return response.blob();
  },
  
  async validateSpec(sessionId: string): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/api/export/validate/${sessionId}`);
    
    if (!response.ok) {
      throw new Error(`Validation error: ${response.statusText}`);
    }
    
    return response.json();
  },

  // Repository discovery and management
  async discoverRepositories(): Promise<DiscoverRepositoriesResponse> {
    const response = await fetch(`${API_BASE_URL}/api/repositories/discover`);
    
    if (!response.ok) {
      throw new Error(`Repository discovery error: ${response.statusText}`);
    }
    
    return response.json();
  },

  async getAvailableRepositories(): Promise<RepositoryInfo[]> {
    const response = await fetch(`${API_BASE_URL}/api/repositories/available`);
    
    if (!response.ok) {
      throw new Error(`Get available repositories error: ${response.statusText}`);
    }
    
    return response.json();
  },

  async indexRepository(request: IndexRepositoryRequest): Promise<IndexRepositoryResponse> {
    const response = await fetch(`${API_BASE_URL}/api/repositories/index`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request)
    });
    
    if (!response.ok) {
      throw new Error(`Index repository error: ${response.statusText}`);
    }
    
    return response.json();
  },

  async getRepositoryStatus(path: string): Promise<any> {
    const encodedPath = encodeURIComponent(path);
    const response = await fetch(`${API_BASE_URL}/api/repositories/status/${encodedPath}`);
    
    if (!response.ok) {
      throw new Error(`Get repository status error: ${response.statusText}`);
    }
    
    return response.json();
  }
};


