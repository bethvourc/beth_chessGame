# beth_chessGame
**ReadMe for Chess Game Code**

This code represents a Python implementation of a chess game, including a start menu and the main chess gameplay. Below is a brief overview of the code structure and functionality:

**StartMenu Class:**
- The `StartMenu` class initializes the game's start menu, where players can begin a new chess game.
- It sets up the game window, loads background music, and handles the play button's hover effect.
- Players can click the play button to start the chess game, triggering a sound effect.

**Main Class:**
- The `Main` class manages the main gameplay of the chess game.
- It creates the game window and initializes the chessboard, pieces, and game logic.
- The main game loop continually updates the display, handles user input (mouse clicks and movements), and allows players to make moves and interact with the chessboard.
- Players can reset the game or change the theme using keyboard shortcuts (R for reset, T for theme change).
- The game continues until the player quits or closes the window.

**Important Modules:**
- The code relies on several custom modules, including `const.py`, `game.py`, `square.py`, `move.py`, and `sound.py`, to manage game constants, game logic, square representations, move validations, and sound effects, respectively.

This chess game offers an interactive user interface and allows players to make valid chess moves using the mouse. It also includes features like theme changes and resetting the game. The code structure is modular and organized, making it easy to maintain and extend. To play the game, simply run the code, and the start menu will guide you into the chessboard interface.