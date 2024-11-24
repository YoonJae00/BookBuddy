import { useState, useEffect } from 'react'
import { collection, getDocs } from 'firebase/firestore'
import { db } from '../firebase'
import './DebugDatabase.css'

function DebugDatabase() {
  const [data, setData] = useState({
    novels: [],
    characters: [],
    events: [],
    chat_history: []
  })
  const [selectedCollection, setSelectedCollection] = useState(null)
  const [selectedItem, setSelectedItem] = useState(null)

  useEffect(() => {
    const fetchAllData = async () => {
      const collections = ['novels', 'characters', 'events', 'chat_history']
      const allData = {}

      for (const collectionName of collections) {
        const querySnapshot = await getDocs(collection(db, collectionName))
        allData[collectionName] = querySnapshot.docs.map(doc => ({
          id: doc.id,
          ...doc.data()
        }))
      }

      setData(allData)
    }

    fetchAllData()
  }, [])

  const renderCollectionButtons = () => (
    <div className="collection-buttons">
      {Object.keys(data).map(collection => (
        <button
          key={collection}
          className={`collection-button ${selectedCollection === collection ? 'active' : ''}`}
          onClick={() => {
            setSelectedCollection(collection)
            setSelectedItem(null)
          }}
        >
          {collection} ({data[collection].length})
        </button>
      ))}
    </div>
  )

  const renderItems = () => {
    if (!selectedCollection) return null
    
    return (
      <div className="items-list">
        {data[selectedCollection].map(item => (
          <div
            key={item.id}
            className={`item-summary ${selectedItem?.id === item.id ? 'active' : ''}`}
            onClick={() => setSelectedItem(item)}
          >
            {item.title || item.full_name || item.content?.slice(0, 50) || item.id}
          </div>
        ))}
      </div>
    )
  }

  const renderItemDetail = () => {
    if (!selectedItem) return null

    return (
      <div className="item-detail">
        <pre>{JSON.stringify(selectedItem, null, 2)}</pre>
      </div>
    )
  }

  return (
    <div className="debug-database">
      <h1>데이터베이스 디버그</h1>
      {renderCollectionButtons()}
      <div className="content-container">
        {renderItems()}
        {renderItemDetail()}
      </div>
    </div>
  )
}

export default DebugDatabase