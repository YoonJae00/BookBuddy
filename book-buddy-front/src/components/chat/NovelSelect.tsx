import { useEffect, useState } from 'react'
import { apiService } from '../../api'
import './NovelSelect.css'

function NovelSelect({ onSelect }) {
  const [novels, setNovels] = useState([])
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchNovels = async () => {
      try {
        const response = await apiService.getNovels()
        setNovels(response.data)
      } catch (error) {
        setError('소설 목록을 불러오는데 실패했습니다.')
      }
    }
    fetchNovels()
  }, [])

  return (
    <div className="novel-select">
      <div className="novel-content">
        <h1 className="title">소설 선택하기</h1>
        {error && <div className="error-message">{error}</div>}
        <div className="novel-grid">
          {novels.map(novel => (
            <div 
              key={novel.id}
              className="novel-card"
              onClick={() => onSelect(novel)}
            >
              <h2 className="novel-title">{novel.title}</h2>
              <p className="novel-author">{novel.author}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default NovelSelect