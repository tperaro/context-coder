import { BrowserRouter, Routes, Route } from 'react-router-dom'
import HomePage from './pages/Home'
import SessionPage from './pages/Session'
import ReviewPage from './pages/Review'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/session/:sessionId" element={<SessionPage />} />
        <Route path="/review/:sessionId" element={<ReviewPage />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App


