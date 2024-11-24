import { useState, useEffect } from 'react'
import { apiService } from '../api'
import './NovelLearning.css'

function NovelLearning() {
  const [title, setTitle] = useState('')
  const [content, setContent] = useState('')
  const [author, setAuthor] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [message, setMessage] = useState(null)
  const [estimatedTime, setEstimatedTime] = useState('')

  const calculateEstimatedTime = (contentLength: number) => {
    const secondsPerChar = 0.08
    const totalSeconds = Math.round(contentLength * secondsPerChar)
    const minutes = Math.floor(totalSeconds / 60)
    const seconds = totalSeconds % 60
    return `예상 소요시간: ${minutes}분 ${seconds}초`
  }

  useEffect(() => {
    if (content) {
      setEstimatedTime(calculateEstimatedTime(content.length))
    } else {
      setEstimatedTime('')
    }
  }, [content])

  const handleSubmit = async () => {
    if (!title || !content || !author) {
      setMessage({ type: 'error', text: '모든 필드를 입력해주세요.' })
      return
    }

    setIsLoading(true)
    try {
      await apiService.createNovel({ title, content, author })
      setMessage({ type: 'success', text: '소설이 성공적으로 학습되었습니다.' })
      setTitle('')
      setContent('')
      setAuthor('')
      setEstimatedTime('')
    } catch (error) {
      setMessage({ type: 'error', text: '소설 학습에 실패했습니다.' })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="novel-learning">
      <div className="novel-learning-content">
        <h1 className="title">소설 학습하기</h1>
        {message && (
          <div className={`message ${message.type}`}>
            {message.text}
          </div>
        )}
        <div className="form">
          <div className="form-group">
            <label>제목</label>
            <input
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="소설 제목을 입력하세요"
            />
          </div>
          <div className="form-group">
            <label>작가</label>
            <input
              value={author}
              onChange={(e) => setAuthor(e.target.value)}
              placeholder="작가 이름을 입력하세요"
            />
          </div>
          <div className="form-group">
            <label>내용</label>
            <textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
              placeholder="소설 내용을 입력하세요"
            />
            {estimatedTime && (
              <div className="estimated-time">{estimatedTime}</div>
            )}
          </div>
          <button
            className={`submit-button ${isLoading ? 'loading' : ''}`}
            onClick={handleSubmit}
            disabled={isLoading}
          >
            {isLoading ? `처리중... (${estimatedTime})` : '학습하기'}
          </button>
        </div>
      </div>
    </div>
  )
}

export default NovelLearning