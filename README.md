## Flappy Hand : A Fun Take on Flappy Bird with Hand Tracking

**Flappy Hand ** is a game that combines the classic Flappy Bird gameplay with real-time hand gesture recognition using OpenCV and MediaPipe. This project is designed to explore the integration of computer vision in game development, allowing players to control a bird's flight with simple hand gestures like moving their index finger and giving a thumbs-up.

## Motivation

This project was born out of a desire to learn how computer vision and machine learning could be used in a fun and engaging way.  By using hand tracking, I have created a game that's not only enjoyable to play but also provides a hands-on understanding of real-time gesture recognition, tough this is my first project while learning Computer Vision.

## How to Play

### Prerequisites

* Python 3.x
* OpenCV (install using `pip install opencv-python`)
* MediaPipe (install using `pip install mediapipe`)
* Pygame (install using `pip install pygame`)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/FlappyHandGesture.git
   cd FlappyHandGesture
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game:**

   ```bash
   python game.py
   ```

### Gameplay Instructions

* **Starting the Game:** After launching the game, you'll see the bird on the screen. The game starts when you show a thumbs-up gesture to the camera.
* **Controlling the Bird:**
    * **Vertical Movement:** Move your index finger up or down in front of the camera to control the bird's vertical movement.
    * **Acceleration:** Move your index finger to the right side of the screen to accelerate the bird forward.
    * **Deceleration/Leftward Movement:** Move your index finger to the left side of the screen to decelerate the bird or move it left.
* **Objective:** Navigate the bird through the gaps between obstacles. The game gets progressively harder as you level up.
* **Game Over:** The game ends when the bird collides with an obstacle. You can restart the game by clicking the "Restart" button.

## Game Structure

### Key Components

* **Hand Gesture Recognition (`hand_gesture.py`):**
    * Uses MediaPipe to track hand landmarks and recognize gestures.
    * Captures the position of the index finger and identifies a thumbs-up gesture to control game mechanics.
* **Game Logic (`game.py`):**
    * Manages game states, rendering, and collision detection.
    * Implements bird movement based on the input from hand gestures.
* **Assets:** The game includes a bird sprite (`assets/bird.png`) and a background image (`assets/background.png`) to enhance the visual appeal.

### Game Flow

1. **Initialization:** The game initializes by setting up the Pygame environment, loading assets, and starting the camera for hand gesture tracking.
2. **Gesture Detection:** Hand gestures are processed in real-time, and the bird's movement is updated accordingly.
3. **Obstacle Generation:** Obstacles are generated at random intervals with varying gaps and speeds to challenge the player.
4. **Collision Detection:** The game continuously checks for collisions between the bird and obstacles, which triggers the game-over state.

## TODO List

* **Add More Gestures:** Implement additional gestures to control different game mechanics, such as pausing the game or changing the bird's speed.
* **Enhance Graphics:** Improve the visual quality of the game with more detailed sprites and background animations.
* **Add Sound Effects:** Incorporate sound effects for bird flapping, collisions, and background music to enhance the gaming experience.
* **Implement a High Score System:** Track and display the highest score achieved by the player.
* **Mobile Version:** Adapt the game for mobile devices by utilizing the camera and touchscreen controls.
* **Multiplayer Mode:** Allow multiple players to compete in real-time by controlling different birds with separate hand gestures.

## Conclusion

Flappy Hand  is a fun and simple game that demonstrates the potential of computer vision in interactive applications.  It's a great starting point for anyone interested in exploring hand tracking and gesture recognition in game development. We encourage you to contribute, enhance, or modify the project!

**Happy coding!**

**Contribution:**

Feel free to fork this repository, raise issues, or contribute to its development. 
