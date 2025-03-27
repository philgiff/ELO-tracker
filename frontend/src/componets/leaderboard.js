import React, { useEffect, useState } from "react";

const Leaderboard = () => {
  const [players, setPlayers] = useState({});

  useEffect(() => {
    fetch("http://127.0.0.1:5000/leaderboard")
      .then((response) => response.json())
      .then((data) => setPlayers(data));
  }, []);

  return (
    <div>
      <h2>Leaderboard</h2>
      <ul>
        {Object.entries(players).map(([player, rating]) => (
          <li key={player}>{player}: {rating}</li>
        ))}
      </ul>
    </div>
  );
};

export default Leaderboard;
