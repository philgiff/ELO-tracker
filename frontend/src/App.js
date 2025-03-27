import React, { useState, useEffect } from 'react';
import axios from 'axios';

const App = () => {
  // State to hold user input for players and match results
  const [playerA, setPlayerA] = useState('');
  const [playerB, setPlayerB] = useState('');
  const [result, setResult] = useState('');
  const [message, setMessage] = useState('');
  const [leaderboard, setLeaderboard] = useState([]);

  // Handle input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    if (name === 'playerA') {
      setPlayerA(value);
    } else if (name === 'playerB') {
      setPlayerB(value);
    } else if (name === 'result') {
      setResult(value);
    }
  };

  // Handle form submission to update ratings
  const handleSubmit = async (e) => {
    e.preventDefault();

    const data = {
      player_a: playerA,
      player_b: playerB,
      result: parseFloat(result), // Convert result to number
    };

    try {
      // Send the match data to the backend (Flask)
      const response = await fetch('http://localhost:5000/update_rating', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      const result = await response.json();

      if (response.ok) {
        setMessage(result.message);  // Success message
        fetchLeaderboard();          // Fetch updated leaderboard
      } else {
        setMessage(result.error);    // Error message
      }
    } catch (error) {
      console.error('Error updating rating:', error);
      setMessage('An error occurred while updating the rating.');
    }
  };

  // Fetch leaderboard from the backend
  const fetchLeaderboard = async () => {
    try {
      const response = await fetch('http://localhost:5000/leaderboard');
      const leaderboardData = await response.json();
      setLeaderboard(Object.entries(leaderboardData).map(([name, rating]) => ({ name, rating })));
    } catch (error) {
      console.error('Error fetching leaderboard:', error);
    }
  };

  // Load leaderboard on initial render
  React.useEffect(() => {
    fetchLeaderboard();
  }, []);

  return (
   
    <div className="App">
      <h1>Elo Tracker</h1>

      {/* Form to submit match results */}
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="playerA">Player A:</label>
          <input
            type="text"
            id="playerA"
            name="playerA"
            value={playerA}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label htmlFor="playerB">Player B:</label>
          <input
            type="text"
            id="playerB"
            name="playerB"
            value={playerB}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label htmlFor="result">Result:</label>
          <select
            name="result"
            value={result}
            onChange={handleChange}
            required
          >
            <option value="">Select Result</option>
            <option value="1">Player A Wins</option>
            <option value="0">Player B Wins</option>
            <option value="0.5">Draw</option>
          </select>
        </div>
        <button type="submit">Update Rating</button>
      </form>

      {/* Message display */}
      {message && <p>{message}</p>}

      {/* Display the leaderboard */}
      <h2>Leaderboard</h2>
      <ul>
        {leaderboard.map((player) => (
          <li key={player.name}>
            {player.name}: {player.rating}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default App;
