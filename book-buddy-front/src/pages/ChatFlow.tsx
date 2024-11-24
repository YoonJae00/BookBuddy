import { useState } from 'react'
import NovelSelect from '../components/chat/NovelSelect'
import CharacterSelect from '../components/chat/CharacterSelect'
import ChatRoom from '../components/chat/ChatRoom'
import './ChatFlow.css'

function ChatFlow() {
  const [selectedNovel, setSelectedNovel] = useState(null)
  const [selectedCharacter, setSelectedCharacter] = useState(null)

  return (
    <div className="chat-flow">
      {!selectedNovel ? (
        <NovelSelect onSelect={setSelectedNovel} />
      ) : !selectedCharacter ? (
        <CharacterSelect 
          novelId={selectedNovel.id} 
          onSelect={setSelectedCharacter}
          onBack={() => setSelectedNovel(null)}
        />
      ) : (
        <ChatRoom 
          character={selectedCharacter}
          onBack={() => setSelectedCharacter(null)}
        />
      )}
    </div>
  )
}

export default ChatFlow