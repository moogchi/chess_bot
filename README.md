# Python Chess Engine ♟️

A playable chess engine built in Python. This project features a robust AI powered by a Negamax search algorithm and a clean, minimalist graphical user interface (GUI) using Python's native Tkinter library.

---

## Features

- **Search Algorithm**: A Negamax search implementation with Alpha-Beta Pruning for efficient move exploration.
- **Board Evaluation**: The engine evaluates positions based on:
  - **Material**: Standard piece values.
  - **Positional Play**: Piece-Square Tables (PSTs) that know where pieces are most effective.
  - **Game Phase**: Switches between middlegame and endgame logic for king activity.
- **Performance**:
  - **Transposition Tables**: Caches previously evaluated positions to drastically speed up search.
  - **Quiescence Search**: Deepens the search for captures to avoid the "horizon effect" and improve tactical accuracy.
- **Cross-Platform GUI**: A simple and responsive interface built with Tkinter that runs on Windows, macOS, and Linux.

---

## Project Structure

The project is organized into three main files:

- `gui.py`: The main application file. **Run this file to start the game.**
- `engine.py`: Contains all the core chess logic, including the search and evaluation functions.
- `pst.py`: A data file that stores all the constants for evaluation, such as piece values and Piece-Square Tables.

---

## Setup and Installation

Before you can run the engine, you need Python 3 and one library.

### Prerequisites

- Python 3.6 or newer
- The `python-chess` library

### Installation

1.  **Get the Code**: Make sure all three files (`gui.py`, `engine.py`, `pst.py`) are in the same folder.

2.  **Install the Library**: Open your terminal or command prompt and run the following command to install the `python-chess` library:
    ```bash
    pip install chess
    ```

---

## How to Run the Game

Navigate to the project folder in your terminal or command prompt, then follow the instructions for your operating system.

### 🖥️ Windows

1.  Open **Command Prompt** or **PowerShell**.
2.  Run the GUI file with the following command:
    ```bash
    python gui.py
    ```
    _If you have multiple Python versions installed, you may need to use `py -3 gui.py`._

### 🍎 macOS & 🐧 Linux

1.  Open the **Terminal** application.
2.  Run the GUI file with the following command:
    ```bash
    python3 gui.py
    ```
    _(On some systems, `python gui.py` may also work)._

A window will appear with the chessboard, and you can begin playing. You play as White by default. To play as Black, you can edit the `self.player_is_white` variable in `gui.py`.
