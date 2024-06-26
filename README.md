# SET Card Game - Python Implementation

## Introduction
SET is a captivating card game that challenges players to identify sets of cards based on distinct features: number, symbol, shading, and color. This Python implementation aims to provide an interactive way to play SET programmatically, making it a great tool for learning both game design and complex logic handling in programming.

## Why This Code?
The purpose of this implementation is to offer an educational tool for individuals interested in understanding the mechanics of the SET card game through coding. It is designed for those with a basic background in Python and can be an excellent project for aspiring game developers or programmers.

## Prerequisites
Before you install and run the game, make sure you have the following:
- **Python**: Version 3.x [Download Python](https://www.python.org/downloads/)
- **Pygame**: This can be installed using pip, which comes with Python. To install Pygame, open your command line and enter:
  ```bash
  pip install pygame

### Installation
To set up the SET game on your local system, follow these steps:
Clone the Repository:
```bash
git clone https://github.com/Ruohann/SET
cd SET
```
Navigate to the Game Directory:
Ensure you are in the directory containing game.py and the images folder.
Running the Game
Execute the following command in the command line within the SET-game directory to start the game:
```bash
python game.py
```
A new window will display the game interface, allowing you to start playing immediately.

## Game Interface
- **Card Display Area**: 12 cards are shown at a time.
- **Score and Timer Display**: Keep track of your score and remaining time at the top of the window.

## How to Play
- **Selecting Cards**: Click on cards to select them; selected cards are highlighted.
- **Identifying SETs**: A set consists of three cards where each attribute (number, symbol, color, shading) is either all the same or all different across the cards.
- **Scoring**: Points are awarded for each valid set, and new cards replace the matched set.

## How It Works
### Card Class
Each card in the game is represented by an instance of the Card class, which includes attributes for number, symbol, color, and shading. Cards are visualized using images loaded based on their attributes.
```python
class Card:
    def __init__(self, number, symbol, color, shading):
        self.number = number  # Number of shapes
        self.symbol = symbol  # Shape type
        self.color = color    # Color of shapes
        self.shading = shading  # Shading type
        self.image = self.load_image()  # Load card image
```
### Game Mechanics
The game logic includes:
#### Loading and displaying card images.
Each card in the game is represented by a 'Card' class, which includes a method for loading the image based on its attributes. Images are named according to a convention that reflects the card's properties, making them easy to load dynamically during gameplay.

Here's how card images are loaded and displayed:
```python
class Card:
    def load_image(self):
        # Maps attributes to filenames
        color_map = {1: 'green', 2: 'purple', 3: 'red'}
        symbol_map = {1: 'diamond', 2: 'oval', 3: 'squiggle'}
        shading_map = {1: 'empty', 2: 'filled', 3: 'shaded'}
        
        # Construct filename based on card attributes
        filename = f"images/{color_map[self.color]}_{symbol_map[self.symbol]}_{shading_map[self.shading]}_{self.number}.gif"
        return pygame.image.load(filename)

def display_cards(screen, cards_on_table, selected_indices):
    card_width = 100
    card_height = 150
    gap = 20  
    start_x = (screen.get_width() - (4 * card_width + 3 * gap)) // 2
    start_y = 50  

    for idx, card in enumerate(cards_on_table):
        card.rect = pygame.Rect(x, y, card_width, card_height)
        screen.blit(image, (x, y))  # Draw the card image on the screen
```
#### Checking for Sets Among Selected Cards 
The game logic includes a function to determine if three selected cards make a set. A set is defined as three cards where each feature (number, symbol, color, shading) is either all the same or all different.

```python
def is_set(card1, card2, card3):
    # Determines if three cards form a set based on their attributes.
    for attr in ['number', 'symbol', 'color', 'shading']:
        values = {getattr(card1, attr), getattr(card2, attr), getattr(card3, attr)}
        if len(values) == 2:
            return False 
    return True
```
#### Managing Game States Including Timing and Score Tracking
The game includes a timer that limits how long players have to find a set. Scores are updated based on successful set identifications or failures. The game loop handles these elements by checking for user inputs, updating game states, and rendering updates to the screen.
```python
def main():
    time_limit = select_difficulty(screen, small_font)  # Player chooses game difficulty, which sets the time limit

    start_time = time.time()
    player_score = 0
    computer_score = 0

    while running:
        current_time = time.time()
        elapsed_time = current_time - start_time
        time_left = max(time_limit - elapsed_time, 0)

        # Event handling for user interactions
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for idx, card in enumerate(cards_on_table):
                    if card.rect.collidepoint(x, y):
                         if idx in selected_indices:
                            selected_indices.remove(idx)
                        else:
                            selected_indices.append(idx)

        # Update display
        display_cards(screen, cards_on_table, selected_indices)

        # Check and update scores
        if len(selected_indices) == 3 and is_set(*[cards_on_table[i] for i in selected_indices]):
            player_score += 1  # Increment score for successful set
            # Remove found set and replenish cards
            update_cards_after_set_found(cards_on_table, remaining_cards, selected_indices)
            start_time = time.time()  # Reset timer

        # Render score and timer
        display_score_and_timer(screen, small_font, player_score, computer_score, time_left)

        pygame.display.flip()  # Update the screen with rendered changes
        clock.tick(30)  # Maintain 30 frames per second
```
