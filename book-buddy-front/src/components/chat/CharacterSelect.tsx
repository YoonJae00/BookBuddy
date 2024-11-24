import { useState, useEffect } from 'react';
import { apiService } from '../../api';
import './CharacterSelect.css';

function CharacterSelect({ novelId, onSelect, onBack }) {
  const [characters, setCharacters] = useState([]);

  useEffect(() => {
    const fetchCharacters = async () => {
      try {
        const response = await apiService.getCharacters(novelId);
        setCharacters(response.data);
      } catch (error) {
        console.error('Failed to fetch characters:', error);
      }
    };
    fetchCharacters();
  }, [novelId]);

  return (
    <div className="character-select">
      <div className="header">
        <button className="back-button" onClick={onBack}>
          ←
        </button>
        <h1 className="title">캐릭터 선택하기</h1>
      </div>
      <div className="character-grid">
        {characters.map(character => (
          <div
            key={character.id}
            className="character-card"
            onClick={() => onSelect(character)}
          >
            <div className="avatar">
              {character.full_name[0]}
            </div>
            <span className="character-name">{character.full_name}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default CharacterSelect;