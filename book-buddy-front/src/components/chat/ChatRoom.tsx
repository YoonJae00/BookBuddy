import { useState, useEffect, useRef } from 'react'
import { apiService } from '../../api'
import './ChatRoom.css'

function ChatRoom({ character, onBack }) {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    const fetchChatHistory = async () => {
      try {
        const response = await apiService.getChatHistory(character.id)
        if (Array.isArray(response.data)) {
          const formattedMessages = response.data.map(msg => ({
            content: msg.content,
            role: msg.role,
            timestamp: msg.timestamp
          }))
          setMessages(formattedMessages)
        } else {
          setMessages([])
        }
      } catch (error) {
        console.error('Failed to fetch chat history:', error)
      }
    }
    fetchChatHistory()
  }, [character.id])

  useEffect(scrollToBottom, [messages])

  const handleSend = async () => {
    if (!input.trim()) return

    const newMessage = {
      content: input,
      role: 'user',
      timestamp: new Date().toISOString()
    }

    setMessages(prev => [...prev, newMessage])
    setInput('')

    try {
      const response = await apiService.sendMessage(character.id, input, "anonymous")
      setMessages(prev => [...prev, {
        content: response.data.response,
        role: 'assistant',
        timestamp: new Date().toISOString()
      }])
    } catch (error) {
      console.error('Failed to send message:', error)
    }
  }

  return (
    <div className="chat-container">
      <div className="chat-content">
        <div className="chat-header">
          <button className="back-button" onClick={onBack}>
            ←
          </button>
          <div className="avatar">{character.full_name[0]}</div>
          <span className="character-name">{character.full_name}</span>
        </div>

        <div className="messages-container">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`message ${message.role === 'user' ? 'user' : 'assistant'}`}
            >
              <div className="message-content">
                {message.content}
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        <div className="input-container">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="메시지를 입력하세요..."
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          />
          <button onClick={handleSend} className="send-button">
            →
          </button>
        </div>
      </div>
    </div>
  )
}

export default ChatRoom