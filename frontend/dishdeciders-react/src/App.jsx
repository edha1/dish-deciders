import { useState } from 'react'
import axios from 'axios';
import './App.css'

function App() {
  const [input, setInput] = useState("");
  const [error, setError] = useState(null);
  const [recommendations, setRecommendations] = useState([]); 
  const [loading, setLoading] = useState(false); 

  const callAPI = async (e) => {
    e.preventDefault(); 
    setLoading(true); 
    try {
      const response = await axios.post("http://127.0.0.1:5000/recommend", {
        userInput: input 
      }); 
      setLoading(false)
      setRecommendations(response.data)
    } catch (error) {
      setError("Error communcating with the server, please try again later."); 
    }
    setInput("");   
  }

  return (
    <>
    <div className="input-container">
      <textarea
        onChange={(e) => setInput(e.target.value)}
        type="text"
        className = "input-search"
        placeholder="Input here..."
      />
      <p className='description'>What kind of dish would you like to eat? We will give you 10 recommendations of recipes from Food.com!</p>
      <button onClick = {callAPI} className='input-button'>GET RECOMMENDATIONS</button>
    </div>
    {loading && (
        <div className="loader-wrapper">
          <div className="loader"></div>
        </div>
    )}
    <div className= "results-container">
      {recommendations.map((recommendation, index) => (
      <div className="card-container" key={index}>
        <h3 className="card-title">🍽 Dish: {recommendation.CleanedName}</h3>
        <p><strong>👨‍🍳 Uploaded by:</strong> {recommendation.AuthorName || 'Unknown'}</p>
        <p><strong>⏱ Total Time:</strong> {recommendation.TotalTimeMinutes}</p>
        <p><strong>🔥 Calories:</strong> {recommendation.Calories || 'Not specified'}</p>
        <p className="ingredients">
        <strong>🧂 Ingredients:</strong><br />
        {recommendation.CleanedIngredients}
        </p>
      </div>
      ))}
    </div>
    <div>
      { error }
    </div>
    </>
  )
}

export default App
