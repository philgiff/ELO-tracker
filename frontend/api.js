const API_URL = "http://localhost:3000";

export async function getLeaderboard() {
    const response = await fetch(`${API_URL}/leaderboard`);
    return response.json();
}

export async function recordMatch(playerA, playerB, result) {
    const response = await fetch(`${API_URL}/match`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ player_a: playerA, player_b: playerB, result })
    });
    return response.json();
}

export async function predictMatch(playerA, playerB) {
    const response = await fetch(`${API_URL}/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ player_a: playerA, player_b: playerB })
    });
    return response.json();
}
