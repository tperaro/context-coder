import { useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'

export default function HomePage() {
  const navigate = useNavigate()

  const startNewSession = () => {
    const sessionId = `session-${Date.now()}`
    navigate(`/session/${sessionId}`)
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
      <Card className="max-w-2xl w-full mx-4 p-8">
        <div className="text-center space-y-6">
          <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-purple-600">
            Context2Task
          </h1>
          <p className="text-xl text-muted-foreground">
            Transforme contexto de repositórios em tasks acionáveis com IA
          </p>
          <div className="flex flex-col gap-4 max-w-md mx-auto">
            <Button 
              size="lg" 
              onClick={startNewSession}
              className="w-full"
            >
              🚀 Criar Nova Especificação
            </Button>
            <p className="text-sm text-muted-foreground">
              Plataforma AI-powered que analisa seu código e gera especificações técnicas completas
            </p>
          </div>
        </div>
      </Card>
    </div>
  )
}


