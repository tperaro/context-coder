import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { FolderOpen, Plus, X, Search, RefreshCw, CheckCircle, Clock } from 'lucide-react';
import { apiClient, RepositoryInfo } from '@/api/client';

interface RepositorySelectorProps {
  selectedRepos: string[];
  onReposChange: (repos: string[]) => void;
}

export default function RepositorySelector({ selectedRepos, onReposChange }: RepositorySelectorProps) {
  const [isAdding, setIsAdding] = useState(false);
  const [newRepoPath, setNewRepoPath] = useState('');
  const [discoveredRepos, setDiscoveredRepos] = useState<RepositoryInfo[]>([]);
  const [isDiscovering, setIsDiscovering] = useState(false);
  const [isIndexing, setIsIndexing] = useState<string | null>(null);
  
  // Discover repositories on component mount
  useEffect(() => {
    discoverRepositories();
  }, []);
  
  const discoverRepositories = async () => {
    setIsDiscovering(true);
    try {
      const response = await apiClient.discoverRepositories();
      setDiscoveredRepos(response.repositories);
    } catch (error) {
      console.error('Error discovering repositories:', error);
    } finally {
      setIsDiscovering(false);
    }
  };
  
  const handleAdd = () => {
    if (newRepoPath.trim()) {
      onReposChange([...selectedRepos, newRepoPath.trim()]);
      setNewRepoPath('');
      setIsAdding(false);
    }
  };
  
  const handleRemove = (index: number) => {
    onReposChange(selectedRepos.filter((_, i) => i !== index));
  };
  
  const handleSelectRepo = (repo: RepositoryInfo) => {
    if (!selectedRepos.includes(repo.path)) {
      onReposChange([...selectedRepos, repo.path]);
    }
  };
  
  const handleIndexRepo = async (repo: RepositoryInfo) => {
    setIsIndexing(repo.path);
    try {
      await apiClient.indexRepository({ path: repo.path, force: false });
      // Refresh the repository list
      await discoverRepositories();
    } catch (error) {
      console.error('Error indexing repository:', error);
    } finally {
      setIsIndexing(null);
    }
  };
  
  return (
    <div className="p-4 border-b">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold">Repositórios</h3>
        <div className="flex gap-1">
          <Button
            variant="ghost"
            size="sm"
            onClick={discoverRepositories}
            disabled={isDiscovering}
            title="Descobrir repositórios"
          >
            <RefreshCw className={`w-4 h-4 ${isDiscovering ? 'animate-spin' : ''}`} />
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setIsAdding(!isAdding)}
            title="Adicionar manualmente"
          >
            <Plus className="w-4 h-4" />
          </Button>
        </div>
      </div>
      
      {/* Discovered Repositories */}
      {discoveredRepos.length > 0 && (
        <div className="mb-3">
          <p className="text-xs text-muted-foreground mb-2">
            Repositórios descobertos ({discoveredRepos.length})
          </p>
          <div className="space-y-1 max-h-32 overflow-y-auto">
            {discoveredRepos.map((repo) => (
              <div
                key={repo.path}
                className={`flex items-center gap-2 p-2 rounded text-xs border ${
                  selectedRepos.includes(repo.path)
                    ? 'bg-blue-50 border-blue-200 dark:bg-blue-900/20'
                    : 'bg-slate-50 border-slate-200 dark:bg-slate-800'
                }`}
              >
                <FolderOpen className="w-3 h-3 text-blue-600" />
                <div className="flex-1 min-w-0">
                  <div className="font-medium truncate" title={repo.path}>
                    {repo.name}
                  </div>
                  <div className="flex items-center gap-1 text-muted-foreground">
                    {repo.is_indexed ? (
                      <CheckCircle className="w-3 h-3 text-green-600" />
                    ) : (
                      <Clock className="w-3 h-3 text-orange-600" />
                    )}
                    <span className="text-xs">
                      {repo.is_indexed ? 'Indexado' : 'Não indexado'}
                    </span>
                    {repo.file_count && (
                      <span className="text-xs">({repo.file_count} arquivos)</span>
                    )}
                  </div>
                </div>
                <div className="flex gap-1">
                  {!repo.is_indexed && (
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => handleIndexRepo(repo)}
                      disabled={isIndexing === repo.path}
                      className="text-xs px-2 py-1 h-6"
                    >
                      {isIndexing === repo.path ? (
                        <RefreshCw className="w-3 h-3 animate-spin" />
                      ) : (
                        'Indexar'
                      )}
                    </Button>
                  )}
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={() => handleSelectRepo(repo)}
                    disabled={selectedRepos.includes(repo.path)}
                    className="text-xs px-2 py-1 h-6"
                  >
                    {selectedRepos.includes(repo.path) ? 'Selecionado' : 'Selecionar'}
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
      
      {/* Selected Repositories */}
      <div className="space-y-2">
        <p className="text-xs text-muted-foreground">
          Repositórios selecionados ({selectedRepos.length})
        </p>
        {selectedRepos.length === 0 && (
          <p className="text-xs text-muted-foreground">
            Nenhum repositório selecionado
          </p>
        )}
        
        {selectedRepos.map((repo, idx) => (
          <div
            key={idx}
            className="flex items-center gap-2 bg-slate-100 dark:bg-slate-800 rounded px-2 py-1 text-xs"
          >
            <FolderOpen className="w-3 h-3 text-blue-600" />
            <span className="flex-1 truncate" title={repo}>
              {repo.split('/').pop() || repo}
            </span>
            <button
              onClick={() => handleRemove(idx)}
              className="hover:text-red-600"
            >
              <X className="w-3 h-3" />
            </button>
          </div>
        ))}
      </div>
      
      {/* Add New Repository Manually */}
      {isAdding && (
        <div className="mt-3 space-y-2">
          <input
            type="text"
            value={newRepoPath}
            onChange={(e) => setNewRepoPath(e.target.value)}
            placeholder="/path/to/repository"
            className="w-full text-xs px-2 py-1 border rounded"
            onKeyDown={(e) => e.key === 'Enter' && handleAdd()}
          />
          <div className="flex gap-2">
            <Button size="sm" variant="outline" onClick={handleAdd} className="flex-1 text-xs">
              Adicionar
            </Button>
            <Button size="sm" variant="ghost" onClick={() => setIsAdding(false)} className="flex-1 text-xs">
              Cancelar
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}


