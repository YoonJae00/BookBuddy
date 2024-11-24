import { useState } from 'react'
import NovelSelect from '../components/chat/NovelSelect'
import CharacterSelect from '../components/chat/CharacterSelect'
import ChatRoom from '../components/chat/ChatRoom'
import './NovelList.css'

function NovelList() {
  const [selectedNovel, setSelectedNovel] = useState(null)
  const [selectedCharacter, setSelectedCharacter] = useState(null)

  const handleNovelSelect = (novel) => {
    setSelectedNovel(novel)
    setSelectedCharacter(null)
  }

  const handleCharacterSelect = (character) => {
    setSelectedCharacter(character)
  }

  const handleBack = () => {
    if (selectedCharacter) {
      setSelectedCharacter(null)
    } else if (selectedNovel) {
      setSelectedNovel(null)
    }
  }

  return (
    <div className="novel-list-container">
      {!selectedNovel && (
        <NovelSelect onSelect={handleNovelSelect} />
      )}
      {selectedNovel && !selectedCharacter && (
        <CharacterSelect 
          novelId={selectedNovel.id} 
          onSelect={handleCharacterSelect}
          onBack={handleBack}
        />
      )}
      {selectedCharacter && (
        <ChatRoom 
          character={selectedCharacter} 
          onBack={handleBack}
        />
      )}
    </div>
  )
}

export default NovelList