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
        self.number = number
        self.symbol = symbol
        self.color = color
        self.shading = shading
        self.image = self.load_image()
        self.rect = None

    def load_image(self):
        color_map = {1: 'green', 2: 'purple', 3: 'red'}
        symbol_map = {1: 'diamond', 2: 'oval', 3: 'squiggle'}
        shading_map = {1: 'empty', 2: 'filled', 3: 'shaded'}
        filename = f"images/{color_map[self.color]}{symbol_map[self.symbol]}{shading_map[self.shading]}{self.number}.gif"
        return pygame.image.load(filename)

    def __eq__(self, other):
        return (self.number == other.number and self.symbol == other.symbol and
                self.color == other.color and self.shading == other.shading)

    def __str__(self):
        """Returns a string representation of the card."""
        return f"Card({self.number}, {self.symbol}, {self.color}, {self.shading})"

    def visualize(self):
        return f"{self.number}{self.symbol}{self.color}{self.shading}"

def is_set(card1, card2, card3):
    """Determines if three cards form a set based on their attributes."""
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

def find_all_sets(cards):
    sets = []
    for i in range(len(cards)):
        for j in range(i + 1, len(cards)):
            for k in range(j + 1, len(cards)):
                if is_set(cards[i], cards[j], cards[k]):
                    sets.append((i, j, k))
    return sets

def show_message(screen, text, font, duration, color, background=None):
    screen.fill((255, 255, 255) if background is None else background)
    message = font.render(text, True, color)
    rect = message.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(message, rect)
    pygame.display.flip()
    time.sleep(duration)

def select_difficulty(screen, font):
    screen.fill((255, 255, 255))
    title = font.render("SET", True, (0, 128, 0))
    title_rect = title.get_rect(center=(400, 100))
    screen.blit(title, title_rect)

    titles = ["1. Easy (60 seconds)", "2. Medium (30 seconds)", "3. Hard (15 seconds)"]
    positions = [(400, 200), (400, 300), (400, 400)]
    rendered_texts = [font.render(title, True, (0, 128, 0)) for title in titles]
    rects = [text.get_rect(center=pos) for text, pos in zip(rendered_texts, positions)]

    for text, rect in zip(rendered_texts, rects):
        screen.blit(text, rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for rect, time_limit in zip(rects, [60, 30, 15]):
                    if rect.collidepoint((x, y)):
                        return time_limit

def display_cards(screen, cards_on_table, selected_indices):
    """Displays the cards on the screen, highlighting selected cards."""
    card_width = 100
    card_height = 150
    gap = 20  
    start_x = (screen.get_width() - (4 * card_width + 3 * gap)) // 2
    start_y = 50  

    x, y = start_x, start_y
    for idx, card in enumerate(cards_on_table):
        image = card.image
        card.rect = pygame.Rect(x, y, card_width, card_height)
        screen.blit(image, (x, y))
        if idx in selected_indices:
            pygame.draw.rect(screen, (255, 255, 0), card.rect.move(0, 20), 5)  # 调整选择框位置，使其与卡牌位置匹配
            pygame.draw.rect(screen, (0, 0, 255), card.rect.move(0, 20).inflate(10, 10), 5)
        x += card_width + gap
        if (idx + 1) % 4 == 0:
            x = start_x
            y += card_height + gap

def main():
    """Main function to run the SET game."""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 36)

    time_limit = select_difficulty(screen, small_font)

    # Show "Ready" and "Go!" messages before starting the game
    show_message(screen, "Ready", font, 1, (0, 128, 0), (255, 255, 255))
    show_message(screen, "Go!", font, 0.5, (0, 128, 0), (255, 255, 255))

    cards = [Card(n, s, c, sh) for n in range(1, 4) for s in range(1, 4) for c in range(1, 4) for sh in range(1, 4)]
    random.shuffle(cards)
    cards_on_table = cards[:12]
    remaining_cards = cards[12:]
    selected_indices = []

    start_time = time.time()
    player_score = 0
    computer_score = 0
    message = ""
    message_start_time = time.time()
    message_duration = 1.5
    # Game loop
    running = True

    while running:
        current_time = time.time()
        elapsed_time = current_time - start_time
        time_left = max(time_limit - elapsed_time, 0)

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
                        break

        screen.fill((255, 255, 255))
        display_cards(screen, cards_on_table, selected_indices)

        if len(selected_indices) == 3:
            if is_set(*[cards_on_table[i] for i in selected_indices]):
                player_score += 1
                message = "You found a set!"
                for i in sorted(selected_indices, reverse=True):
                    del cards_on_table[i]
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
            message_rect = message_text.get_rect(center=(400, 50))  
            screen.blit(message_text, message_rect)

        timer_text = small_font.render(f"Time left: {int(time_left)}s", True, (0, 128, 0))
        screen.blit(timer_text, (600, 20))

        score_text = small_font.render(f"Player: {player_score} | Computer: {computer_score}", True, (0, 128, 0))
        screen.blit(score_text, (300, 5))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
