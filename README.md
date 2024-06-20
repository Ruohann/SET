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

## Game Interface
- **Card Display Area**: 12 cards are shown at a time.
- **Score and Timer Display**: Keep track of your score and remaining time at the top of the window.

## How to Play
- **Selecting Cards**: Click on cards to select them; selected cards are highlighted.
- **Identifying SETs**: A set consists of three cards where each attribute (number, symbol, color, shading) is either all the same or all different across the cards.
- **Scoring**: Points are awarded for each valid set, and new cards replace the matched set.

## Code Structure

### Card Class
This class encapsulates the properties of a SET card, which includes number, symbol, shading, and color.

```python
class Card:
    def __init__(self, number, symbol, shading, color):
        self.number = number
        self.symbol = symbol
        self.shading = shading
        self.color = color
```

### Deck Creation and Shuffling
Generates a deck of 81 unique cards and shuffles them to ensure random distribution:

```python
def create_deck():
    features = {
        'number': [1, 2, 3],
        'symbol': ['diamond', 'squiggle', 'oval'],
        'shading': ['solid', 'striped', 'open'],
        'color': ['red', 'green', 'purple']
    }
    deck = [Card(number, symbol, shading, color) 
            for number in features['number']
            for symbol in features['symbol']
            for shading in features['shading']
            for color in features['color']]
    random.shuffle(deck)
    return deck
