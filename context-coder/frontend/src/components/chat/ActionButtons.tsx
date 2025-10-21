import { useState } from 'react';
import { useSessionStore } from '@/stores/session';
import { apiClient } from '@/api/client';
import { Button } from '@/components/ui/button';
import { FileText, AlertTriangle, Shield, GitBranch, Download } from 'lucide-react';

export default function ActionButtons() {
  const { sessionId, isComplete } = useSessionStore();
  const [isExporting, setIsExporting] = useState(false);
  
  const handleCommand = async (command: string) => {
    if (!sessionId) return;
    
    try {
      await apiClient.executeCommand(sessionId, command);
      // Idealmente, o resultado seria exibido em um modal
      alert(`Comando ${command} executado com sucesso!`);
    } catch (error) {
      console.error('Command error:', error);
      alert('Erro ao executar comando');
    }
  };
  
  const handleExport = async () => {
    if (!sessionId || !isComplete) return;
    
    setIsExporting(true);
    try {
      const blob = await apiClient.exportMarkdown(sessionId, 'Feature Specification');
      
      // Download file
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'specification.md';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      
      alert('Especificação exportada com sucesso!');
    } catch (error) {
      console.error('Export error:', error);
      alert('Erro ao exportar especificação');
    } finally {
      setIsExporting(false);
    }
  };
  
  if (!isComplete) {
    return (
      <div className="text-center text-sm text-muted-foreground p-4">
        Continue a conversa para completar a especificação (mínimo 80%)
      </div>
    );
  }
  
  return (
    <div className="p-4 border-t space-y-3">
      <p className="text-sm font-medium text-center mb-3">
        ✅ Especificação completa! Ações adicionais:
      </p>
      
      <div className="grid grid-cols-2 gap-2">
        <Button
          variant="outline"
          size="sm"
          onClick={() => handleCommand('analyze_tech_debt')}
        >
          <AlertTriangle className="w-4 h-4 mr-2" />
          Tech Debt
        </Button>
        
        <Button
          variant="outline"
          size="sm"
          onClick={() => handleCommand('check_security')}
        >
          <Shield className="w-4 h-4 mr-2" />
          Segurança
        </Button>
        
        <Button
          variant="outline"
          size="sm"
          onClick={() => handleCommand('generate_diagram')}
        >
          <GitBranch className="w-4 h-4 mr-2" />
          Diagrama
        </Button>
        
        <Button
          variant="outline"
          size="sm"
          onClick={() => handleCommand('detect_multi_spec')}
        >
          <FileText className="w-4 h-4 mr-2" />
          Multi-Spec
        </Button>
      </div>
      
      <Button
        className="w-full"
        onClick={handleExport}
        disabled={isExporting}
      >
        <Download className="w-4 h-4 mr-2" />
        {isExporting ? 'Exportando...' : 'Exportar Markdown'}
      </Button>
    </div>
  );
}


