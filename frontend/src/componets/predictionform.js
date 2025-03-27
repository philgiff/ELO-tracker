import React, { useState } from "react";

const PredictionForm = () => {
  const [playerA, setPlayerA] = useState("");
  const [playerB, setPlayerB] = useState("");
  const [prediction, setPrediction] = useState(null);

  const handlePredict = async () => {
    const response = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ player_a: playerA, player_b: playerB }),
    });
    const data = await response.json();
    setPrediction(data);
  };

  return (
    <div>
      <h3>Predict Match Outcome</h3>
      <input
        type="text"
        placeholder="Player A"
        value={playerA}
        onChange={(e) => setPlayerA(e.target.value)}
      />
      <input
        type="text"
        placeholder="Player B"
        value={playerB}
        onChange={(e) => setPlayerB(e.target.value)}
      />
      <button onClick={handlePredict}>Predict</button>

      {prediction && (
        <div>
          <h4>Prediction Results:</h4>
          <p>{prediction.player_a} ({prediction.rating_a}) Win Chance: {prediction.win_probability_a}%</p>
          <p>{prediction.player_b} ({prediction.rating_b}) Win Chance: {prediction.win_probability_b}%</p>
        </div>
      )}
    </div>
  );
};

export default PredictionForm;
