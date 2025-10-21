import { useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { useSessionStore } from '@/stores/session'
import ChatInterface from '@/components/chat/ChatInterface'
import ActionButtons from '@/components/chat/ActionButtons'
import RepositorySelector from '@/components/sidebar/RepositorySelector'
import ProfileSelector from '@/components/sidebar/ProfileSelector'

export default function SessionPage() {
  const { sessionId } = useParams()
  const { 
    setSessionId, 
    reset, 
    selectedRepositories,
    userProfile,
    setRepositories,
    setUserProfile: setStoreUserProfile
  } = useSessionStore()

  useEffect(() => {
    if (sessionId) {
      reset()
      setSessionId(sessionId)
    }
  }, [sessionId, setSessionId, reset])
  
  const handleReposChange = (repos: string[]) => {
    setRepositories(repos)
  }
  
  const handleProfileChange = (profile: 'technical' | 'non_technical') => {
    setStoreUserProfile(profile)
  }

  return (
    <div className="h-screen flex flex-col">
      <header className="bg-white dark:bg-slate-900 border-b px-6 py-4">
        <div className="flex items-center justify-between">
          <h1 className="text-xl font-bold">Context2Task</h1>
          <span className="text-sm text-muted-foreground">
            Session: {sessionId?.slice(0, 8)}...
          </span>
        </div>
      </header>
      
      <div className="flex-1 flex overflow-hidden">
        {/* Main Chat Area - 70% */}
        <div className="flex-1 flex flex-col">
          <ChatInterface />
        </div>
        
        {/* Sidebar - 30% */}
        <aside className="w-80 border-l bg-slate-50 dark:bg-slate-900 overflow-y-auto">
          <ProfileSelector 
            profile={userProfile}
            onProfileChange={handleProfileChange}
          />
          
          <RepositorySelector
            selectedRepos={selectedRepositories}
            onReposChange={handleReposChange}
          />
          
          <ActionButtons />
        </aside>
      </div>
    </div>
  )
}

