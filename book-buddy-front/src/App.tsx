import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import NovelList from './pages/NovelList'
import NovelLearning from './pages/NovelLearning'
import DebugDatabase from './pages/DebugDatabase'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/novels" element={<NovelList />} />
        <Route path="/learning" element={<NovelLearning />} />
        <Route path="/debug" element={<DebugDatabase />} />
      </Routes>
    </Router>
  )
}

export default App
