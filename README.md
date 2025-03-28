# ELO-tracker
final bootcamp project


A web application to track Elo ratings for players and update their ratings based on match results.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation

To run this project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/username/project-name.git
   ```

2. Navigate into the project directory:
   ```bash
   cd ELO-tracker
   ```

3. Install dependencies:
   - For the backend (Flask):
     ```bash
     pip install -r requirements.txt
     ```

   - For the frontend (React):
     ```bash
     npm install
     ```

4. Set up your environment variables (if necessary). Example:
   ```bash
   export FLASK_APP=app.py
   export FLASK_ENV=development
   ```

5. Run the project:
   - Backend (Flask):
     ```bash
     flask run
     ```
   - Frontend (React):
     ```bash
     npm start
     ```

The app should now be running at `http://localhost:3000` (frontend) and `http://localhost:5000` (backend).


## Usage

- Open your browser and go to `http://localhost:3000` to view the application.
- You can add players, view the leaderboard, and update ratings based on match results.

**Example API Usage (for backend):**

- To get the leaderboard:
  ```bash
  GET http://localhost:5000/leaderboard
  ```
- To update player ratings:
  ```bash
  POST http://localhost:5000/update_rating
  {
    "player_a": "Player1",
    "player_b": "Player2",
    "result": 1
  }
  ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
