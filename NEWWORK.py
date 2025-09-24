import tkinter as tk
from tkinter import messagebox
import random
import mysql.connector

# ----------------------------
# MySQL Database Functions
# ----------------------------
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",         # <-- Your MySQL username
        password="boko6999", # <-- Your MySQL password
        database="racing_game"
    )

def save_score(score, difficulty):
    """Save player score to MySQL database automatically."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO scores (player_name, score, difficulty) VALUES ('Player', %s, %s)", (score, difficulty))
    conn.commit()
    conn.close()

def get_top_scores():
    """Fetch top 5 highest scores."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT player_name, score, difficulty FROM scores ORDER BY score DESC LIMIT 5")
    result = cursor.fetchall()
    conn.close()
    return result

# ----------------------------
# Racing Game Class
# ----------------------------
class RacingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter Racing Game with Obstacles")
        self.root.geometry("420x680")
        self.root.resizable(False, False)

        # ----------------------------
        # Game Variables
        # ----------------------------
        self.running = False
        self.paused = False
        self.score = 0
        self.speed = 10
        self.obstacles = []
        self.difficulty = "Medium"

        # ----------------------------
        # Game Canvas
        # ----------------------------
        self.canvas = tk.Canvas(self.root, width=400, height=600, bg="gray")
        self.canvas.pack(pady=10)

        # Draw road
        self.canvas.create_rectangle(100, 0, 300, 600, fill="black")

        # Player car
        self.car = self.canvas.create_rectangle(180, 500, 220, 550, fill="blue")

        # ----------------------------
        # Controls Frame
        # ----------------------------
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=5)

        self.start_btn = tk.Button(control_frame, text="Start", command=self.start_game, width=10, bg="green", fg="white")
        self.start_btn.grid(row=0, column=0, padx=5)

        self.stop_btn = tk.Button(control_frame, text="Stop", command=self.toggle_pause, width=10, bg="orange", fg="white")
        self.stop_btn.grid(row=0, column=1, padx=5)

        self.restart_btn = tk.Button(control_frame, text="Restart", command=self.restart_game, width=10, bg="red", fg="white")
        self.restart_btn.grid(row=0, column=2, padx=5)

        # Speed / Difficulty selection dropdown
        tk.Label(self.root, text="Select Difficulty:").pack()
        self.speed_var = tk.StringVar(value="Medium")
        self.speed_menu = tk.OptionMenu(self.root, self.speed_var, "Easy", "Medium", "Hard")
        self.speed_menu.pack()

        # Score display
        self.score_label = tk.Label(self.root, text="Score: 0", font=("Arial", 16), fg="blue")
        self.score_label.pack(pady=5)

        # ----------------------------
        # Key Bindings
        # ----------------------------
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)

    # ----------------------------
    # Game Control Methods
    # ----------------------------
    def set_difficulty_level(self):
        """Adjust speed and obstacle spawn rate based on difficulty."""
        level = self.speed_var.get()
        self.difficulty = level
        if level == "Easy":
            self.speed = 8
            self.obstacle_rate = 1800
        elif level == "Medium":
            self.speed = 12
            self.obstacle_rate = 1200
        elif level == "Hard":
            self.speed = 16
            self.obstacle_rate = 800

    def start_game(self):
        """Start a new game."""
        if not self.running:
            self.set_difficulty_level()
            self.running = True
            self.paused = False
            self.score = 0
            self.obstacles.clear()
            self.canvas.delete("all")

            # Draw road and car again
            self.canvas.create_rectangle(100, 0, 300, 600, fill="black")
            self.car = self.canvas.create_rectangle(180, 500, 220, 550, fill="blue")

            self.spawn_obstacle()
            self.update_game()

    def toggle_pause(self):
        """Pause or resume the game."""
        if self.running:
            self.paused = not self.paused
            if self.paused:
                self.stop_btn.config(text="Resume", bg="green")
            else:
                self.stop_btn.config(text="Stop", bg="orange")
                self.update_game()

    def restart_game(self):
        """Restart the game completely."""
        self.running = False
        self.paused = False
        self.start_game()

    # ----------------------------
    # Player Movement
    # ----------------------------
    def move_left(self, event):
        if self.running and not self.paused:
            pos = self.canvas.coords(self.car)
            if pos[0] > 110:
                self.canvas.move(self.car, -20, 0)

    def move_right(self, event):
        if self.running and not self.paused:
            pos = self.canvas.coords(self.car)
            if pos[2] < 290:
                self.canvas.move(self.car, 20, 0)

    # ----------------------------
    # Obstacle Logic
    # ----------------------------
    def spawn_obstacle(self):
        """Create obstacles at random lanes."""
        if not self.running or self.paused:
            return
        x_position = random.choice([120, 160, 200, 240])
        obstacle = self.canvas.create_rectangle(x_position, -40, x_position + 40, 0, fill="red")
        self.obstacles.append(obstacle)
        self.root.after(self.obstacle_rate, self.spawn_obstacle)

    def update_game(self):
        if not self.running or self.paused:
            return

        # Move obstacles downward
        for obstacle in self.obstacles:
            self.canvas.move(obstacle, 0, self.speed)

        # Collision detection
        self.check_collision()

        # Update score
        self.score += 1
        self.score_label.config(text=f"Score: {self.score}")

        # Increase difficulty slightly as score goes up
        if self.score % 300 == 0:
            self.speed += 1

        # Remove obstacles off screen
        self.obstacles = [o for o in self.obstacles if self.canvas.coords(o)[1] < 600]

        # Keep the game loop running
        self.root.after(50, self.update_game)

    # ----------------------------
    # Collision Detection
    # ----------------------------
    def check_collision(self):
        car_coords = self.canvas.coords(self.car)
        for obstacle in self.obstacles:
            obs_coords = self.canvas.coords(obstacle)
            if (car_coords[0] < obs_coords[2] and
                car_coords[2] > obs_coords[0] and
                car_coords[1] < obs_coords[3] and
                car_coords[3] > obs_coords[1]):
                self.game_over()

    # ----------------------------
    # Game Over Logic
    # ----------------------------
    def game_over(self):
        self.running = False
        self.paused = False
        self.canvas.create_text(200, 300, text="GAME OVER", font=("Arial", 24), fill="white")

        # Save score automatically
        save_score(self.score, self.difficulty)

        # Show leaderboard
        self.show_leaderboard()

    def show_leaderboard(self):
        top_scores = get_top_scores()
        leaderboard_text = "\n".join(
            [f"{i+1}. {row[0]} - {row[1]} pts ({row[2]})" for i, row in enumerate(top_scores)]
        )
        messagebox.showinfo("Leaderboard", leaderboard_text)

# ----------------------------
# Run the Game
# ----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    game = RacingGame(root)
    root.mainloop()
