## Jonathan-Mulyono-AlgoPro_FP

# Overview of Pixel Jack
**Pixel Jack** is a pixelated Blackjack game built using Pyhton and the Pygame library. This game has a pixel art style and retro aesthetic. The game simulates a simple version of Blackjack, where you can play against the dealer by getting a hand total as close as possible to 21 without going over, while competing against the dealer's hand. The game features includes:
- Card Dealing and Scoring
- Pixel Art Style
- Game Soundtrack
- Game Record (wins, losses, and ties)
- Dealer AI
- Interactive Buttons

# Dependencies or Installation Steps
1. Install Pygame: pip install pygame
2. Download or clone the Pixel Jack repository. Ensure the following files are in the root directory of the game:
- main.py (The main game script)
- button_class.py (Contains the button class used for UI elements)
- logo.png, exit.png, card1.png, deal_hand.mp3, defaultclick.mp3, etc. (Assets like images and sounds)
- music_1.mp3 (Background music)
3. Starting Game: Locate main.py and run to start

# Instruction to Run Code and Play the Game
**Running the Game:**
- Once you have all the dependencies and assets in place, open a terminal or command prompt.
- Navigate to the directory where Pixel Jack is stored.
- Run the game by executing the following command: phyton main.py

**Game Instructions:**
- **Start a New Hand:** Press the "DEAL HAND" button to start a new round.
- **Hit:** Click on the "HIT" button to draw another card.
- **Stand:** Click on the "STAND" button to stop drawing cards and let the dealer play.
- **Next Round:** Click on the "NEW HAND" button to play the next round
- **Quit:** Press the "Quit" button to exit the game at any time.
- **Sound Control:** Toggle the background music on and off using the sound button in the top-right corner.

**Game Rules:**
- You and the dealer are dealt two cards each. The goal is to get a hand total as close to 21 as possible without going over.
- Number cards (2-10) are worth their face value, face cards (J, Q, K) are worth 10 points, and A (Aces) can be worth either 1 or 11 points, depending on the hand.
- After your turn, the dealer will reveal their hidden card and follow the rules to hit or stand (dealer must hit if their score is below 17).
- You win if your hand is closer to 21 than the dealer's, and you lose if your hand exceeds 21 or is lower than the dealer's.
- There are indicators for how many wins, losses, and ties.

**Important Keybinds:**
- To Exit the Game: [ESC]
