import { useNavigate } from 'react-router-dom'
import './Home.css'

function Home() {
  const navigate = useNavigate()

  return (
    <div className="home-container">
      <div className="content">
        <h1 className="title">Book Buddy</h1>
        <button 
          className="button button-primary"
          onClick={() => navigate('/chat')}
        >
          캐릭터와 대화하기
        </button>
        <button 
          className="button button-secondary"
          onClick={() => navigate('/learn')}
        >
          소설 학습하기
        </button>
      </div>
    </div>
  )
}

export default Home