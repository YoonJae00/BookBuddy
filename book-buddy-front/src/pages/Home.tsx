import { Link } from 'react-router-dom'
import './Home.css'

function Home() {
  return (
    <div className="home">
      <h1>Book Buddy</h1>
      <div className="menu-grid">
        <Link to="/novels" className="menu-item">
          <h2>소설 목록</h2>
          <p>학습된 소설들을 확인하세요</p>
        </Link>
        <Link to="/learning" className="menu-item">
          <h2>소설 학습</h2>
          <p>새로운 소설을 학습시키세요</p>
        </Link>
        <Link to="/debug" className="menu-item debug">
          <h2>디버그</h2>
          <p>데이터베이스 내용 확인</p>
        </Link>
      </div>
    </div>
  )
}

export default Home