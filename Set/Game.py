import pygame
import sys
import random
import time

class Card:
    """
    Represents a card in the game of SET with a number, symbol, color, and shading.
    
    Attributes:
        number (int): Number of shapes on the card.
        symbol (int): Shape type of the card.
        color (int): Color of the shapes.
        shading (int): Shading type of the shapes.
        image (pygame.Surface): Loaded image of the card for rendering.
        rect (pygame.Rect): The rectangle defining the card's position and dimensions.
    """

    def __init__(self, number, symbol, color, shading):
       # Initialize each card with provided attributes and load its image

        self.number = number
        self.symbol = symbol
        self.color = color
        self.shading = shading
        self.image = self.load_image()# Load the card image upon initialization
        self.rect = None # Will be set when the card is displayed on the screen.

    def load_image(self):
        """
        Loads an image based on the card's attributes from the file system.

        Returns:
            pygame.Surface: The loaded image.
        """
        # Maps card attributes to filenames
        color_map = {1: 'green', 2: 'purple', 3: 'red'}
        symbol_map = {1: 'diamond', 2: 'oval', 3: 'squiggle'}
        shading_map = {1: 'empty', 2: 'filled', 3: 'shaded'}
        filename = f"images/{color_map[self.color]}{symbol_map[self.symbol]}{shading_map[self.shading]}{self.number}.gif"
        return pygame.image.load(filename)# Load and return the card image

    def __eq__(self, other):
       # Equality check to see if two cards are the same
        return (self.number == other.number and self.symbol == other.symbol and
                self.color == other.color and self.shading == other.shading)

    def __str__(self):
       # Returns a string representation of the card
        return f"Card({self.number}, {self.symbol}, {self.color}, {self.shading})"

    def visualize(self):
        # Optional method for text-based representation (useful for debugging)
        return f"{self.number}{self.symbol}{self.color}{self.shading}"

def is_set(card1, card2, card3):
    """Determines if three cards form a set based on their attributes.
    A set is formed if, for each attribute, the values are either all different or all the same.
    """
    
    for attr in ['number', 'symbol', 'color', 'shading']:
        values = {getattr(card1, attr), getattr(card2, attr), getattr(card3, attr)}
        if len(values) == 2:
            return False
    return True

def find_one_set(cards):
    """Finds and returns the indices of the first valid set found among the cards, or None if no set is found."""
    for i in range(len(cards)):
        for j in range(i + 1, len(cards)):
            for k in range(j + 1, len(cards)):
                if is_set(cards[i], cards[j], cards[k]):
                    return [i, j, k]
    return None

def find_all_set(cards):
    """Finds and returns all valid sets among the provided cards as a list of tuples of indices."""
    sets = []
    for i in range(len(cards)):
        for j in range(i + 1, len(cards)):
            for k in range(j + 1, len(cards)):
                if is_set(cards[i], cards[j], cards[k]):
                    sets.append((i, j, k))
    return sets

def show_message(screen, text, font, duration, color, background=None):
    """Displays a message on the screen for a certain duration with specified font and color.
    This function can be used to show game status updates such as 'Ready' or 'Go!'."""
    screen.fill((255, 255, 255) if background is None else background)
    message = font.render(text, True, color)
    rect = message.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(message, rect)# Blit the text onto the screen
    pygame.display.flip()# Update the display
    time.sleep(duration)# Pause for the duration before the next action

def select_difficulty(screen, font):
    """Displays difficulty selection and returns the selected time limit.
    Players can choose between Easy (60 seconds), Medium (30 seconds), or Hard (15 seconds).
    """
    screen.fill((255, 255, 255))
    title = font.render("SET", True, (0, 128, 0))
    title_rect = title.get_rect(center=(400, 100))
    screen.blit(title, title_rect)

    titles = ["1. Easy (60 seconds)", "2. Medium (30 seconds)", "3. Hard (15 seconds)"]
    positions = [(400, 200), (400, 300), (400, 400)]
    rendered_texts = [font.render(title, True, (0, 128, 0)) for title in titles]
    rects = [text.get_rect(center=pos) for text, pos in zip(rendered_texts, positions)]

    for text, rect in zip(rendered_texts, rects):
        screen.blit(text, rect) # Display each difficulty option

    pygame.display.flip() # Update the display

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() # Quit if window is closed
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:# Get the position of the mouse click
                x, y = event.pos
                for rect, time_limit in zip(rects, [60, 30, 15]):
                    if rect.collidepoint((x, y)):
                        return time_limit

def display_cards(screen, cards_on_table, selected_indices):
    """Displays the cards on the screen, highlighting selected cards.
    The function arranges cards in a grid layout and highlights cards that are currently selected.
    """
    card_width = 100
    card_height = 150
    gap = 20   # Spacing between cards
    start_x = (screen.get_width() - (4 * card_width + 3 * gap)) // 2
    start_y = 50  # Initial position for card display

    x, y = start_x, start_y
    for idx, card in enumerate(cards_on_table):
        image = card.image
        card.rect = pygame.Rect(x, y, card_width, card_height) # Define the position and size of the card
        screen.blit(image, (x, y))  # Display the card
        if idx in selected_indices:
            # Draw a yellow rectangle around the selected card to highlight it
            pygame.draw.rect(screen, (255, 255, 0), card.rect.move(0, 20), 5)  
            pygame.draw.rect(screen, (0, 0, 255), card.rect.move(0, 20).inflate(10, 10), 5)
        x += card_width + gap
        if (idx + 1) % 4 == 0: # Move to next row after every 4 cards
            x = start_x
            y += card_height + gap

def main():
    """
    Main function to run the SET game. Initializes the game, processes user inputs, and manages game states.
    The function sets up the game environment, displays cards, handles user interactions, and updates scores.
    """
    pygame.init() # Initialize all imported pygame modules
    screen = pygame.display.set_mode((800, 600))  # Set up the main display
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 36)

    time_limit = select_difficulty(screen, small_font)  # Let player select game difficulty

    # Show "Ready" and "Go!" messages before starting the game
    show_message(screen, "Ready", font, 1, (0, 128, 0), (255, 255, 255))
    show_message(screen, "Go!", font, 0.5, (0, 128, 0), (255, 255, 255))

    # Generate and shuffle cards
    cards = [Card(n, s, c, sh) for n in range(1, 4) for s in range(1, 4) for c in range(1, 4) for sh in range(1, 4)]
    random.shuffle(cards) # Shuffle the deck of cards
    cards_on_table = cards[:12] # Display the first 12 cards on the table
    remaining_cards = cards[12:]
    selected_indices = [] # Track indices of selected cards

    start_time = time.time()  # Start timing for the game
    player_score = 0 # Player's score
    computer_score = 0
    message = ""
    message_start_time = time.time()
    message_duration = 1.5 # Duration to display messages on the screen.

    # Game loop
    running = True

    while running:
        current_time = time.time()
        elapsed_time = current_time - start_time
        time_left = max(time_limit - elapsed_time, 0)  # Compute remaining time.

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for idx, card in enumerate(cards_on_table):
                    if card.rect.collidepoint(x, y):
                        if idx in selected_indices:
                            selected_indices.remove(idx) # Deselect card if already selected
                        else:
                            selected_indices.append(idx) # Select card if not already selected

                        break

        screen.fill((255, 255, 255)) # Clear the screen
        display_cards(screen, cards_on_table, selected_indices)

        if len(selected_indices) == 3:
            if is_set(*[cards_on_table[i] for i in selected_indices]):
                player_score += 1 # Increment player's score for finding a set
                message = "You found a set!"
                for i in sorted(selected_indices, reverse=True):
                    del cards_on_table[i] # Remove found set from table
                if len(remaining_cards) >= 3:
                    cards_on_table.extend(remaining_cards[:3])
                    remaining_cards = remaining_cards[3:]
                selected_indices = []
                start_time = time.time()  # Reset the timer after a successful set
                message_start_time = current_time
            else:
                message = "Not a set, try again!"
                selected_indices = []
                message_start_time = current_time

        if time_left <= 0:
            if find_one_set(cards_on_table):
                computer_score += 1 
                message = "Time's up - Computer scores a point!"
            else:
                message = "Time's up - No sets found."
            for _ in range(3):
                if cards_on_table:
                    cards_on_table.pop(0)
            if len(remaining_cards) >= 3:
                cards_on_table.extend(remaining_cards[:3])
                remaining_cards = remaining_cards[3:]
            selected_indices = []
            start_time = time.time()  # Reset the timer for new round
            message_start_time = current_time

        if current_time - message_start_time < message_duration:
            message_text = small_font.render(message, True, (255, 0, 0))
            message_rect = message_text.get_rect(center=(400, 50))  # Display message at the top center
            screen.blit(message_text, message_rect)

        timer_text = small_font.render(f"Time left: {int(time_left)}s", True, (0, 128, 0))
        screen.blit(timer_text, (600, 20)) # Display remaining time

        score_text = small_font.render(f"Player: {player_score} | Computer: {computer_score}", True, (0, 128, 0))
        screen.blit(score_text, (300, 5)) # Display scores

        pygame.display.flip() # Update the display
        clock.tick(30)  # Limit the frame rate to 30 FPS

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
