import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import NovelLearning from './pages/NovelLearning'
import ChatFlow from './pages/ChatFlow'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/learn" element={<NovelLearning />} />
        <Route path="/chat" element={<ChatFlow />} />
      </Routes>
    </Router>
  )
}

export default App
