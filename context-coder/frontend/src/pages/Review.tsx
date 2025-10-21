import { useParams } from 'react-router-dom'

export default function ReviewPage() {
  const { sessionId } = useParams()

  return (
    <div className="min-h-screen bg-background">
      <div className="max-w-7xl mx-auto p-4">
        <h1 className="text-2xl font-bold mb-4">Review & Approval</h1>
        <p className="text-muted-foreground">Session ID: {sessionId}</p>
        <div className="mt-8">
          <p className="text-center text-muted-foreground">
            Review page será implementado posteriormente
          </p>
        </div>
      </div>
    </div>
  )
}


