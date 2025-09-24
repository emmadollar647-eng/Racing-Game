
# 🚗 Tkinter Racing Game with MySQL Integration  

A fun **car racing game** built with **Python Tkinter** for the GUI and **MySQL** for storing player scores and difficulty levels.  
This game features **real-time scoring**, **multiple difficulty levels**, and a **leaderboard** that saves results to a database automatically.

---

## **📌 Features**
- 🏎 **Simple Car Racing Gameplay** – Avoid obstacles and survive as long as you can.  
- 📊 **Score Tracking** – Score updates live as you play.  
- 🎚 **Difficulty Levels** – Choose between:
  - **Easy** – Slower speed, fewer obstacles.  
  - **Medium** – Balanced challenge.  
  - **Hard** – High speed, frequent obstacles.  
- 💾 **MySQL Integration** – Automatically saves scores and difficulty to a database.  
- 🏆 **Leaderboard** – Displays the top 5 highest scores after every game.  
- ⏸ **Pause / Resume** – Stop the game and resume at any time.  
- 🔁 **Restart Button** – Instantly restart a fresh game session.

---

## **🛠 Tech Stack**
- **Python 3.9+**
- **Tkinter** – For the game UI.
- **MySQL** – For storing and managing player scores.
- **mysql-connector-python** – To connect Python with MySQL.

---

## **⚙️ Setup Instructions**

### **1. Clone the Repository**
`bash
git clone https://github.com/yourusername/tkinter-racing-game.git
cd tkinter-racing-game`


### 2. Install Python Dependencies 

Make sure you have pip installed.
Install MySQL connector:

`pip install mysql-connector-python`

### **3. Set Up MySQL Database**

Open MySQL and run the following commands:

`CREATE DATABASE IF NOT EXISTS racing_game;`

`USE racing_game;`

`CREATE TABLE IF NOT EXISTS scores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    player_name VARCHAR(50) DEFAULT 'Player',
    score INT,
    difficulty VARCHAR(20),
    date_played TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);`


Update the database credentials in the Python script (connect_db function):

`def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",         # Your MySQL username
        password="boko6999", # Your MySQL password
        database="racing_game"
    )`

### ▶️ Run the Game

Run the Python script:

`python racing_game.py`

### 🎮 How to Play
Action	Control
Move Left	⬅ Left Arrow
Move Right	➡ Right Arrow
Pause / Resume	Stop Button
Restart Game	Restart Button

Avoid the red obstacles while driving.

Survive as long as possible to increase your score.

Your score is automatically saved when the game ends.

### 📊 Difficulty Levels
Level	Speed	Obstacle Spawn Rate
Easy	Slow	1 obstacle every 1.8 sec
Medium	Moderate	1 obstacle every 1.2 sec
Hard	Fast	1 obstacle every 0.8 sec


