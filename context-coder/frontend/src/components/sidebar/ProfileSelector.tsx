import { Button } from '@/components/ui/button';
import { User, Code } from 'lucide-react';

interface ProfileSelectorProps {
  profile: 'technical' | 'non_technical';
  onProfileChange: (profile: 'technical' | 'non_technical') => void;
}

export default function ProfileSelector({ profile, onProfileChange }: ProfileSelectorProps) {
  return (
    <div className="p-4 border-b">
      <h3 className="text-sm font-semibold mb-3">Perfil do Usuário</h3>
      
      <div className="grid grid-cols-2 gap-2">
        <Button
          variant={profile === 'technical' ? 'default' : 'outline'}
          size="sm"
          onClick={() => onProfileChange('technical')}
          className="text-xs"
        >
          <Code className="w-3 h-3 mr-1" />
          Técnico
        </Button>
        
        <Button
          variant={profile === 'non_technical' ? 'default' : 'outline'}
          size="sm"
          onClick={() => onProfileChange('non_technical')}
          className="text-xs"
        >
          <User className="w-3 h-3 mr-1" />
          Negócio
        </Button>
      </div>
      
      <p className="text-xs text-muted-foreground mt-2">
        {profile === 'technical' 
          ? 'Linguagem técnica, detalhes de implementação'
          : 'Linguagem simples, foco em valor de negócio'
        }
      </p>
    </div>
  );
}


